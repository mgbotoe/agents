#!/usr/bin/env python3
"""Lightweight git sync check for SessionStart hook.

Prints one line: either "[GIT] in sync" or "[GIT] behind N, ahead M — run git pull --rebase".
Always exits 0 — failure to check git is not a session-blocking issue.
"""

import subprocess
import sys


def run(cmd: list[str], timeout: int = 10) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def main() -> int:
    fetch = subprocess.run(
        ["git", "fetch", "-q", "origin"],
        capture_output=True, text=True, timeout=15
    )
    if fetch.returncode != 0:
        print("[GIT] sync check skipped (no remote or offline)")
        return 0

    behind = run(["git", "rev-list", "--count", "HEAD..@{u}"]) or "0"
    ahead = run(["git", "rev-list", "--count", "@{u}..HEAD"]) or "0"

    if behind == "0" and ahead == "0":
        print("[GIT] in sync")
    else:
        msg = []
        if behind != "0":
            msg.append(f"behind {behind}")
        if ahead != "0":
            msg.append(f"ahead {ahead}")
        hint = " — run `git pull --rebase`" if behind != "0" else " — push when ready"
        print(f"[GIT] {', '.join(msg)}{hint}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
