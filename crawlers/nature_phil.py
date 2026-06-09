"""
自然/哲学领域爬虫
===============
信源（RSS）: New Scientist（英文）, ScienceDaily Mind（英文）
"""

from .base import BaseCrawler, Article


class NewScientistNatureCrawler(BaseCrawler):
    """New Scientist — 自然/科学（英文）"""
    domain = "自然/哲学"
    source = "New Scientist"
    rss_url = "https://www.newscientist.com/feed/home"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        kw = ["consciousness", "evolution", "genetic", "dna",
              "neuroscien", "mental", "memory", "sleep",
              "animal", "plant", "fungi", "bacteria", "virus", "cell",
              "quantum", "physics", "math", "nature",
              "物种", "意识", "基因", "大脑", "神经", "动物",
              "植物", "量子", "物理", "数学"]
        filtered = [a for a in articles if any(k in a.title.lower() for k in kw)]
        return filtered


class ScienceDailyMindCrawler(BaseCrawler):
    """ScienceDaily — 心理与大脑（英文）"""
    domain = "自然/哲学"
    source = "ScienceDaily"
    rss_url = "https://www.sciencedaily.com/rss/mind_brain.xml"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


NATURE_PHIL_CRAWLERS = [NewScientistNatureCrawler, ScienceDailyMindCrawler]