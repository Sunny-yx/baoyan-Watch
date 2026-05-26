from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class SourceConfig:
    id: str
    school: str
    college: str
    url: str
    enabled: bool = True
    match_mode: str = "any"
    keywords: list[str] = field(default_factory=list)
    selectors: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class AppConfig:
    sources: list[SourceConfig]
    global_keywords: list[str]
    global_match_mode: str = "any"


def load_config(
    schools_path: Path | str = "config/schools.yaml",
    keywords_path: Path | str = "config/keywords.yaml",
) -> AppConfig:
    schools_data = _load_yaml(Path(schools_path))
    keywords_data = _load_yaml(Path(keywords_path))

    global_keywords = _read_string_list(keywords_data.get("keywords", []), "keywords")
    global_match_mode = keywords_data.get("match_mode", "any")
    _validate_match_mode(global_match_mode, "config/keywords.yaml")

    raw_sources = schools_data.get("sources")
    if not isinstance(raw_sources, list) or not raw_sources:
        raise ValueError("config/schools.yaml must contain a non-empty 'sources' list.")

    sources = [
        _parse_source(raw_source, global_keywords, global_match_mode)
        for raw_source in raw_sources
    ]
    return AppConfig(
        sources=sources,
        global_keywords=global_keywords,
        global_match_mode=global_match_mode,
    )


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a mapping: {path}")
    return data


def _parse_source(
    raw_source: Any,
    global_keywords: list[str],
    global_match_mode: str,
) -> SourceConfig:
    if not isinstance(raw_source, dict):
        raise ValueError("Each source in config/schools.yaml must be a mapping.")

    required_fields = ["id", "school", "college", "url"]
    missing = [field_name for field_name in required_fields if not raw_source.get(field_name)]
    if missing:
        raise ValueError(f"Source is missing required fields: {', '.join(missing)}")

    keywords = raw_source.get("keywords", global_keywords)
    keywords = _read_string_list(keywords, f"source {raw_source['id']} keywords")

    match_mode = raw_source.get("match_mode", global_match_mode)
    _validate_match_mode(match_mode, f"source {raw_source['id']}")

    selectors = raw_source.get("selectors", {})
    if selectors is None:
        selectors = {}
    if not isinstance(selectors, dict):
        raise ValueError(f"source {raw_source['id']} selectors must be a mapping.")

    return SourceConfig(
        id=str(raw_source["id"]),
        school=str(raw_source["school"]),
        college=str(raw_source["college"]),
        url=str(raw_source["url"]),
        enabled=bool(raw_source.get("enabled", True)),
        match_mode=str(match_mode),
        keywords=keywords,
        selectors={str(key): str(value) for key, value in selectors.items()},
    )


def _read_string_list(value: Any, name: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a non-empty list.")
    result = [str(item).strip() for item in value if str(item).strip()]
    if not result:
        raise ValueError(f"{name} must contain at least one non-empty string.")
    return result


def _validate_match_mode(value: str, owner: str) -> None:
    if value not in {"any", "all"}:
        raise ValueError(f"{owner} match_mode must be either 'any' or 'all'.")

