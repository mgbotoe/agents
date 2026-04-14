#!/usr/bin/env python3
"""
Search daily logs using SQLite FTS5.
Usage: python3 .claude/scripts/search-logs.py <query> [--date YYYY-MM-DD] [--limit N]
"""

import sqlite3
import sys
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
DB_PATH = PROJECT_DIR / ".claude" / "memory.db"


def search(query: str, date_filter: str | None = None, limit: int = 10):
    if not DB_PATH.exists():
        print("No search index found. Run: python3 .claude/scripts/index-daily-logs.py")
        return

    conn = sqlite3.connect(str(DB_PATH))

    sql = "SELECT date, time_block, source_file, snippet(log_entries, 2, '>>>', '<<<', '...', 64) as snippet FROM log_entries WHERE log_entries MATCH ?"
    params: list[str | int] = [query]

    if date_filter:
        sql += " AND date = ?"
        params.append(date_filter)

    sql += " ORDER BY rank LIMIT ?"
    params.append(limit)

    results = conn.execute(sql, params).fetchall()

    if not results:
        print(f"No results for: {query}")
        return

    print(f"Found {len(results)} result(s) for: {query}\n")
    for date, time_block, source, snippet in results:
        print(f"[{date}] {time_block}")
        print(f"  Source: {source}")
        print(f"  {snippet}")
        print()

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Search daily logs")
    parser.add_argument("query", nargs="+", help="Search query (FTS5 syntax)")
    parser.add_argument("--date", help="Filter by date (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    args = parser.parse_args()

    query = " ".join(args.query)
    search(query, args.date, args.limit)


if __name__ == "__main__":
    main()
