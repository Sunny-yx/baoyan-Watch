from __future__ import annotations

import json
from pathlib import Path

from .parser import Notice


def load_seen(path: Path | str = "data/seen.json") -> set[str]:
    seen_path = Path(path)
    if not seen_path.exists():
        return set()
    with seen_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return set(data.get("seen_ids", []))


def filter_new_notices(notices: list[Notice], seen_ids: set[str]) -> list[Notice]:
    return [notice for notice in notices if notice.fingerprint not in seen_ids]


def save_seen(seen_ids: set[str], notices: list[Notice], path: Path | str = "data/seen.json") -> None:
    seen_path = Path(path)
    seen_path.parent.mkdir(parents=True, exist_ok=True)
    updated_ids = sorted(seen_ids | {notice.fingerprint for notice in notices})
    with seen_path.open("w", encoding="utf-8") as file:
        json.dump({"seen_ids": updated_ids}, file, ensure_ascii=False, indent=2)
        file.write("\n")

