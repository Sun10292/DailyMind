"""
邮件发送模块
==========
将文章摘要渲染为 HTML 邮件并发送。
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, timedelta
from typing import List
from config import SMTP_CONFIG, TO_EMAIL
from crawlers.base import Article


def build_html(articles: List[Article]) -> str:
    """将文章列表渲染为 HTML"""

    # 按领域分组
    domains = {}
    for article in articles:
        domain = article.domain or "未分类"
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(article)

    domain_emoji = {
        "天文": "🌌",
        "地理": "🌍",
        "心理": "🧠",
        "社会": "👥",
        "人文": "🎭",
        "自然": "🌿",
        "哲学": "💭",
        "科技": "🤖",
        "经济": "💰",
        "生物": "🧬",
    }

    today = date.today().isoformat()

    # 构建每个领域的 HTML
    sections_html = ""
    for domain, domain_articles in domains.items():
        emoji = domain_emoji.get(domain, "📖")

        articles_html = ""
        for i, article in enumerate(domain_articles, 1):
            summary_html = (
                f"<p style='color:#444; line-height:1.7; font-size:14px; margin:8px 0;'>{article.summary}</p>"
            ) if article.summary else ""

            question_html = (
                f"<div style='background:#f0f7ff; border-left:3px solid #4a90d9; padding:10px 14px; "
                f"margin:10px 0; border-radius:4px;'>"
                f"<span style='color:#4a90d9; font-weight:bold;'>💭 想一想：</span>"
                f"<span style='color:#555;'>{article.thinking_question}</span>"
                f"</div>"
            ) if article.thinking_question else ""

            articles_html += f"""
            <div style="margin-bottom:20px; padding:16px; background:#fafafa; border-radius:8px; border:1px solid #eee;">
                <div style="display:flex; align-items:flex-start; gap:10px;">
                    <span style="color:#999; font-size:12px; min-width:20px;">#{i}</span>
                    <div style="flex:1;">
                        <a href="{article.url}" target="_blank"
                           style="color:#333; text-decoration:none; font-size:16px; font-weight:bold; line-height:1.4;"
                           onmouseover="this.style.color='#4a90d9'" onmouseout="this.style.color='#333'">
                            {article.title}
                        </a>
                        <div style="color:#999; font-size:12px; margin-top:4px;">
                            来源: {article.source}
                        </div>
                        {summary_html}
                        {question_html}
                    </div>
                </div>
            </div>"""

        sections_html += f"""
        <div style="margin-bottom:30px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:15px;
                        padding-bottom:8px; border-bottom:2px solid #4a90d9;">
                <span style="font-size:22px;">{emoji}</span>
                <h2 style="margin:0; color:#333; font-size:18px;">{domain}</h2>
            </div>
            {articles_html}
        </div>"""

    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin:0; padding:0; background:#f5f5f5; font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;">
        <div style="max-width:640px; margin:0 auto; background:#fff;">

            <!-- 头部 -->
            <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding:30px 24px; text-align:center; border-radius:0 0 20px 20px;">
                <div style="font-size:36px; margin-bottom:8px;">🧠</div>
                <h1 style="color:#fff; margin:0; font-size:22px; letter-spacing:2px;">DailyMind</h1>
                <p style="color:rgba(255,255,255,0.85); margin:6px 0 0 0; font-size:14px;">
                    每日跨领域思维食粮 · {today}
                </p>
                <p style="color:rgba(255,255,255,0.6); margin:10px 0 0 0; font-size:12px;">
                    今日精选 {len(articles)} 篇文章 · {len(domains)} 个领域
                </p>
            </div>

            <!-- 引言 -->
            <div style="padding:20px 24px 10px; text-align:center;">
                <p style="color:#888; font-size:13px; font-style:italic; margin:0;">
                    "不是所有的知识都要立刻有用，有些思考本身就是目的。"
                </p>
            </div>

            <!-- 正文 -->
            <div style="padding:10px 24px 24px;">
                {sections_html}
            </div>

            <!-- 底部 -->
            <div style="background:#fafafa; padding:20px 24px; text-align:center;
                        border-top:1px solid #eee; border-radius:20px 20px 0 0;">
                <p style="color:#bbb; font-size:12px; margin:0;">
                    DailyMind · 不追踪 · 不算法 · 只为思考<br>
                    明日 {(date.today() + timedelta(days=1)).isoformat()} 晚 8 点再见
                </p>
            </div>

        </div>
    </body>
    </html>
    """
    return html


def send_email(articles: List[Article]) -> bool:
    """发送邮件"""
    html_content = build_html(articles)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🧠 DailyMind | 每日跨领域摘要 ({date.today().isoformat()})"
    msg["From"] = SMTP_CONFIG["user"]
    msg["To"] = TO_EMAIL

    # 纯文本后备
    text_content = f"DailyMind - {date.today().isoformat()}\n\n"
    for a in articles:
        text_content += f"- [{a.domain}] {a.title}\n  {a.url}\n\n"

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            SMTP_CONFIG["host"], SMTP_CONFIG["port"], context=context
        ) as server:
            server.login(SMTP_CONFIG["user"], SMTP_CONFIG["password"])
            server.sendmail(SMTP_CONFIG["user"], TO_EMAIL, msg.as_string())
        return True
    except Exception as e:
        print(f"[邮件发送失败] {e}")
        return False