"""
社科领域爬虫
===========
信源（RSS）: 36氪（商业/社会分析/中文）, New Scientist（社科方向/英文）
"""

from .base import BaseCrawler, Article


class Kr36SocialCrawler(BaseCrawler):
    """36氪 — 商业/社会分析/深度（中文）"""
    domain = "社科"
    source = "36氪"
    rss_url = "https://36kr.com/feed"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        social_keywords = ["社会", "调查", "报告", "研究", "数据", "趋势",
                           "人口", "城市", "经济", "消费", "市场", "行业",
                           "深度", "分析", "观察", "现象"]
        filtered = [a for a in articles if any(kw in a.title for kw in social_keywords)]
        return filtered


class NewScientistSocialCrawler(BaseCrawler):
    """New Scientist — 社科/趋势（英文）"""
    domain = "社科"
    source = "New Scientist"
    rss_url = "https://www.newscientist.com/feed/home"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        social_keywords = ["society", "culture", "history", "archaeolog",
                           "anthropology", "sociology", "psychology",
                           "population", "urban", "city", "human"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in social_keywords)]
        return filtered


SOCIAL_SCIENCE_CRAWLERS = [Kr36SocialCrawler, NewScientistSocialCrawler]