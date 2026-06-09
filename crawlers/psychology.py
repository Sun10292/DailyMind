"""
心理/社会领域爬虫
===============
信源（RSS）: ScienceDaily Mind（英文）, Solidot（中文科技/社会）
"""

from .base import BaseCrawler, Article


class ScienceDailyMindCrawler(BaseCrawler):
    """ScienceDaily — 心理与大脑（英文）"""
    domain = "心理/社会"
    source = "ScienceDaily"
    rss_url = "https://www.sciencedaily.com/rss/mind_brain.xml"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


class SolidotSocialCrawler(BaseCrawler):
    """Solidot — 科技/社会评论（中文）"""
    domain = "心理/社会"
    source = "Solidot"
    rss_url = "https://www.solidot.org/index.rss"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        # Solidot 内容偏科技+社会，适合心理/社会领域
        social_keywords = ["社会", "隐私", "法律", "监管", "教育", "健康",
                           "心理", "大脑", "研究", "调查", "报告", "调查",
                           "中国", "美国", "欧洲", "世界", "AI", "人工"]
        filtered = [a for a in articles if any(kw in a.title for kw in social_keywords)]
        return filtered if filtered else articles[:5]


PSYCHOLOGY_CRAWLERS = [ScienceDailyMindCrawler, SolidotSocialCrawler]