from src.notifier import _render_email_body
from src.parser import Notice


def test_render_email_body_uses_formal_notice_wording() -> None:
    notice = Notice(
        "sustech-aim",
        "南方科技大学",
        "自动化与智能制造学院",
        "全国优秀大学生暑期交流营报名通知",
        "https://example.com/notice/1",
        "2026年5月26日",
    )

    body = _render_email_body([notice])

    assert "你关注的 南方科技大学 自动化与智能制造学院 发布了《全国优秀大学生暑期交流营报名通知》通知。" in body
    assert "发布日期：2026年5月26日" in body
    assert "通知链接：https://example.com/notice/1" in body
    assert "请以学校或学院官网原文为准" in body
