"""
DailyMind 主程序
==============
运行流程：
1. 从注册表中随机选择 5 个领域爬虫
2. 爬取文章
3. 去重（过滤已推送的）
4. 生成摘要和思考问题
5. 渲染 HTML 邮件
6. 发送
7. 记录已推送文章
"""

import random
import sys
import os
import logging

# 确保项目根目录在 path 中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import RANDOM_DOMAINS_COUNT, ARTICLES_PER_DOMAIN, MAX_DAYS, LOG_PATH
from crawlers.registry import get_random_crawlers
from crawlers.base import Article
from db import init_db, is_pushed, mark_pushed, get_stats
from digest import generate_digest
from mail_sender import send_email


def setup_logging():
    """配置日志"""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # 同时输出到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(console)


def main():
    setup_logging()
    logging.info("=" * 40)
    logging.info("🧠 DailyMind 启动")

    # 1. 初始化数据库
    init_db()
    logging.info("📦 数据库已初始化")

    # 2. 随机选择爬虫
    crawlers = get_random_crawlers(RANDOM_DOMAINS_COUNT)
    domain_names = [c.domain for c in crawlers]
    logging.info(f"🎯 本次选择的领域: {', '.join(domain_names)}")

    # 3. 爬取文章（只保留最近 3 天内的）
    all_articles: list[Article] = []
    for crawler in crawlers:
        try:
            logging.info(f"⏳ 正在爬取 [{crawler.domain}] {crawler.source}...")
            articles = crawler.fetch_recent(max_days=MAX_DAYS, max_articles=10)
            for article in articles:
                article.domain = crawler.domain
            logging.info(f"  ✅ 获取到 {len(articles)} 篇（已过滤 >3天的）")
            all_articles.extend(articles)
        except Exception as e:
            logging.error(f"  ❌ 爬取失败: {e}")

    if not all_articles:
        logging.warning("⚠️ 没有获取到任何文章，本次跳过")
        return

    logging.info(f"📚 共获取 {len(all_articles)} 篇文章")

    # 4. 去重（过滤已推送过的）
    new_articles = [a for a in all_articles if not is_pushed(a.url_hash)]
    logging.info(f"🆕 去重后剩余 {len(new_articles)} 篇新文章")

    if not new_articles:
        logging.warning("⚠️ 没有新文章，本次跳过")
        return

    # 5. 每领域随机选指定数量
    selected = []
    domain_groups = {}
    for article in new_articles:
        domain_groups.setdefault(article.domain, []).append(article)

    for domain, articles in domain_groups.items():
        if len(articles) <= ARTICLES_PER_DOMAIN:
            selected.extend(articles)
        else:
            selected.extend(random.sample(articles, ARTICLES_PER_DOMAIN))

    logging.info(f"🎯 最终精选 {len(selected)} 篇文章")

    # 6. 生成摘要
    logging.info("✍️ 正在生成摘要...")
    selected = generate_digest(selected)
    logging.info("✅ 摘要生成完成")

    # 7. 发送邮件
    logging.info("📧 正在发送邮件...")
    success = send_email(selected)
    if success:
        logging.info("✅ 邮件发送成功！")
    else:
        logging.error("❌ 邮件发送失败")
        return

    # 8. 记录已推送
    for article in selected:
        mark_pushed(article.url_hash, article.title, article.domain, article.source)
    logging.info(f"📝 已记录 {len(selected)} 篇文章到历史")

    # 9. 打印统计
    stats = get_stats()
    logging.info(f"📊 累计已推送: {stats['total']} 篇")
    for domain, count in stats["by_domain"].items():
        logging.info(f"   {domain}: {count} 篇")

    logging.info("✨ DailyMind 本次运行完成")


if __name__ == "__main__":
    main()