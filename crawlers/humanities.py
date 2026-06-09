"""
人文领域爬虫
===========
信源（RSS）: Aeon（人文/文化/历史/英文）, The Guardian Books（书评/英文）
"""

from .base import BaseCrawler, Article


class AeonHumanitiesCrawler(BaseCrawler):
    """Aeon — 哲学/文化/历史（英文）"""
    domain = "人文"
    source = "Aeon"
    rss_url = "https://aeon.co/feed.rss"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        kw = ["philosoph", "history", "art", "literature", "language",
              "ancient", "medieval", "poetry", "fiction", "culture",
              "伦理", "哲学", "历史", "艺术", "文学", "文明"]
        filtered = [a for a in articles if any(k in a.title.lower() for k in kw)]
        return filtered if filtered else articles[:2]


class GuardianBooksCrawler(BaseCrawler):
    """The Guardian — 书评/文化（英文）"""
    domain = "人文"
    source = "The Guardian"
    rss_url = "https://www.theguardian.com/books/rss"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


HUMANITIES_CRAWLERS = [AeonHumanitiesCrawler, GuardianBooksCrawler]