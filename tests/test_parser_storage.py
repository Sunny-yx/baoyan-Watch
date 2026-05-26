from src.parser import Notice, parse_notices
from src.storage import filter_new_notices


def test_parse_generic_normalizes_relative_links() -> None:
    html = '<html><body><a href="/notice/1.html">26 5月 全国优秀大学生暑期交流营报名通知</a></body></html>'

    notices = parse_notices(html, "https://aim.sustech.edu.cn/", "sustech-aim", "南方科技大学", "自动化与智能制造学院")

    assert notices[0].title == "全国优秀大学生暑期交流营报名通知"
    assert notices[0].date == "26 5月"
    assert notices[0].url == "https://aim.sustech.edu.cn/notice/1.html"


def test_filter_new_notices_skips_seen_fingerprints() -> None:
    seen_notice = Notice("sustech-aim", "南方科技大学", "自动化与智能制造学院", "全国优秀大学生暑期交流营报名通知", "https://example.com/a")
    new_notice = Notice("sustech-aim", "南方科技大学", "自动化与智能制造学院", "预推免报名通知", "https://example.com/b")

    result = filter_new_notices([seen_notice, new_notice], {seen_notice.fingerprint})

    assert result == [new_notice]

