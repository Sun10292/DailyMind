"""
心理领域爬虫
===========
信源（RSS）: ScienceDaily Mind（英文）, 爱范儿（心理/认知相关中文）
"""

from .base import BaseCrawler, Article


class ScienceDailyMindCrawler(BaseCrawler):
    """ScienceDaily — 心理与大脑（英文）"""
    domain = "心理"
    source = "ScienceDaily"
    rss_url = "https://www.sciencedaily.com/rss/mind_brain.xml"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


class IfanrPsychCrawler(BaseCrawler):
    """爱范儿 — 科技/心理/认知（中文）"""
    domain = "心理"
    source = "爱范儿"
    rss_url = "https://www.ifanr.com/feed"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        psych_keywords = ["心理", "情绪", "认知", "大脑", "记忆", "注意力",
                          "睡眠", "压力", "焦虑", "抑郁", "幸福", "习惯",
                          "mind", "brain", "mental", "emotion", "psych"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in psych_keywords)]
        return filtered if filtered else articles[:3]


PSYCHOLOGY_CRAWLERS = [ScienceDailyMindCrawler, IfanrPsychCrawler]