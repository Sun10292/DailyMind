"""
经济领域爬虫
===========
信源（RSS）: 36氪（商业/财经/中文）, BBC Business（英文）
"""

from .base import BaseCrawler, Article


class Kr36EconomyCrawler(BaseCrawler):
    """36氪 — 商业/财经/经济（中文）"""
    domain = "经济"
    source = "36氪"
    rss_url = "https://36kr.com/feed"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        econ_keywords = ["融资", "IPO", "上市", "投资", "收购", "财报",
                         "营收", "利润", "增长", "经济", "市场", "股市",
                         "创业", "商业", "消费", "品牌", "电商", "出海",
                         "资本", "估值", "交易", "基金", "股票"]
        filtered = [a for a in articles if any(kw in a.title for kw in econ_keywords)]
        return filtered if filtered else articles[:5]


class BBCBusinessCrawler(BaseCrawler):
    """BBC News — 商业/经济（英文）"""
    domain = "经济"
    source = "BBC Business"
    rss_url = "https://feeds.bbci.co.uk/news/business/rss.xml"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


ECONOMY_CRAWLERS = [Kr36EconomyCrawler, BBCBusinessCrawler]