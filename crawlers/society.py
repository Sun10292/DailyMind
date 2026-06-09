"""
社会领域爬虫
===========
信源（RSS）: Solidot（中文社会评论）, BBC（社会议题）
"""

from .base import BaseCrawler, Article


class SolidotSocietyCrawler(BaseCrawler):
    """Solidot — 科技/社会评论（中文）"""
    domain = "社会"
    source = "Solidot"
    rss_url = "https://www.solidot.org/index.rss"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        social_keywords = ["社会", "隐私", "法律", "监管", "教育", "健康",
                           "中国", "美国", "欧洲", "世界", "政策", "伦理",
                           "安全", "保护", "人权", "平等", "公正"]
        filtered = [a for a in articles if any(kw in a.title for kw in social_keywords)]
        return filtered


class BBCSocialCrawler(BaseCrawler):
    """BBC News — 社会议题（英文）"""
    domain = "社会"
    source = "BBC"
    rss_url = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        social_keywords = ["social", "society", "education", "health", "policy",
                           "privacy", "rights", "inequality", "justice", "poverty",
                           "housing", "crime", "community", "welfare"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in social_keywords)]
        return filtered


SOCIETY_CRAWLERS = [SolidotSocietyCrawler, BBCSocialCrawler]