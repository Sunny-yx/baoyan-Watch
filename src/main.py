from __future__ import annotations

import argparse
import sys

from .config_loader import load_config
from .crawler import fetch_html
from .matcher import matches_keywords
from .notifier import send_email
from .parser import Notice, parse_notices
from .report import write_report
from .storage import filter_new_notices, load_seen, save_seen


def main() -> int:
    args = _parse_args()
    config = load_config(args.schools, args.keywords)
    seen_ids = load_seen(args.seen)

    matched_notices: list[Notice] = []
    for source in config.sources:
        if not source.enabled:
            continue
        try:
            html = fetch_html(source.url)
            notices = parse_notices(
                html=html,
                base_url=source.url,
                source_id=source.id,
                school=source.school,
                college=source.college,
                selectors=source.selectors,
            )
            matched_notices.extend(
                notice
                for notice in notices
                if matches_keywords(notice, source.keywords, source.match_mode)
            )
        except Exception as exc:
            print(f"Source failed: {source.id} {source.url} ({exc})", file=sys.stderr)

    new_notices = filter_new_notices(matched_notices, seen_ids)
    write_report(new_notices, args.report)

    if new_notices and not args.no_email:
        send_email(new_notices)

    save_seen(seen_ids, new_notices, args.seen)
    print(f"Matched notices: {len(matched_notices)}")
    print(f"New notices: {len(new_notices)}")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor baoyan-related school notices.")
    parser.add_argument("--schools", default="config/schools.yaml")
    parser.add_argument("--keywords", default="config/keywords.yaml")
    parser.add_argument("--seen", default="data/seen.json")
    parser.add_argument("--report", default="docs/latest.md")
    parser.add_argument("--no-email", action="store_true", help="Do not send email.")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())

