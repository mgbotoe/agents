#!/usr/bin/env python3
"""SessionEnd hook: auto-commit + push daily-logs only.

Safety net for when a session closes without the agent running its
end-of-session discipline. ONLY touches `daily-logs/` — append-only
data that's safe to push without review.

Other tracked changes (identity/memory.md, memory/*.md, code, wiki)
are left alone. Those still require the agent's CLAUDE.md "Session
Discipline" flow (propose commits + ask Dina before push).

Always exits 0 — failure shouldn't block session end.
"""

import subprocess
import sys
from datetime import datetime, timezone


def run(cmd: list[str], timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def main() -> int:
    # Anything pending under daily-logs/?
    status = run(["git", "status", "--porcelain", "--", "daily-logs/"])
    if not status.stdout.strip():
        return 0  # silent — clean tree case

    add = run(["git", "add", "--", "daily-logs/"])
    if add.returncode != 0:
        print(f"[SESSION-END] git add failed: {add.stderr.strip()}")
        return 0

    # Confirm something was actually staged (path could be empty after add)
    cached = run(["git", "diff", "--cached", "--name-only", "--", "daily-logs/"])
    if not cached.stdout.strip():
        return 0

    msg = f"chore(daily-logs): session end {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
    commit = run(["git", "commit", "-m", msg, "--", "daily-logs/"])
    if commit.returncode != 0:
        print(f"[SESSION-END] commit failed: {commit.stderr.strip()}")
        return 0
    print(f"[SESSION-END] committed daily-logs: {msg}")

    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    push = run(["git", "push", "origin", branch])
    if push.returncode == 0:
        print(f"[SESSION-END] pushed to origin/{branch}")
    else:
        print(f"[SESSION-END] push failed — run manually: git push origin {branch}")
        print(f"  reason: {push.stderr.strip()[:200]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
