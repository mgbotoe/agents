#!/usr/bin/env python3
"""PreToolUse hook — soft warning when scope crosses Builder-delegation threshold.

Fires on Edit / Write / MultiEdit. Counts distinct files touched in
external repos (outside dev-agent/) per session. Warns to stderr at
thresholds. Never blocks — exits 0 always.

State: .claude/state/session-edits.json keyed by session_id from stdin.
Stale entries (>48h) are pruned on each run.

Thresholds (soft, tunable):
  4 distinct external files -> first warning ("Builder territory")
  8 distinct external files -> second warning ("Hard delegation candidate")

Sub-agent recursion: if env CLAUDE_AGENT_NAME or CLAUDE_SUBAGENT is set
(non-empty), suppress entirely — the sub-agent is already doing the work.
This is best-effort; if Claude Code names the env differently, the hook
just behaves as if we're in main session, which is the safe default.
"""

import json
import os
import sys
import time
from pathlib import Path

STATE_PATH = Path(__file__).resolve().parent.parent / "state" / "session-edits.json"
SELF_ROOT = Path(__file__).resolve().parent.parent.parent  # dev-agent/
WARN_THRESHOLD = 4
HARD_THRESHOLD = 8
STALE_SECONDS = 48 * 3600


def in_subagent() -> bool:
    for var in ("CLAUDE_AGENT_NAME", "CLAUDE_SUBAGENT", "CLAUDE_SUBAGENT_TYPE"):
        if os.environ.get(var):
            return True
    return False


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def prune_stale(state: dict) -> dict:
    now = time.time()
    return {k: v for k, v in state.items() if now - v.get("last_seen", 0) < STALE_SECONDS}


def is_external(file_path: str) -> bool:
    if not file_path:
        return False
    try:
        p = Path(file_path).resolve()
    except Exception:
        return False
    try:
        p.relative_to(SELF_ROOT)
        return False  # inside dev-agent/
    except ValueError:
        return True


def main() -> int:
    if in_subagent():
        return 0

    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool = payload.get("tool_name") or ""
    if tool not in ("Edit", "Write", "MultiEdit"):
        return 0

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not is_external(file_path):
        return 0

    session_id = payload.get("session_id") or "unknown"

    state = prune_stale(load_state())
    entry = state.get(session_id) or {"files": [], "warned_soft": False, "warned_hard": False}
    if file_path not in entry["files"]:
        entry["files"].append(file_path)
    entry["last_seen"] = time.time()
    state[session_id] = entry
    save_state(state)

    count = len(entry["files"])

    if count >= HARD_THRESHOLD and not entry["warned_hard"]:
        entry["warned_hard"] = True
        save_state(state)
        sys.stderr.write(
            f"\n[delegation-scope] {count} distinct external files touched this session.\n"
            f"  This is clear Builder territory. Spawn Builder via Agent(subagent_type=builder)\n"
            f"  with a delegation packet — don't keep grinding solo.\n"
            f"  Override: ignore this message (it's logged, surfaces at next SessionStart).\n\n"
        )
        return 0

    if count >= WARN_THRESHOLD and not entry["warned_soft"]:
        entry["warned_soft"] = True
        save_state(state)
        sys.stderr.write(
            f"\n[delegation-scope] {count} distinct external files touched. "
            f"Consider delegating to Builder before continuing.\n\n"
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[delegation-scope] error: {e}\n")
        sys.exit(0)
