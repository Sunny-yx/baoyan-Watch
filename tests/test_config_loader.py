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


def test_source_without_keywords_uses_global_keywords(tmp_path: Path) -> None:
    schools = tmp_path / "schools.yaml"
    keywords = tmp_path / "keywords.yaml"
    schools.write_text(
        """
sources:
  - id: sustech-aim
    school: 南方科技大学
    college: 自动化与智能制造学院
    url: https://aim.sustech.edu.cn/
    enabled: true
    match_mode: all
    keywords:
      - 全国优秀大学生
      - 暑期
      - 营
  - id: zju-aim
    school: 浙江大学
    college: 管理学院
    url: http://www.som.zju.edu.cn/main.htm
    enabled: true
    match_mode: any
""",
        encoding="utf-8",
    )
    keywords.write_text(
        "match_mode: any\nkeywords:\n  - 夏令营\n  - 推荐免试\n",
        encoding="utf-8",
    )

    config = load_config(schools, keywords)

    assert config.sources[1].id == "zju-aim"
    assert config.sources[1].match_mode == "any"
    assert config.sources[1].keywords == ["夏令营", "推荐免试"]


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
