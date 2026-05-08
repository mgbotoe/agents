#!/usr/bin/env python3
"""Lightweight git sync check for SessionStart hook.

Reports two things:
  1. Remote sync state — behind/ahead/in sync.
  2. Local dirty state — uncommitted changes, split into:
     - daily-logs (auto-handled by SessionEnd hook on graceful exit)
     - other (memory/, identity/, code, wiki — requires the agent's
       Session Discipline flow to commit + push)

Always exits 0 — failure to check git is not a session-blocking issue.
"""

import subprocess
import sys


def run(cmd: list[str], timeout: int = 10) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def remote_sync_line() -> str:
    fetch = subprocess.run(
        ["git", "fetch", "-q", "origin"],
        capture_output=True, text=True, timeout=15
    )
    if fetch.returncode != 0:
        return "[GIT] remote check skipped (no remote or offline)"

    behind = run(["git", "rev-list", "--count", "HEAD..@{u}"]) or "0"
    ahead = run(["git", "rev-list", "--count", "@{u}..HEAD"]) or "0"

    if behind == "0" and ahead == "0":
        return "[GIT] remote: in sync"
    parts = []
    if behind != "0":
        parts.append(f"behind {behind}")
    if ahead != "0":
        parts.append(f"ahead {ahead}")
    hint = " - run `git pull --rebase`" if behind != "0" else " - push when ready"
    return f"[GIT] remote: {', '.join(parts)}{hint}"


def get_dirty_paths() -> list[str]:
    staged = run(["git", "diff", "--cached", "--name-only"]).splitlines()
    unstaged = run(["git", "diff", "--name-only"]).splitlines()
    untracked = run(["git", "ls-files", "--others", "--exclude-standard"]).splitlines()
    seen = set()
    out = []
    for p in staged + unstaged + untracked:
        p = p.strip()
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def local_dirty_line() -> str:
    paths = get_dirty_paths()
    if not paths:
        return "[GIT] local: clean"

    daily_log_paths = [p for p in paths if p.startswith("daily-logs/") or "/daily-logs/" in p]
    other_paths = [p for p in paths if p not in daily_log_paths]

    parts = []
    if daily_log_paths:
        parts.append(f"{len(daily_log_paths)} daily-log change(s) (auto-pushed on session end)")
    if other_paths:
        sample = ", ".join(other_paths[:3])
        more = f" +{len(other_paths) - 3} more" if len(other_paths) > 3 else ""
        parts.append(f"{len(other_paths)} other uncommitted: {sample}{more} - review before ending session")

    return "[GIT] local: " + " | ".join(parts)


def main() -> int:
    print(remote_sync_line())
    print(local_dirty_line())
    return 0


if __name__ == "__main__":
    sys.exit(main())
