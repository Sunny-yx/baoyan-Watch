from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

from .parser import Notice


def send_email(notices: list[Notice]) -> bool:
    if not notices:
        return False

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port_raw = os.getenv("SMTP_PORT") or "465"
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    mail_to = os.getenv("MAIL_TO")

    missing = [
        name
        for name, value in {
            "SMTP_HOST": smtp_host,
            "SMTP_USER": smtp_user,
            "SMTP_PASSWORD": smtp_password,
            "MAIL_TO": mail_to,
        }.items()
        if not value
    ]
    if missing:
        print(f"Email skipped because secrets are missing: {', '.join(missing)}")
        return False

    try:
        smtp_port = int(smtp_port_raw)
    except ValueError:
        print("Email skipped because SMTP_PORT must be a number.")
        return False

    message = EmailMessage()
    message["Subject"] = f"保研通知提醒：发现 {len(notices)} 条新通知"
    message["From"] = smtp_user
    message["To"] = mail_to
    message.set_content(_render_email_body(notices))

    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(message)
    else:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)
    return True


def _render_email_body(notices: list[Notice]) -> str:
    lines = [
        "您好，",
        "",
        "你关注的院校发布了新的保研相关通知，详情如下：",
        "",
    ]
    for index, notice in enumerate(notices, start=1):
        date_text = notice.date or "官网未识别到发布日期"
        lines.extend(
            [
                f"{index}. 你关注的 {notice.school} {notice.college} 发布了《{notice.title}》通知。",
                f"   发布日期：{date_text}",
                f"   通知链接：{notice.url}",
                "",
            ]
        )
    lines.extend(
        [
            "以上信息由 BaoyanWatch 自动监控生成，请以学校或学院官网原文为准。",
            "",
            "祝顺利。",
        ]
    )
    return "\n".join(lines)
