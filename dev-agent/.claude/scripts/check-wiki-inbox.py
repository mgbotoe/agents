"""Check wiki/sources/ for new technical items not yet reviewed by Polaris.

Looks for files with `routing: technical` in frontmatter that haven't been
marked as reviewed. Outputs a summary for the SessionStart hook.
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path

WIKI_SOURCES = Path("C:/Workspace/agents/wiki/sources")
REVIEWED_FILE = Path("C:/Workspace/agents/dev-agent/.claude/reviewed-sources.txt")

def load_reviewed():
    if not REVIEWED_FILE.exists():
        return set()
    return set(REVIEWED_FILE.read_text().strip().splitlines())

def save_reviewed(reviewed):
    REVIEWED_FILE.write_text("\n".join(sorted(reviewed)) + "\n")

def parse_frontmatter(text):
    match = re.match(r"^---\n(.+?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip().strip('"')
    return fm

def safe_print(text):
    """Print with fallback for Windows encoding issues."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))

def main():
    if not WIKI_SOURCES.exists():
        return

    reviewed = load_reviewed()
    new_items = []

    # Only check sources from the last 7 days
    cutoff = datetime.now() - timedelta(days=7)

    for f in sorted(WIKI_SOURCES.glob("*.md")):
        if f.name in reviewed:
            continue

        # Quick date filter from filename (YYYY-MM-DD-slug.md)
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
        if date_match:
            file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
            if file_date < cutoff:
                continue

        text = f.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)

        if fm.get("routing") == "technical":
            new_items.append({
                "file": f.name,
                "title": fm.get("title", f.stem),
                "date": fm.get("date", "unknown"),
                "granola_id": fm.get("granola_id", ""),
            })

    if not new_items:
        return

    safe_print("[WIKI INBOX] New technical items from Atlas:")
    for item in new_items:
        granola_hint = f" | Granola: {item['granola_id']}" if item["granola_id"] else ""
        safe_print(f"  - [{item['date']}] {item['title']}")
        safe_print(f"    wiki/sources/{item['file']}{granola_hint}")
    safe_print(f"  -> {len(new_items)} item(s) awaiting your technical review.")
    safe_print("  -> After reviewing, call: python3 .claude/scripts/check-wiki-inbox.py --mark <filename>")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "--mark":
        reviewed = load_reviewed()
        for fname in sys.argv[2:]:
            reviewed.add(fname)
        save_reviewed(reviewed)
        print(f"Marked {len(sys.argv) - 2} source(s) as reviewed.")
    else:
        main()
