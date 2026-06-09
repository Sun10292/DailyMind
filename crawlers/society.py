"""
社会领域爬虫
===========
信源（RSS）: Solidot（中文）, BBC（英文社会议题）,
             36氪（中文社会分析）, New Scientist（英文社科趋势）
"""

from .base import BaseCrawler, Article


class SolidotSocietyCrawler(BaseCrawler):
    """Solidot — 科技/社会评论（中文）"""
    domain = "社会"
    source = "Solidot"
    rss_url = "https://www.solidot.org/index.rss"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        social_keywords = ["社会", "隐私", "法律", "监管", "教育", "健康",
                           "中国", "美国", "欧洲", "世界", "政策", "伦理",
                           "安全", "保护", "人权", "平等", "公正"]
        filtered = [a for a in articles if any(kw in a.title for kw in social_keywords)]
        return filtered


class BBCSocialCrawler(BaseCrawler):
    """BBC News — 社会议题（英文）"""
    domain = "社会"
    source = "BBC"
    rss_url = "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        social_keywords = ["social", "society", "education", "health", "policy",
                           "privacy", "rights", "inequality", "justice", "poverty",
                           "housing", "crime", "community", "welfare"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in social_keywords)]
        return filtered


class Kr36SocialCrawler(BaseCrawler):
    """36氪 — 商业/社会分析/深度（中文）"""
    domain = "社会"
    source = "36氪"
    rss_url = "https://36kr.com/feed"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        social_keywords = ["社会", "调查", "报告", "研究", "数据", "趋势",
                           "人口", "城市", "经济", "消费", "市场", "行业",
                           "深度", "分析", "观察", "现象"]
        filtered = [a for a in articles if any(kw in a.title for kw in social_keywords)]
        return filtered


class NewScientistSocialCrawler(BaseCrawler):
    """New Scientist — 社科/趋势（英文）"""
    domain = "社会"
    source = "New Scientist"
    rss_url = "https://www.newscientist.com/feed/home"

    def fetch(self) -> list[Article]:
        articles = self.parse_rss()
        social_keywords = ["society", "culture", "history", "archaeolog",
                           "anthropology", "sociology", "psychology",
                           "population", "urban", "city", "human"]
        filtered = [a for a in articles if any(kw in a.title.lower() for kw in social_keywords)]
        return filtered


SOCIETY_CRAWLERS = [SolidotSocietyCrawler, BBCSocialCrawler, Kr36SocialCrawler, NewScientistSocialCrawler]