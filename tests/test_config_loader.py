from pathlib import Path

import pytest

from src.config_loader import load_config


def test_load_config_reads_sustech_sample() -> None:
    config = load_config()

    source = config.sources[0]
    assert source.id == "sustech-aim"
    assert source.school == "南方科技大学"
    assert source.college == "自动化与智能制造学院"
    assert source.url == "https://aim.sustech.edu.cn/"
    assert source.match_mode == "all"
    assert source.keywords == ["全国优秀大学生", "暑期", "营"]


def test_load_config_rejects_missing_required_field(tmp_path: Path) -> None:
    schools = tmp_path / "schools.yaml"
    keywords = tmp_path / "keywords.yaml"
    schools.write_text(
        "sources:\n  - id: bad\n    school: 南方科技大学\n    url: https://example.com\n",
        encoding="utf-8",
    )
    keywords.write_text("keywords:\n  - 推免\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required fields"):
        load_config(schools, keywords)

