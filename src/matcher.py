from __future__ import annotations

from .parser import Notice


def matches_keywords(notice: Notice, keywords: list[str], match_mode: str = "any") -> bool:
    text = notice.title.casefold()
    normalized_keywords = [keyword.casefold() for keyword in keywords if keyword.strip()]
    if not normalized_keywords:
        return False
    if match_mode == "all":
        return all(keyword in text for keyword in normalized_keywords)
    if match_mode == "any":
        return any(keyword in text for keyword in normalized_keywords)
    raise ValueError("match_mode must be either 'any' or 'all'.")

