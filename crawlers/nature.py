"""
自然领域爬虫
===========
信源（RSS）: New Scientist（自然/科学/英文）, BBC Science（自然方向/英文）
"""

from .base import BaseCrawler, Article


class NewScientistNatureCrawler(BaseCrawler):
    """New Scientist — 自然/科学（英文）"""
    domain = "自然"
    source = "New Scientist"
    rss_url = "https://www.newscientist.com/feed/home"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        kw = ["animal", "plant", "fungi", "bacteria", "virus", "cell",
              "evolution", "genetic", "dna", "gene", "species",
              "ocean", "forest", "climate", "ecolog", "conservation",
              "bird", "fish", "insect", "dinosaur", "fossil",
              "动物", "植物", "物种", "生态", "进化", "基因"]
        filtered = [a for a in articles if any(k in a.title.lower() for k in kw)]
        return filtered


class BBCNatureCrawler(BaseCrawler):
    """BBC Science — 自然/环境（英文）"""
    domain = "自然"
    source = "BBC Science"
    rss_url = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        nature_keywords = ["animal", "plant", "bird", "fish", "insect",
                           "ocean", "forest", "climate", "wildlife",
                           "nature", "species", "extinct", "endangered",
                           "ecolog", "conservation"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in nature_keywords)]
        return filtered


NATURE_CRAWLERS = [NewScientistNatureCrawler, BBCNatureCrawler]