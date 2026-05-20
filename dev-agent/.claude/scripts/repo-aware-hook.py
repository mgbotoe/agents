#!/usr/bin/env python3
"""PreToolUse hook — block Edit/Write on substantive docs without prior repo-aware scan.

Fires on Edit / Write / MultiEdit. If the target file matches a "claim-bearing"
pattern (roadmap, ADR, pending-review, design doc, conventions), checks that
.claude/state/repo-aware-cache.json has a fresh entry (<30 min) for the file's
repo. If not, blocks with a message telling the agent to invoke
.claude/scripts/repo-aware.py against the repo first.

Block mechanism: exit code 2 with reason on stderr (Claude Code convention).
Non-substantive edits (CLAUDE.md trivia, .gitkeep, source code) pass through.

Sub-agent recursion: same suppression as delegation-scope-hook.py.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

DEV_AGENT_ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_PATH = DEV_AGENT_ROOT / ".claude" / "state" / "repo-aware-cache.json"
FRESH_SECONDS = 30 * 60

# Patterns where edit-without-scan is the failure mode we're guarding against
TRIGGER_PATTERNS = [
    r"roadmap.*\.md$",
    r"pending-.*\.md$",
    r"design-doc.*\.md$",
    r"decisions/[^/]+\.md$",
    r"docs/adr/[^/]+\.md$",
    r"docs/repos\.md$",
    r"docs/conventions/.*\.md$",
]


def in_subagent() -> bool:
    for var in ("CLAUDE_AGENT_NAME", "CLAUDE_SUBAGENT", "CLAUDE_SUBAGENT_TYPE"):
        if os.environ.get(var):
            return True
    return False


def find_repo_root(file_path: Path) -> Path | None:
    """Walk up from file_path looking for a .git directory."""
    try:
        current = file_path.parent.resolve()
    except Exception:
        return None
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def is_trigger(file_path: Path) -> bool:
    posix = file_path.as_posix()
    return any(re.search(p, posix, re.IGNORECASE) for p in TRIGGER_PATTERNS)


def cache_fresh_for(repo: Path) -> bool:
    if not CACHE_PATH.exists():
        return False
    try:
        cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return False
    entry = cache.get(str(repo))
    if not entry:
        return False
    return (time.time() - entry.get("scanned_at", 0)) < FRESH_SECONDS


def main() -> int:
    if in_subagent():
        return 0

    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # malformed input — don't block

    tool_input = payload.get("tool_input") or {}
    raw_path = tool_input.get("file_path") or ""
    if not raw_path:
        return 0

    try:
        file_path = Path(raw_path).expanduser().resolve()
    except Exception:
        return 0

    if not is_trigger(file_path):
        return 0

    repo = find_repo_root(file_path)
    if repo is None:
        # Not inside a git repo — nothing to scan against, allow
        return 0

    # Don't gate edits inside dev-agent itself — that's self-modification, separate concern
    if str(repo) == str(DEV_AGENT_ROOT):
        return 0

    if cache_fresh_for(repo):
        return 0

    msg = (
        f"\n[repo-aware] Edit blocked: {file_path.name} is a claim-bearing document "
        f"in {repo.name}.\n"
        f"You haven't run a repo-aware scan against this repo in the last 30 minutes.\n\n"
        f"Run this first, then retry the edit:\n"
        f"  python .claude/scripts/repo-aware.py \"{repo}\"\n\n"
        f"Rationale: editing roadmap/ADR/conventions/pending-review docs without "
        f"verifying current repo state is the drift failure mode in "
        f"feedback_verify_plan_against_code.md.\n"
    )
    print(msg, file=sys.stderr)
    return 2  # exit 2 = block, stderr shown to agent


if __name__ == "__main__":
    sys.exit(main())
