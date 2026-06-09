"""
地理领域爬虫
===========
信源（RSS）: ScienceDaily（考古/地理/英文）, Solidot（中文地理相关）
"""

from .base import BaseCrawler, Article


class ScienceDailyGeoCrawler(BaseCrawler):
    """ScienceDaily — 社会/考古/地理（英文）"""
    domain = "地理"
    source = "ScienceDaily"
    rss_url = "https://www.sciencedaily.com/rss/science_society.xml"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        geo_keywords = ["earth", "climate", "environment", "ocean", "volcano",
                        "earthquake", "fossil", "dinosaur", "archaeolog", "ancient",
                        "glacier", "ice", "weather", "map", "migration", "hominin",
                        "human evolution"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in geo_keywords)]
        return filtered


class SolidotGeoCrawler(BaseCrawler):
    """Solidot — 科技/社会/地理（中文）"""
    domain = "地理"
    source = "Solidot"
    rss_url = "https://www.solidot.org/index.rss"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        geo_keywords = ["地球", "气候", "环境", "海洋", "火山", "地震",
                        "化石", "考古", "冰川", "天气", "地图", "地理",
                        "生态", "物种", "森林"]
        filtered = [a for a in articles if any(kw in a.title for kw in geo_keywords)]
        return filtered


GEOGRAPHY_CRAWLERS = [ScienceDailyGeoCrawler, SolidotGeoCrawler]