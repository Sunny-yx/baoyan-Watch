from __future__ import annotations

import requests


DEFAULT_TIMEOUT_SECONDS = 20
USER_AGENT = (
    "BaoyanWatch/0.1 "
    "(https://github.com/your-name/baoyan-watch; respectful academic notice monitor)"
)


def fetch_html(url: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> str:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()
    if not response.encoding:
        response.encoding = response.apparent_encoding
    return response.text

