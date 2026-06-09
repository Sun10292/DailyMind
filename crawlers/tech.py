"""
科技领域爬虫
===========
信源（RSS）: 36氪（中文）, Ars Technica（英文）, 爱范儿（中文科技）
"""

from .base import BaseCrawler, Article


class Kr36RssCrawler(BaseCrawler):
    """36氪 — 科技/商业资讯（中文）"""
    domain = "科技"
    source = "36氪"
    rss_url = "https://36kr.com/feed"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


class ArsTechnicaCrawler(BaseCrawler):
    """Ars Technica — 深度科技（英文）"""
    domain = "科技"
    source = "Ars Technica"
    rss_url = "https://feeds.arstechnica.com/arstechnica/index"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


class IfanrTechCrawler(BaseCrawler):
    """爱范儿 — 科技/数码（中文）"""
    domain = "科技"
    source = "爱范儿"
    rss_url = "https://www.ifanr.com/feed"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


TECH_CRAWLERS = [Kr36RssCrawler, ArsTechnicaCrawler, IfanrTechCrawler]