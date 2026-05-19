#!/usr/bin/env python3
"""SessionEnd + PreCompact hook — appends activity snapshot to daily log.

Pure local-state aggregation. No LLM call, no API spend. Captures what's
factually available so /promote (cloud cron, has LLM) can mine the
signal:

  - External-repo files touched this session
  - Delegation warnings fired
  - Trigger source (SessionEnd vs PreCompact)
  - Session duration if first-seen time is known

Format appended to daily-logs/YYYY-MM-DD.md:

  ## Snapshot HH:MM UTC (SessionEnd)
  - 5 external files: foo.tsx, bar.ts, baz.py
  - Delegation: soft-warn fired at 4 files
  - Session duration: ~1.5h

Idempotent: each snapshot is timestamped + trigger-tagged, so multiple
fires (e.g., PreCompact mid-session followed by SessionEnd later) each
get their own entry.

Always exits 0. Hook failure must never block session lifecycle.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "state"
SESSION_EDITS = STATE_DIR / "session-edits.json"
SNAPSHOT_STATE = STATE_DIR / "last-snapshot.json"
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "daily-logs"

# Hook event name comes through env or argv. SessionEnd vs PreCompact.
EVENT_HINT = os.environ.get("CLAUDE_HOOK_EVENT") or (sys.argv[1] if len(sys.argv) > 1 else "unknown")


def read_payload() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def load_session_edits() -> dict:
    if not SESSION_EDITS.exists():
        return {}
    try:
        return json.loads(SESSION_EDITS.read_text(encoding="utf-8"))
    except Exception:
        return {}


def load_snapshot_state() -> dict:
    if not SNAPSHOT_STATE.exists():
        return {}
    try:
        return json.loads(SNAPSHOT_STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_snapshot_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def humanize_duration(seconds: float) -> str:
    if seconds < 300:
        return f"~{int(seconds/60)}m"
    if seconds < 3600:
        return f"~{int(seconds/60)}m"
    return f"~{seconds/3600:.1f}h"


def build_snapshot(session_id: str, trigger: str) -> str | None:
    """Return markdown block, or None if nothing worth logging."""
    edits = load_session_edits().get(session_id, {})
    files = edits.get("files", [])
    warned_soft = edits.get("warned_soft", False)
    warned_hard = edits.get("warned_hard", False)
    snapshot_state = load_snapshot_state()
    first_seen = snapshot_state.get("first_seen", {}).get(session_id)

    # Skip if literally nothing happened this session
    if not files and not warned_soft and not warned_hard:
        return None

    now = time.time()
    hhmm = datetime.now(timezone.utc).strftime("%H:%M")
    lines = [f"## Snapshot {hhmm} UTC ({trigger})"]

    if files:
        # Trim to relative names for readability
        names = []
        for f in files:
            try:
                p = Path(f)
                names.append(p.name)
            except Exception:
                names.append(str(f))
        n = len(names)
        sample = ", ".join(names[:6])
        more = f" (+{n - 6} more)" if n > 6 else ""
        lines.append(f"- {n} external file{'s' if n != 1 else ''} touched: {sample}{more}")

    if warned_hard:
        lines.append(f"- Delegation: HARD warning fired (8+ files; clear Builder territory)")
    elif warned_soft:
        lines.append(f"- Delegation: soft-warn fired (4+ external files)")

    if first_seen:
        dur = now - first_seen
        if dur > 60:
            lines.append(f"- Session duration: {humanize_duration(dur)}")

    return "\n".join(lines) + "\n"


def append_to_daily_log(block: str) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_path = LOG_DIR / f"{today}.md"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not log_path.exists():
        log_path.write_text(f"# {today}\n\n{block}\n", encoding="utf-8")
        return

    text = log_path.read_text(encoding="utf-8")
    suffix = "" if text.endswith("\n") else "\n"
    if not text.endswith("\n\n"):
        suffix += "\n"
    log_path.write_text(text + suffix + block + "\n", encoding="utf-8")


def main() -> int:
    payload = read_payload()
    session_id = payload.get("session_id") or "unknown"
    trigger = "SessionEnd" if "end" in EVENT_HINT.lower() else (
        "PreCompact" if "compact" in EVENT_HINT.lower() else EVENT_HINT
    )

    # Record first-seen time for this session if not yet known
    snapshot_state = load_snapshot_state()
    first_seen = snapshot_state.setdefault("first_seen", {})
    if session_id not in first_seen:
        first_seen[session_id] = time.time()
        save_snapshot_state(snapshot_state)

    block = build_snapshot(session_id, trigger)
    if block:
        append_to_daily_log(block)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[session-snapshot] error: {e}\n")
        sys.exit(0)
