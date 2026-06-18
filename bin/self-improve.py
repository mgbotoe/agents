#!/usr/bin/env python3
"""
Recursive self-improvement — cloud/PR-gated variant.

Reads the last N days of daily logs (friction signal) plus the agent's own
editable behavioral files (rules + sub-agent definitions), and asks Claude to
propose conservative refinements. Edits are written to the working tree; the
GitHub Actions workflow then opens a PR — this job NEVER pushes to master.

Safety boundary (why this differs from promote.py/discuss.py):
  promote/discuss auto-push because they touch DATA (memory, transcripts).
  self-improve touches BEHAVIOR (rules, agent defs) — categorically higher risk
  for an unattended job — so it is PR-gated, and the highest-sensitivity files
  (security.md, identity/SOUL.md, CLAUDE.md) are NEVER auto-edited. The model may
  only surface suggestions about those in `observations_for_human`, which land in
  the PR body for a human to action.

Designed to run via GitHub Actions cron (or standalone). Single Anthropic API
call, no claude.exe, no MCP servers.

Usage:
    python bin/self-improve.py --agent polaris
    python bin/self-improve.py --agent polaris --dry-run --days 14
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8192
DEFAULT_DAYS = 7

AGENT_DIRS = {"atlas": "chief-of-staff", "polaris": "dev-agent"}

# Files the job may NEVER auto-edit (defense in depth — even a PR diff should not
# originate from an autonomous job for these). Matched by relative path suffix.
OFF_LIMITS = (
    ".claude/rules/security.md",
    "identity/SOUL.md",
    "CLAUDE.md",
)

SELF_IMPROVE_TOOL = {
    "name": "submit_self_improve",
    "description": "Submit proposed self-improvement edits after analyzing recent daily logs and current behavioral files.",
    "input_schema": {
        "type": "object",
        "properties": {
            "edits": {
                "type": "array",
                "description": "Proposed edits to EDITABLE files only. Each is a full-file replacement. Empty if nothing warrants a change.",
                "items": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Repo-relative path, must be one of the editable files provided."},
                        "new_content": {"type": "string", "description": "Full replacement content for the file."},
                        "rationale": {"type": "string", "description": "Why, citing specific evidence from the daily logs."},
                    },
                    "required": ["path", "new_content", "rationale"],
                },
            },
            "observations_for_human": {
                "type": "array",
                "description": "Suggestions about OFF-LIMITS files (security.md, SOUL.md, CLAUDE.md) or anything needing human judgment. These are NOT applied — they go in the PR body.",
                "items": {"type": "string"},
            },
            "summary": {"type": "string", "description": "2-4 line report of what was proposed and what was skipped."},
        },
        "required": ["edits", "observations_for_human", "summary"],
    },
}


def is_off_limits(rel_path: str) -> bool:
    norm = rel_path.replace("\\", "/")
    return any(norm.endswith(suffix) for suffix in OFF_LIMITS)


def read_recent_logs(logs_dir: Path, days: int) -> str:
    if not logs_dir.exists():
        return ""
    cutoff = date.today() - timedelta(days=days)
    chunks = []
    for f in sorted(logs_dir.glob("*.md")):
        try:
            d = datetime.strptime(f.stem, "%Y-%m-%d").date()
        except ValueError:
            continue
        if d < cutoff:
            continue
        chunks.append(f"### {f.name}\n{f.read_text(encoding='utf-8', errors='replace')}")
    return "\n\n".join(chunks)


def collect_editable(agent_root: Path) -> dict[str, str]:
    """Editable behavioral files: rules/*.md (minus off-limits) + agents/*.md."""
    out: dict[str, str] = {}
    for sub in ("rules", "agents"):
        d = agent_root / ".claude" / sub
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            rel = f.relative_to(agent_root).as_posix()
            if is_off_limits(rel):
                continue
            out[rel] = f.read_text(encoding="utf-8", errors="replace")
    return out


def collect_skill_descriptions(agent_root: Path) -> str:
    """Skill names + frontmatter descriptions for awareness (not editable in v1)."""
    skills_dir = agent_root / ".claude" / "skills"
    if not skills_dir.is_dir():
        return ""
    lines = []
    fm_desc = re.compile(r"^description:\s*(.+)$", re.MULTILINE)
    for sk in sorted(skills_dir.glob("*/SKILL.md")):
        text = sk.read_text(encoding="utf-8", errors="replace")[:600]
        m = fm_desc.search(text)
        desc = m.group(1).strip() if m else "(no description)"
        lines.append(f"- {sk.parent.name}: {desc}")
    return "\n".join(lines)


PROMPT_TEMPLATE = """You are reviewing the operational infrastructure of an AI agent named {agent_name}, to propose conservative self-improvements grounded in evidence from recent daily logs.

# Rules of engagement (hard constraints)
- Be conservative. If unsure whether a change is an improvement, SKIP it.
- Only add, refine, or consolidate. NEVER delete a rule or remove functionality.
- Preserve intent, personality, and role. Improve clarity and coverage only.
- One concern per edit. Don't bundle unrelated changes into one file rewrite.
- Cite specific daily-log evidence in every rationale. No evidence -> no edit.
- You may ONLY edit the files listed under "Editable files". For anything about
  security rules, SOUL.md, or CLAUDE.md, do NOT edit — put a note in
  observations_for_human instead (a human will action it via PR review).
- This proposal becomes a pull request reviewed by a human before merge.

# Editable files (full current content — return full replacements for any you change)
{editable_dump}

# Skills (names + descriptions, for awareness — NOT editable in this run)
{skills}

# Recent daily logs ({days} days) — the evidence base
{logs}

Submit via the submit_self_improve tool. If nothing warrants a change, return empty edits with a summary saying so.
"""


def build_prompt(agent_name: str, editable: dict[str, str], skills: str, logs: str, days: int) -> str:
    dump = "\n\n".join(f"## {path}\n```\n{content}\n```" for path, content in editable.items())
    return PROMPT_TEMPLATE.format(
        agent_name=agent_name,
        editable_dump=dump or "(none found)",
        skills=skills or "(none)",
        logs=logs or "(no recent logs)",
        days=days,
    )


def call_claude(prompt: str) -> dict:
    client = Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
        tools=[SELF_IMPROVE_TOOL],
        tool_choice={"type": "tool", "name": "submit_self_improve"},
    )
    if resp.stop_reason == "max_tokens":
        raise RuntimeError(f"max_tokens ({MAX_TOKENS}) hit during tool_use — output truncated.")
    for block in resp.content:
        if block.type == "tool_use" and block.name == "submit_self_improve":
            return block.input
    raise RuntimeError(f"no submit_self_improve tool_use (stop_reason={resp.stop_reason})")


def apply_updates(agent_root: Path, editable: dict[str, str], result: dict, dry_run: bool) -> list[str]:
    actions: list[str] = []
    allowed = set(editable.keys())
    for edit in result.get("edits") or []:
        rel = (edit.get("path") or "").replace("\\", "/")
        body = edit.get("new_content")
        if not rel or body is None:
            continue
        # Whitelist enforcement — reject anything not in the editable set, and
        # hard-reject off-limits files even if the model returned them.
        if is_off_limits(rel) or rel not in allowed:
            actions.append(f"REJECTED (not editable): {rel}")
            continue
        if body == editable[rel]:
            continue  # no-op
        actions.append(f"edit {rel} ({len(body)} chars) — {edit.get('rationale', '')[:120]}")
        if not dry_run:
            (agent_root / rel).write_text(body, encoding="utf-8")
    return actions


def write_runtime_marker(agent_root: Path) -> None:
    runtime = agent_root / ".claude" / "runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "self-improve-last-run.ts").write_text(str(int(time.time())), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Propose self-improvement edits (PR-gated).")
    parser.add_argument("--agent", required=True, choices=list(AGENT_DIRS.keys()))
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--repo-root", default=os.environ.get("REPO_ROOT", str(Path(__file__).resolve().parent.parent)))
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2

    agent_root = Path(args.repo_root) / AGENT_DIRS[args.agent]
    if not agent_root.exists():
        print(f"ERROR: agent dir not found: {agent_root}", file=sys.stderr)
        return 2

    logs = read_recent_logs(agent_root / "daily-logs", args.days)
    if not logs.strip():
        print(f"[{args.agent}] no daily logs in last {args.days} days — nothing to learn from")
        return 0

    editable = collect_editable(agent_root)
    skills = collect_skill_descriptions(agent_root)
    prompt = build_prompt(args.agent, editable, skills, logs, args.days)

    print(f"[{args.agent}] calling Claude (model={MODEL}, editable={len(editable)} files, prompt={len(prompt)} chars)")
    try:
        result = call_claude(prompt)
    except RuntimeError as e:
        print(f"ERROR: tool-use call failed: {e}", file=sys.stderr)
        return 3

    actions = apply_updates(agent_root, editable, result, args.dry_run)
    print(f"[{args.agent}] summary: {result.get('summary', '(none)')}")
    print(f"[{args.agent}] actions ({'DRY RUN' if args.dry_run else 'applied'}):")
    for a in actions:
        print(f"  - {a}")
    for obs in result.get("observations_for_human") or []:
        print(f"  [human] {obs}")

    if not args.dry_run:
        write_runtime_marker(agent_root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
