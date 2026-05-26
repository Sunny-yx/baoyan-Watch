from src.matcher import matches_keywords
from src.parser import Notice


def make_notice(title: str) -> Notice:
    return Notice("sustech-aim", "南方科技大学", "自动化与智能制造学院", title, "https://example.com")


def test_match_mode_all_matches_sustech_acceptance_title() -> None:
    notice = make_notice("南科大自动化与智能制造学院2026年全国优秀大学生暑期交流营报名通知")

    assert matches_keywords(notice, ["全国优秀大学生", "暑期", "营"], "all")


def test_match_mode_all_rejects_title_that_only_contains_ying() -> None:
    notice = make_notice("学院举行科研训练营活动通知")

    assert not matches_keywords(notice, ["全国优秀大学生", "暑期", "营"], "all")


def test_match_mode_any_accepts_any_global_keyword() -> None:
    notice = make_notice("2026年推荐免试研究生招生通知")

    assert matches_keywords(notice, ["夏令营", "推荐免试"], "any")

