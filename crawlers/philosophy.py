"""
哲学领域爬虫
===========
信源（RSS）: Aeon（哲学/思想/英文）, New Scientist（意识/哲学/英文）
"""

from .base import BaseCrawler, Article


class AeonPhilosophyCrawler(BaseCrawler):
    """Aeon — 哲学/思想/文化（英文）"""
    domain = "哲学"
    source = "Aeon"
    rss_url = "https://aeon.co/feed.rss"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        kw = ["philosoph", "consciousness", "ethics", "moral", "meaning",
              "exist", "reason", "truth", "knowledge", "belief",
              "mind", "self", "free will", "reality", "perception",
              "伦理", "道德", "存在", "意义", "真理", "自由",
              "意识", "思维", "理性"]
        filtered = [a for a in articles if any(k in a.title.lower() for k in kw)]
        return filtered if filtered else articles[:2]


class NewScientistPhilCrawler(BaseCrawler):
    """New Scientist — 意识/哲学/思想（英文）"""
    domain = "哲学"
    source = "New Scientist"
    rss_url = "https://www.newscientist.com/feed/home"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        kw = ["consciousness", "philosoph", "ethics", "moral",
              "quantum", "reality", "mind", "brain", "perception",
              "identity", "meaning", "exist", "free will"]
        filtered = [a for a in articles if any(k in a.title.lower() for k in kw)]
        return filtered if filtered else articles[:2]


PHILOSOPHY_CRAWLERS = [AeonPhilosophyCrawler, NewScientistPhilCrawler]