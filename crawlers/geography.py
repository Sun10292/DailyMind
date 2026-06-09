"""
地理领域爬虫
===========
信源（RSS）: ScienceDaily（考古/地理）, New Scientist（环境）, 爱范儿（旅行/地理）
"""

from .base import BaseCrawler, Article


class ScienceDailySocietyCrawler(BaseCrawler):
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
        return filtered if filtered else articles[:5]


class NewScientistGeoCrawler(BaseCrawler):
    """New Scientist — 环境/地理（英文）"""
    domain = "地理"
    source = "New Scientist"
    rss_url = "https://www.newscientist.com/feed/home"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        geo_keywords = ["earth", "climate", "environment", "ocean", "volcano",
                        "earthquake", "fossil", "dinosaur", "archaeolog", "ancient",
                        "planet", "geolog"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in geo_keywords)]
        return filtered if filtered else articles[:3]


GEOGRAPHY_CRAWLERS = [ScienceDailySocietyCrawler, NewScientistGeoCrawler]