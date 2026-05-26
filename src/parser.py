from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag


@dataclass(frozen=True)
class Notice:
    source_id: str
    school: str
    college: str
    title: str
    url: str
    date: str = ""

    @property
    def fingerprint(self) -> str:
        raw = f"{self.source_id}|{self.title}|{self.url}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def parse_notices(
    html: str,
    base_url: str,
    source_id: str,
    school: str,
    college: str,
    selectors: dict[str, str] | None = None,
) -> list[Notice]:
    soup = BeautifulSoup(html, "html.parser")
    selectors = selectors or {}
    notices = (
        _parse_with_selectors(soup, base_url, source_id, school, college, selectors)
        if selectors.get("item")
        else _parse_generic(soup, base_url, source_id, school, college)
    )
    return _deduplicate_notices(notices)


def _parse_with_selectors(
    soup: BeautifulSoup,
    base_url: str,
    source_id: str,
    school: str,
    college: str,
    selectors: dict[str, str],
) -> list[Notice]:
    notices: list[Notice] = []
    for item in soup.select(selectors["item"]):
        title_node = _select_one(item, selectors.get("title"))
        link_node = _select_one(item, selectors.get("link")) or title_node
        date_node = _select_one(item, selectors.get("date"))

        title = _clean_text(title_node.get_text(" ", strip=True) if title_node else item.get_text(" ", strip=True))
        if not title:
            continue

        href = link_node.get("href") if isinstance(link_node, Tag) else None
        url = urljoin(base_url, href) if href else base_url
        date = _clean_text(date_node.get_text(" ", strip=True)) if date_node else _extract_date(title)
        notices.append(Notice(source_id, school, college, _strip_leading_date(title), url, date))
    return notices


def _parse_generic(
    soup: BeautifulSoup,
    base_url: str,
    source_id: str,
    school: str,
    college: str,
) -> list[Notice]:
    notices: list[Notice] = []
    for link in soup.find_all("a"):
        title = _clean_text(link.get_text(" ", strip=True))
        href = link.get("href")
        if not title or not href or len(title) < 4:
            continue
        if _looks_like_navigation(title):
            continue

        url = urljoin(base_url, str(href))
        date = _extract_date(title)
        notices.append(Notice(source_id, school, college, _strip_leading_date(title), url, date))
    return notices


def _select_one(item: Tag, selector: str | None) -> Tag | None:
    if not selector:
        return None
    return item.select_one(selector)


def _deduplicate_notices(notices: list[Notice]) -> list[Notice]:
    seen: set[str] = set()
    result: list[Notice] = []
    for notice in notices:
        key = f"{notice.title}|{notice.url}"
        if key in seen:
            continue
        seen.add(key)
        result.append(notice)
    return result


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _looks_like_navigation(title: str) -> bool:
    navigation_words = {
        "English",
        "学院概况",
        "学院简介",
        "院长致辞",
        "现任领导",
        "师资队伍",
        "人才培养",
        "科学研究",
        "新闻动态",
        "通知公告",
        "学术交流",
        "人才招聘",
        "工作台",
        "查看更多",
    }
    return title in navigation_words or title.startswith("######")


def _extract_date(title: str) -> str:
    patterns = [
        r"\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}日?",
        r"\d{1,2}\s*\d{1,2}月",
        r"\d{1,2}月\d{1,2}日",
    ]
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            return match.group(0)
    return ""


def _strip_leading_date(title: str) -> str:
    patterns = [
        r"^\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}日?\s*",
        r"^\d{1,2}\s*\d{1,2}月\s*",
        r"^\d{1,2}月\d{1,2}日\s*",
    ]
    result = title
    for pattern in patterns:
        result = re.sub(pattern, "", result).strip()
    return result

