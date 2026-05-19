#!/usr/bin/env python3
"""Scan daily-logs for sessions where work should have been delegated but wasn't.

Two modes:
  - default: print rolling 7-day summary (used by SessionStart hook)
  - --range N: print last N days
  - --since YYYY-MM-DD: print since date
  - --json: machine-readable output

A "miss" is a session that shows substantial external-repo work
(multi-file PRs, big diffs, cross-repo work) with zero sub-agent
mentions. Heuristic, not authoritative — surfaces candidates for review.

Always exits 0. SessionStart hook must never block.
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "daily-logs")
LOG_DIR = os.path.abspath(LOG_DIR)

EXT_REPO_TOKENS = [
    "WDAI", "wdai", "Women Defining AI", "mailchimp-cc", "media-theater",
    "CineVault", "portfolio", "tax-engine", "Personal Projects",
    "Webdesign Business", "SAMESF", "open-design", "PR #",
]
SUBAGENT_TOKENS = [
    "Builder", "Designer", " QA ", "DevOps", "Security sub-agent",
    "delegate", "delegated", "spawned", "Agent(", "subagent_type",
]
PR_RE = re.compile(r"PR\s*#(\d+)")
FILES_RE = re.compile(r"(\d+)\s+files?", re.IGNORECASE)
LINES_RE = re.compile(r"(\d+)\s+lines?|\+(\d+)/-(\d+)", re.IGNORECASE)


def parse_log(path):
    try:
        text = open(path, encoding="utf-8").read()
    except Exception:
        return None
    name = os.path.basename(path).replace(".md", "")
    if not re.match(r"\d{4}-\d{2}-\d{2}$", name):
        return None
    ext = sum(text.lower().count(t.lower()) for t in EXT_REPO_TOKENS)
    sub = sum(text.count(t) for t in SUBAGENT_TOKENS)
    prs = sorted(set(PR_RE.findall(text)))
    file_counts = [int(m) for m in FILES_RE.findall(text)]
    file_counts = [c for c in file_counts if 0 < c < 100]
    return {
        "date": name,
        "log_lines": len(text.splitlines()),
        "ext_repo_signal": ext,
        "subagent_mentions": sub,
        "prs": prs,
        "max_files": max(file_counts) if file_counts else 0,
    }


def is_miss(s):
    if s["log_lines"] < 15:
        return False
    if s["subagent_mentions"] >= 2:
        return False
    if s["max_files"] >= 5:
        return True
    if s["ext_repo_signal"] >= 10 and s["subagent_mentions"] == 0:
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", type=int, default=7, help="last N days")
    ap.add_argument("--since", help="YYYY-MM-DD")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.since:
        since = datetime.strptime(args.since, "%Y-%m-%d").date()
    else:
        since = date.today() - timedelta(days=args.range)

    sessions = []
    for path in sorted(glob.glob(os.path.join(LOG_DIR, "*.md"))):
        s = parse_log(path)
        if not s:
            continue
        try:
            d = datetime.strptime(s["date"], "%Y-%m-%d").date()
        except ValueError:
            continue
        if d < since:
            continue
        sessions.append(s)

    misses = [s for s in sessions if is_miss(s)]

    if args.json:
        print(json.dumps({"sessions": sessions, "misses": misses}, indent=2))
        return 0

    if not sessions:
        return 0

    if not misses:
        print(f"[delegation-scan] {len(sessions)} sessions since {since}, no clear misses. Keep watching.")
        return 0

    print(f"[delegation-scan] {len(misses)} possible missed delegations in last {args.range}d ({len(sessions)} sessions reviewed):")
    for m in misses[-5:]:
        pr_note = f" PRs: #{', #'.join(m['prs'])}" if m["prs"] else ""
        files_note = f" {m['max_files']}f" if m["max_files"] else ""
        print(f"  - {m['date']}:{files_note}{pr_note}  (subagent_mentions={m['subagent_mentions']})")
    print("[delegation-scan] Triggers reminder: >4 files in external repo = Builder territory. Auth/payments/PII = Security.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[delegation-scan] skipped: {e}", file=sys.stderr)
        sys.exit(0)
