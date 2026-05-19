#!/usr/bin/env python3
"""PostToolUse hook — appends a one-liner to today's daily log when HEAD advances.

Mechanism: compare current HEAD against last-seen HEAD stored in
.claude/state/last-commit.txt. If different, append:

    - HH:MM UTC `abc1234` <subject> [+lines/-lines, N files]

to daily-logs/YYYY-MM-DD.md under a "## Commits" section (created if absent).

Robust to commit method (Bash, terminal, GUI) — always reflects HEAD state.
Only tracks the dev-agent repo for v1. Cross-repo logging deferred.

Always exits 0. Hook failures must never block tool calls.
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = REPO_ROOT / ".claude" / "state" / "last-commit.txt"
LOG_DIR = REPO_ROOT / "daily-logs"


def run(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True,
                           timeout=5, encoding="utf-8", errors="replace")
        return r.stdout.strip()
    except Exception:
        return ""


def get_head() -> str:
    return run(["git", "rev-parse", "HEAD"])


def get_commit_info(sha: str) -> dict:
    pretty = run(["git", "log", "-1", "--pretty=format:%h|%s|%aI", sha])
    if not pretty or "|" not in pretty:
        return {}
    short, subject, iso = pretty.split("|", 2)
    stats = run(["git", "diff-tree", "--no-commit-id", "--numstat", sha])
    files = adds = dels = 0
    for line in stats.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            files += 1
            try:
                adds += int(parts[0])
                dels += int(parts[1])
            except ValueError:
                pass
    return {"short": short, "subject": subject, "iso": iso,
            "files": files, "adds": adds, "dels": dels}


def append_entry(info: dict) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hhmm = datetime.now(timezone.utc).strftime("%H:%M")
    log_path = LOG_DIR / f"{today}.md"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    line = (f"- {hhmm} UTC `{info['short']}` {info['subject']} "
            f"[+{info['adds']}/-{info['dels']}, {info['files']} files]")

    if not log_path.exists():
        log_path.write_text(f"# {today}\n\n## Commits\n{line}\n", encoding="utf-8")
        return

    text = log_path.read_text(encoding="utf-8")
    if "## Commits" in text:
        # append after the Commits header block — find the section and add line at its tail
        lines = text.splitlines()
        out = []
        inserted = False
        i = 0
        while i < len(lines):
            out.append(lines[i])
            if not inserted and lines[i].strip() == "## Commits":
                # find end of this section (next ## or EOF)
                j = i + 1
                while j < len(lines) and not lines[j].startswith("## "):
                    out.append(lines[j])
                    j += 1
                out.append(line)
                inserted = True
                i = j
                continue
            i += 1
        if not inserted:
            out.append("")
            out.append("## Commits")
            out.append(line)
        log_path.write_text("\n".join(out) + ("\n" if not text.endswith("\n") else ""),
                            encoding="utf-8")
    else:
        suffix = "" if text.endswith("\n") else "\n"
        log_path.write_text(text + suffix + "\n## Commits\n" + line + "\n", encoding="utf-8")


def main() -> int:
    head = get_head()
    if not head:
        return 0

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    last = STATE_FILE.read_text(encoding="utf-8").strip() if STATE_FILE.exists() else ""

    if head == last:
        return 0

    # First run: just record HEAD, don't backfill
    if not last:
        STATE_FILE.write_text(head, encoding="utf-8")
        return 0

    info = get_commit_info(head)
    if info:
        append_entry(info)
    STATE_FILE.write_text(head, encoding="utf-8")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[log-commit] error: {e}\n")
        sys.exit(0)
