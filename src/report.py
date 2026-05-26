from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .parser import Notice


def write_report(notices: list[Notice], path: Path | str = "docs/latest.md") -> None:
    report_path = Path(path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z")

    lines = [
        "# BaoyanWatch 最新通知",
        "",
        f"更新时间：{now}",
        "",
    ]

    if not notices:
        lines.extend(["本次没有发现新的保研相关通知。", ""])
    else:
        lines.extend(["| 学校 | 学院 | 日期 | 标题 |", "| --- | --- | --- | --- |"])
        for notice in notices:
            title = notice.title.replace("|", "\\|")
            lines.append(
                f"| {notice.school} | {notice.college} | {notice.date or '未识别'} | [{title}]({notice.url}) |"
            )
        lines.append("")

    lines.append("> BaoyanWatch 只做提醒，请以官网原文为准。")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")

