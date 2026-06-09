"""
生物/生命科学领域爬虫
==================
信源（RSS）: Nature（顶级科学/英文）, ScienceDaily 生物（英文）
"""

from .base import BaseCrawler, Article


class NatureCrawler(BaseCrawler):
    """Nature — 顶级科学期刊（英文）"""
    domain = "生物"
    source = "Nature"
    rss_url = "https://feeds.nature.com/nature/rss/current"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        bio_keywords = ["gene", "genome", "cell", "protein", "dna", "rna",
                        "evolution", "mutation", "bacteria", "virus",
                        "immunolog", "cancer", "stem cell", "neuroscien",
                        "biolog", "organ", "enzyme", "receptor",
                        "chromosome", "mitochondria", "photosynthesis",
                        "基因", "细胞", "蛋白质", "病毒", "细菌",
                        "进化", "免疫", "癌症", "神经", "生物"]
        filtered = [a for a in articles if any(k in a.title.lower() for k in bio_keywords)]
        return filtered


class ScienceDailyBioCrawler(BaseCrawler):
    """ScienceDaily — 生命科学（英文）"""
    domain = "生物"
    source = "ScienceDaily"
    rss_url = "https://www.sciencedaily.com/rss/plants_animals.xml"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


class ScienceDailyBioCellCrawler(BaseCrawler):
    """ScienceDaily — 细胞/微生物（英文）"""
    domain = "生物"
    source = "ScienceDaily"
    rss_url = "https://www.sciencedaily.com/rss/microbes_and_cells.xml"

    def fetch(self) -> list[Article]:
        return self.parse_rss()


BIOLOGY_CRAWLERS = [NatureCrawler, ScienceDailyBioCrawler, ScienceDailyBioCellCrawler]