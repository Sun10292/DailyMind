"""
爬虫基类
========
所有领域爬虫都继承自 BaseCrawler。
"""

import hashlib
import random
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup


@dataclass
class Article:
    """一篇文章的数据"""
    title: str                    # 标题
    url: str                      # 原文链接
    summary: str = ""             # 摘要（由 digest 模块填充）
    thinking_question: str = ""   # 思考引导问题（由 digest 模块填充）
    domain: str = ""              # 领域
    source: str = ""              # 来源名称
    url_hash: str = ""            # URL 的哈希值（用于去重）
    published_date: str = ""       # 发布日期，格式 YYYY-MM-DD

    def __post_init__(self):
        if not self.url_hash:
            self.url_hash = hashlib.md5(self.url.encode()).hexdigest()


class BaseCrawler(ABC):
    """爬虫基类，所有领域爬虫继承此类"""

    # 领域名称
    domain: str = ""
    # 来源名称
    source: str = ""
    # 来源网站URL
    source_url: str = ""
    # RSS feed URL（优先使用）
    rss_url: str = ""
    # HTTP 请求头，模拟浏览器
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    # 请求超时（秒）
    timeout = 15

    @abstractmethod
    def fetch(self) -> list[Article]:
        """抓取文章列表，子类必须实现此方法"""
        ...

    # ---------- RSS 解析 ----------

    def parse_rss(self, rss_url: str = None) -> list[Article]:
        """
        解析 RSS feed，返回文章列表。
        兼容 RSS 2.0 和 Atom 格式。
        """
        url = rss_url or self.rss_url
        if not url:
            return []

        resp = requests.get(url, headers=self.headers, timeout=self.timeout)
        resp.encoding = "utf-8"
        root = ET.fromstring(resp.text)

        articles = []

        # RSS 2.0: /rss/channel/item
        for item in root.iter("item"):
            title = self._get_xml_text(item, "title")
            link = self._get_xml_text(item, "link")
            pub_date_str = self._get_xml_text(item, "pubDate")
            desc = self._get_xml_text(item, "description")

            if not title or not link:
                continue

            pub_date = self._parse_rss_date(pub_date_str) if pub_date_str else ""

            articles.append(Article(
                title=title.strip(),
                url=link.strip(),
                summary=(desc or "")[:300],
                published_date=pub_date,
                source=self.source,
            ))

        # Atom: /feed/entry
        for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
            title = self._get_xml_text(entry, "{http://www.w3.org/2005/Atom}title")
            link_el = entry.find("{http://www.w3.org/2005/Atom}link")
            link = link_el.get("href") if link_el is not None else ""
            pub_date_str = (
                self._get_xml_text(entry, "{http://www.w3.org/2005/Atom}published")
                or self._get_xml_text(entry, "{http://www.w3.org/2005/Atom}updated")
            )
            desc = self._get_xml_text(entry, "{http://www.w3.org/2005/Atom}summary") or ""

            if not title or not link:
                continue

            pub_date = self._parse_atom_date(pub_date_str) if pub_date_str else ""

            articles.append(Article(
                title=title.strip(),
                url=link.strip(),
                summary=(desc or "")[:300],
                published_date=pub_date,
                source=self.source,
            ))

        return articles

    def _get_xml_text(self, parent, tag: str) -> str:
        # 兼容无命名空间和有命名空间
        el = parent.find(tag)
        if el is None:
            # 尝试去掉命名空间查找
            local = tag.split("}")[-1] if "}" in tag else tag
            for child in parent:
                ctag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                if ctag == local:
                    el = child
                    break
        return el.text.strip() if el is not None and el.text else ""

    def _parse_rss_date(self, date_str: str) -> str:
        """
        解析 RSS 2.0 日期格式。
        处理: 'Mon, 08 Jun 2026 06:09:53 GMT'
              'Tue, 09 Jun 2026 04:48:10 +0000'
              '2026-06-09 14:19:43  +0800'
              'Mon, 08 Jun 2026 19:23:33 EDT'
        """
        try:
            s = date_str.strip()
            # 统一空格：多个空格变一个
            import re as _re
            s = _re.sub(r'\s+', ' ', s)
            # 替换常见的时区缩写为 +0000（让 Python 解析）
            tz_map = {"GMT": "+0000", "UTC": "+0000", "EDT": "-0400", "EST": "-0500",
                      "PDT": "-0700", "PST": "-0800", "CDT": "-0500", "CST": "-0600",
                      "BST": "+0100", "CEST": "+0200", "CET": "+0100", "JST": "+0900",
                      "AEST": "+1000", "AEDT": "+1100"}
            parts = s.split()
            if parts and parts[-1] in tz_map:
                s = " ".join(parts[:-1]) + " " + tz_map[parts[-1]]

            for fmt in [
                "%a, %d %b %Y %H:%M:%S %z",
                "%Y-%m-%d %H:%M:%S %z",
                "%a, %d %b %Y %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d",
            ]:
                try:
                    dt = datetime.strptime(s, fmt)
                    return dt.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            return ""
        except Exception:
            return ""

    def _parse_atom_date(self, date_str: str) -> str:
        """解析 Atom 日期格式，如 '2026-06-08T19:58:30-04:00'"""
        try:
            s = date_str.strip()
            import re as _re
            s = _re.sub(r'\s+', ' ', s)
            for fmt in [
                "%Y-%m-%dT%H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d",
            ]:
                try:
                    # 去掉时区中的冒号（如 -04:00 -> -0400）
                    # Python 3.7+ 支持 %z 的冒号格式，3.12 应该没问题
                    dt = datetime.strptime(s, fmt)
                    return dt.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            return ""
        except Exception:
            return ""

    # ---------- HTML 解析（次要） ----------

    def get_soup(self, url: str = None) -> BeautifulSoup:
        """获取页面并解析为 BeautifulSoup 对象"""
        url = url or self.source_url
        resp = requests.get(url, headers=self.headers, timeout=self.timeout)
        resp.encoding = resp.apparent_encoding
        return BeautifulSoup(resp.text, "html.parser")

    def pick_random(self, articles: list[Article], n: int = 2) -> list[Article]:
        """从文章列表中随机选 n 篇"""
        if len(articles) <= n:
            return articles
        return random.sample(articles, n)

    def filter_recent(self, articles: list[Article], max_days: int = 3) -> list[Article]:
        """
        只保留最近 max_days 天内的文章。
        如果文章没有 published_date 或者解析失败，默认保留（放宽策略）。
        """
        cutoff = bj_now() - timedelta(days=max_days)
        filtered = []
        for a in articles:
            if not a.published_date:
                filtered.append(a)  # 没日期信息就保留
                continue
            try:
                pub_date = datetime.strptime(a.published_date, "%Y-%m-%d").replace(tzinfo=BJT)
                if pub_date >= cutoff:
                    filtered.append(a)
            except ValueError:
                filtered.append(a)  # 日期解析失败也保留
        return filtered

    def fetch_recent(self, max_days: int = 3, max_articles: int = 10) -> list[Article]:
        """
        抓取并过滤出最近的文章。
        子类实现 fetch()，这个方法是统一入口。
        """
        articles = self.fetch()
        recent = self.filter_recent(articles, max_days=max_days)
        return recent[:max_articles]


# 北京时间
BJT = timezone(timedelta(hours=8))


def bj_now() -> datetime:
    """返回当前北京时间"""
    return datetime.now(BJT)