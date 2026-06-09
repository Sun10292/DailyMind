"""
爬虫注册表
=========
将各领域的爬虫类汇总到一起，并提供统一的获取接口。
"""

import random
from typing import Type
from .base import BaseCrawler
from .astronomy import ASTRONOMY_CRAWLERS
from .geography import GEOGRAPHY_CRAWLERS
from .psychology import PSYCHOLOGY_CRAWLERS
from .humanities import HUMANITIES_CRAWLERS
from .nature_phil import NATURE_PHIL_CRAWLERS
from .tech import TECH_CRAWLERS

# 所有领域爬虫列表
# 每个条目: (领域名称, 该领域下的爬虫类列表)
ALL_DOMAINS = [
    ("天文", ASTRONOMY_CRAWLERS),
    ("地理", GEOGRAPHY_CRAWLERS),
    ("心理/社会", PSYCHOLOGY_CRAWLERS),
    ("人文/社科", HUMANITIES_CRAWLERS),
    ("自然/哲学", NATURE_PHIL_CRAWLERS),
    ("科技", TECH_CRAWLERS),
]


def get_random_crawlers(count: int = 4) -> list[Type[BaseCrawler]]:
    """
    随机选择 count 个领域的爬虫。
    每个领域随机选取一个信源（爬虫类）。

    返回: 爬虫类实例的列表
    """
    if count >= len(ALL_DOMAINS):
        selected_domains = ALL_DOMAINS
    else:
        selected_domains = random.sample(ALL_DOMAINS, count)

    instances = []
    for domain_name, crawler_classes in selected_domains:
        crawler_cls = random.choice(crawler_classes)
        instances.append(crawler_cls())

    return instances