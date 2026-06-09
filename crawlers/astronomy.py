"""
天文领域爬虫
===========
信源（RSS）: BBC Science（天文过滤）, Ars Technica（太空）
"""

from .base import BaseCrawler, Article


class SkyNewsCrawler(BaseCrawler):
    """BBC Science — 天文/空间新闻（英文）"""
    domain = "天文"
    source = "BBC Science"
    rss_url = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        astro_keywords = ["space", "nasa", "astronom", "planet", "star", "galax",
                          "telescope", "mars", "moon", "solar", "cosmic", "universe",
                          "saturn", "jupiter", "venus", "mercury", "comet", "asteroid",
                          "太空", "天文", "宇宙", "火星", "月球"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in astro_keywords)]
        return filtered if filtered else articles[:3]


class ArTechSpaceCrawler(BaseCrawler):
    """Ars Technica — 太空/航天（英文）"""
    domain = "天文"
    source = "Ars Technica"
    rss_url = "https://feeds.arstechnica.com/arstechnica/index"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        space_keywords = ["space", "nasa", "astronom", "mars", "moon", "satellit",
                          "telescop", "rocket", "launch", "orbit"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in space_keywords)]
        return filtered if filtered else articles[:2]


ASTRONOMY_CRAWLERS = [SkyNewsCrawler, ArTechSpaceCrawler]