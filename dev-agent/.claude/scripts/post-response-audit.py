#!/usr/bin/env python3
"""Stop hook — post-response shallow-output audit.

Fires after every assistant turn. Reads the last assistant message from
the transcript. If the response contains mermaid blocks or claim-bearing
content about WDAI repos, cross-references the inventory-repo invocation
log. If any mentioned repo wasn't inventoried in the last 30 minutes,
emits a user-visible warning.

This is accountability, not prevention. The model can still produce
shallow output, but now violations are flagged to Dina — raising the
cost of skipping the discipline.

Per Claude Code Stop hook spec:
- stdin: JSON with session_id, transcript_path
- stdout: visible to user
- stderr: logged
- exit 0: continue normally; non-zero would block (we don't want that)
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

DEV_AGENT_ROOT = Path(__file__).resolve().parent.parent.parent
INVOCATION_STATE = DEV_AGENT_ROOT / ".claude" / "state" / "inventory-invocations.json"

# Repos in WDAI ecosystem the audit applies to
WDAI_REPOS = [
    "wdai-foundation-platform",
    "wdai-admin",
    "wdai-marketing",
    "wdai-lumabot",
    "wdai-team-os",
    "mailchimp-cc",
    "claude-code-skills",
    "perplex_computer",
]

FRESH_SECONDS = 30 * 60  # 30-minute window matches repo-aware


def in_subagent() -> bool:
    for var in ("CLAUDE_AGENT_NAME", "CLAUDE_SUBAGENT", "CLAUDE_SUBAGENT_TYPE"):
        if os.environ.get(var):
            return True
    return False


def load_invocations() -> dict:
    if not INVOCATION_STATE.exists():
        return {}
    try:
        return json.loads(INVOCATION_STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_last_assistant_message(transcript_path: str) -> str:
    """Read JSONL transcript, return text content of most recent assistant message."""
    p = Path(transcript_path)
    if not p.exists():
        return ""
    try:
        # Read the tail — full transcripts can be huge
        with p.open("r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return ""
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line)
        except Exception:
            continue
        # Claude Code transcript schema varies; try common shapes
        if evt.get("type") in ("assistant", "message") or evt.get("role") == "assistant":
            content = evt.get("content") or evt.get("message", {}).get("content") or evt.get("text")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                parts = []
                for c in content:
                    if isinstance(c, dict):
                        if c.get("type") == "text":
                            parts.append(c.get("text", ""))
                        elif "text" in c:
                            parts.append(c["text"])
                return "\n".join(parts)
    return ""


def detect_diagram_blocks(text: str) -> bool:
    """True if the response contains mermaid blocks or large repo-state tables."""
    if "```mermaid" in text.lower():
        return True
    # Heuristic: a table with >5 rows referencing WDAI repos by name
    table_rows = re.findall(r"^\s*\|.*\|.*\|", text, re.MULTILINE)
    if len(table_rows) >= 6:
        repo_mentions_in_table = sum(1 for r in table_rows for repo in WDAI_REPOS if repo in r)
        if repo_mentions_in_table >= 3:
            return True
    return False


def mentioned_repos(text: str) -> list[str]:
    """Return WDAI repo names mentioned in the text (excluding URL fragments)."""
    found = []
    for repo in WDAI_REPOS:
        # Word-boundary check, count only actual mentions
        if re.search(rf"\b{re.escape(repo)}\b", text):
            found.append(repo)
    return found


def is_repo_fresh(repo_name: str, invocations: dict) -> bool:
    """Check if any path in invocations log ends with repo_name and is within fresh window."""
    now = time.time()
    for path, ts in invocations.items():
        if Path(path).name == repo_name:
            if isinstance(ts, (int, float)) and now - ts < FRESH_SECONDS:
                return True
    return False


def main() -> int:
    if in_subagent():
        return 0

    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    transcript_path = payload.get("transcript_path") or ""
    if not transcript_path:
        return 0

    msg = read_last_assistant_message(transcript_path)
    if not msg:
        return 0

    if not detect_diagram_blocks(msg):
        return 0

    mentioned = mentioned_repos(msg)
    if not mentioned:
        return 0

    invocations = load_invocations()
    stale = [r for r in mentioned if not is_repo_fresh(r, invocations)]

    if not stale:
        return 0

    # User-visible warning
    print("")
    print("⚠ [inventory-audit] Diagram / repo-state table detected without recent inventory-repo deep read.")
    print("")
    print("Repos referenced but NOT inventoried in the last 30 min:")
    for r in stale:
        print(f"  - {r}")
    print("")
    print("Polaris should have invoked before producing the diagram:")
    print("  python .claude/scripts/inventory-repo.py <repo-path>")
    print("")
    print("This is post-hoc accountability — the response already shipped. Treat its specifics")
    print("with extra skepticism until verified, or ask Polaris to re-draw after running inventory-repo.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        sys.stderr.write(f"[post-response-audit] error: {exc}\n")
        sys.exit(0)
