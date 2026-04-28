#!/usr/bin/env python3
"""Decay old daily logs into monthly archives.

Daily logs (`daily-logs/YYYY-MM-DD.md`) older than DECAY_DAYS get appended
to `memory/archive-YYYY-MM.md` (one archive per calendar month) and the
originals are deleted.

Non-dated files in `daily-logs/` (e.g. `research-*.md`) are left alone.
Identity memory and cold `memory/*.md` files are NOT touched here —
those are hand-curated by `/promote`.

Run weekly via Windows Task Scheduler. Idempotent.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR = ROOT / "daily-logs"
ARCHIVE_DIR = ROOT / "memory"
DECAY_DAYS = 180

DATED = re.compile(r"^(\d{4})-(\d{2})-(\d{2})\.md$")


def main() -> int:
    if not LOGS_DIR.is_dir():
        print(f"No daily-logs dir at {LOGS_DIR}. Nothing to decay.")
        return 0

    cutoff = date.today() - timedelta(days=DECAY_DAYS)
    by_month: dict[str, list[tuple[date, Path]]] = {}

    for log in sorted(LOGS_DIR.glob("*.md")):
        m = DATED.match(log.name)
        if not m:
            continue
        y, mo, d = (int(p) for p in m.groups())
        log_date = date(y, mo, d)
        if log_date >= cutoff:
            continue
        by_month.setdefault(f"{y:04d}-{mo:02d}", []).append((log_date, log))

    if not by_month:
        print(f"No logs older than {DECAY_DAYS} days. Nothing to decay.")
        return 0

    moved = 0
    for key, entries in sorted(by_month.items()):
        archive = ARCHIVE_DIR / f"archive-{key}.md"
        with archive.open("a", encoding="utf-8") as out:
            for log_date, log in sorted(entries):
                out.write(f"\n\n## {log_date.isoformat()}\n\n")
                out.write(log.read_text(encoding="utf-8"))
        print(f"Archived {len(entries)} log(s) -> {archive.name}")
        for _, log in entries:
            log.unlink()
            moved += 1

    print(f"Decay complete: {moved} log(s) moved to monthly archives.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
