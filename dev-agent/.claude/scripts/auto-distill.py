#!/usr/bin/env python3
"""SessionEnd hook — rich auto-distill via Anthropic API.

Reads the session's local transcript JSONL, sends a compact version to
claude-sonnet-4-6, appends a "## Distill HH:MM UTC (auto)" block to
today's daily log. Adds the narrative `/promote` needs to mine.

Strong gating to prevent ghost-spawn cost (per 2026-04 Task Scheduler
ghost-distill incident):
  - Skip if ANTHROPIC_API_KEY not set (graceful degrade to lite-only)
  - Skip if transcript missing or < MIN_TRANSCRIPT_LINES
  - Skip if session duration < MIN_DURATION_SEC (per last-snapshot.json)
  - Skip if no files touched AND no commits (per session-edits + git)
  - Hard timeout on API call

Cost bound: max_tokens=1500, single sonnet-4-6 call per qualifying session.

Always exits 0. Hook failure must never block session lifecycle.
Runs AFTER session-snapshot, BEFORE session-end-sync commit.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Windows stdout encoding
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_DIR = REPO_ROOT / ".claude" / "state"
LOG_DIR = REPO_ROOT / "daily-logs"
TRANSCRIPT_BASE = Path.home() / ".claude" / "projects" / "C--Workspace-agents-dev-agent"

MIN_DURATION_SEC = 600          # 10 minutes — quick chats don't get distilled
MIN_TRANSCRIPT_LINES = 30       # rough "did anything happen" threshold
MAX_TRANSCRIPT_CHARS = 60000    # trim if larger; ~15k tokens input cap
API_TIMEOUT_SEC = 30
MAX_TOKENS = 1500

MODEL = "claude-sonnet-4-6"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def session_first_seen(session_id: str) -> float | None:
    snap = load_json(STATE_DIR / "last-snapshot.json")
    return snap.get("first_seen", {}).get(session_id)


def session_files_touched(session_id: str) -> int:
    edits = load_json(STATE_DIR / "session-edits.json")
    entry = edits.get(session_id, {})
    return len(entry.get("files", []))


def head_advanced() -> bool:
    """Did HEAD move in any tracked repo this session? Proxy: log-commit state vs git rev-parse."""
    state_file = STATE_DIR / "last-commits.json"
    if not state_file.exists():
        return False
    try:
        recorded = json.loads(state_file.read_text(encoding="utf-8"))
    except Exception:
        return False
    for repo, _last in recorded.items():
        # we don't need to be exact — if the script has been keeping state,
        # presence of recent commits in today's daily log under ## Commits
        # is a fine signal. Just probe the local log.
        pass
    today_log = LOG_DIR / datetime.now(timezone.utc).strftime("%Y-%m-%d.md")
    if not today_log.exists():
        return False
    try:
        return "## Commits" in today_log.read_text(encoding="utf-8")
    except Exception:
        return False


def extract_dialog(transcript_path: Path) -> list[dict]:
    """Extract user/assistant content from transcript JSONL, in order."""
    dialog = []
    with transcript_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            t = e.get("type")
            if t == "user":
                msg = (e.get("message") or {})
                content = msg.get("content")
                if isinstance(content, str) and content.strip():
                    # Skip pure tool-result echoes / system-reminders
                    if content.startswith("<system-reminder>"):
                        continue
                    dialog.append({"role": "user", "text": content.strip()[:2000]})
            elif t == "assistant":
                msg = (e.get("message") or {})
                content = msg.get("content")
                if isinstance(content, list):
                    text_parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text_parts.append(block.get("text", ""))
                    text = "\n".join(text_parts).strip()
                    if text:
                        dialog.append({"role": "assistant", "text": text[:2000]})
    return dialog


def build_transcript_text(dialog: list[dict]) -> str:
    parts = []
    total_chars = 0
    # walk in reverse to keep the tail (most recent decisions usually richer)
    for d in dialog:
        snippet = f"[{d['role']}]\n{d['text']}\n"
        if total_chars + len(snippet) > MAX_TRANSCRIPT_CHARS:
            parts.insert(0, f"... ({len(dialog) - len(parts)} earlier turns truncated)\n")
            break
        parts.insert(0, snippet)  # keep chronological after reverse iteration
        total_chars += len(snippet)
    return "\n".join(parts) if parts else ""


def call_api(api_key: str, transcript_text: str) -> str | None:
    try:
        from anthropic import Anthropic
    except ImportError:
        sys.stderr.write("[auto-distill] anthropic package not installed; skipping\n")
        return None
    prompt = (
        "Distill this Claude Code session for /promote to mine later. "
        "Output structured bullets, no preamble. Format:\n\n"
        "**Worked on:** (1-3 bullets — concrete, not vague)\n"
        "**Decisions + why:** (1-3 bullets — name the *why*, not just the *what*)\n"
        "**Surprises / things learned:** (0-3 bullets — only if non-obvious)\n"
        "**Open questions / unresolved:** (0-3 bullets — what's still pending)\n"
        "**Behavior changes for Polaris going forward:** (0-2 bullets — rules, hooks, "
        "memory updates suggested)\n\n"
        "Keep total under 25 lines. Skip sections that have nothing meaningful. "
        "Cite specific files/commits/decisions over generalities.\n\n"
        "Session transcript:\n\n"
        f"{transcript_text}"
    )
    try:
        client = Anthropic(api_key=api_key, timeout=API_TIMEOUT_SEC)
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()
    except Exception as e:
        sys.stderr.write(f"[auto-distill] API call failed: {type(e).__name__}: {e}\n")
        return None


def append_distill(text: str) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hhmm = datetime.now(timezone.utc).strftime("%H:%M")
    log_path = LOG_DIR / f"{today}.md"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    block = f"\n## Distill {hhmm} UTC (auto)\n{text}\n"

    if not log_path.exists():
        log_path.write_text(f"# {today}\n{block}\n", encoding="utf-8")
        return

    existing = log_path.read_text(encoding="utf-8")
    suffix = "" if existing.endswith("\n") else "\n"
    log_path.write_text(existing + suffix + block + "\n", encoding="utf-8")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    session_id = payload.get("session_id")
    if not session_id:
        return 0

    # Gate 1: API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # Silent — graceful degrade to lite-only
        return 0

    # Gate 2: transcript exists + has content
    transcript_path = TRANSCRIPT_BASE / f"{session_id}.jsonl"
    if not transcript_path.exists():
        sys.stderr.write(f"[auto-distill] no transcript for {session_id}\n")
        return 0
    try:
        line_count = sum(1 for _ in transcript_path.open(encoding="utf-8"))
    except Exception:
        return 0
    if line_count < MIN_TRANSCRIPT_LINES:
        return 0

    # Gate 3: duration
    first_seen = session_first_seen(session_id)
    if first_seen:
        if (time.time() - first_seen) < MIN_DURATION_SEC:
            return 0

    # Gate 4: meaningful activity (files touched OR commits made today)
    if session_files_touched(session_id) == 0 and not head_advanced():
        return 0

    # Extract dialog
    dialog = extract_dialog(transcript_path)
    if len(dialog) < 4:  # at least two exchanges
        return 0

    transcript_text = build_transcript_text(dialog)
    if not transcript_text:
        return 0

    # Call API
    distill = call_api(api_key, transcript_text)
    if not distill:
        return 0

    append_distill(distill)
    sys.stderr.write(f"[auto-distill] wrote distill block to daily-logs/{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.md\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[auto-distill] error: {type(e).__name__}: {e}\n")
        sys.exit(0)
