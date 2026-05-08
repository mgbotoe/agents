#!/usr/bin/env python3
"""
Multi-turn overnight discussion between Atlas and Polaris.

Each turn loads the speaking agent's identity (CLAUDE.md, SOUL.md,
identity/memory.md, identity/user.md) as a system prompt, then asks Anthropic
for the next response. Loop until NO_RESPONSE or max_turns. Save transcript
to wiki/discussions/YYYY-MM-DD-<slug>.md.

Triggered nightly by .github/workflows/discuss.yml. Manual trigger via
`gh workflow run discuss.yml -f topic="..."` or directly:
    python bin/discuss.py --topic "..." --first-agent polaris

CLI args > env vars (DISCUSS_TOPIC, DISCUSS_FIRST_AGENT, DISCUSS_MAX_TURNS) > defaults.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
MAX_TOKENS_PER_TURN = 2048
DEFAULT_MAX_TURNS = 5
NO_RESPONSE = "NO_RESPONSE"

AGENT_DIRS = {
    "atlas": "chief-of-staff",
    "polaris": "dev-agent",
}

IDENTITY_FILES = ["CLAUDE.md", "identity/SOUL.md", "identity/user.md", "identity/memory.md"]


def load_agent_identity(repo_root: Path, agent: str) -> str:
    agent_root = repo_root / AGENT_DIRS[agent]
    if not agent_root.exists():
        raise FileNotFoundError(f"agent dir missing: {agent_root}")
    chunks = []
    for rel in IDENTITY_FILES:
        path = agent_root / rel
        if path.exists():
            chunks.append(f"# {rel}\n\n{path.read_text(encoding='utf-8', errors='replace')}")
    if not chunks:
        raise FileNotFoundError(f"no identity files found under {agent_root}")
    return "\n\n---\n\n".join(chunks)


def pick_topic(repo_root: Path, override: str | None) -> dict:
    if override:
        return {"topic": override, "first_agent": None}
    topics_path = repo_root / "bin" / "topics.yml"
    with topics_path.open(encoding="utf-8") as f:
        topics = yaml.safe_load(f)
    week = datetime.now(timezone.utc).isocalendar().week
    chosen = topics[week % len(topics)]
    return {"topic": chosen["topic"], "first_agent": chosen.get("first_agent")}


def build_user_message(speaker: str, listener: str, topic: str, thread: list[dict]) -> str:
    if thread:
        history_lines = []
        for msg in thread:
            history_lines.append(f"### {msg['from']}\n{msg['content']}\n")
        history = "\n".join(history_lines)
    else:
        history = "(no prior turns — you speak first)"

    return f"""You are speaking with {listener}, your sister agent. This is an automated overnight discussion. Dina is asleep — she'll read the transcript when she wakes up.

# Discussion topic
{topic}

# Conversation so far
{history}

# Your turn
Respond as {speaker}, in your established voice. Keep it under 250 words. Be substantive and concrete:
- Propose specific changes (file paths, exact text, named tasks)
- Identify real issues you see in the codebase, memory, or workflow
- Push back if you disagree with the other agent — directly, with reasoning
- Reference your memory and recent daily logs for evidence

Do NOT:
- Repeat what the other agent just said
- Add filler ("great point", "I agree we should...")
- Speak as Dina or claim authority you don't have
- Take actions you can't verify (you have no MCP tools right now — propose, don't claim)

If the discussion has reached a natural conclusion, OR if you have nothing substantive to add, return EXACTLY this single token and nothing else: {NO_RESPONSE}"""


def call_agent(client: Anthropic, system_prompt: str, user_message: str) -> str:
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS_PER_TURN,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in resp.content if block.type == "text").strip()


def slugify(text: str, max_len: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len].rstrip("-") or "discussion"


def write_transcript(repo_root: Path, topic: str, first_agent: str, thread: list[dict], ended_by: str) -> Path:
    out_dir = repo_root / "wiki" / "discussions"
    out_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = out_dir / f"{today}-{slugify(topic)}.md"

    lines = [
        "---",
        f"date: {today}",
        f"topic: {topic.replace(chr(10), ' ')}",
        f"first_agent: {first_agent}",
        f"turns: {len(thread)}",
        f"ended_by: {ended_by}",
        "---",
        "",
        f"# {topic}",
        "",
        f"_First agent: **{first_agent}** — {len(thread)} turn(s) — ended by **{ended_by}**_",
        "",
    ]
    for i, msg in enumerate(thread, 1):
        lines.append(f"## Turn {i} — {msg['from']}")
        lines.append("")
        lines.append(msg["content"])
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def env_or_none(key: str) -> str | None:
    v = os.environ.get(key, "").strip()
    return v if v else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an overnight discussion between Atlas and Polaris.")
    parser.add_argument("--topic", default=env_or_none("DISCUSS_TOPIC"))
    parser.add_argument("--first-agent", choices=["atlas", "polaris"], default=env_or_none("DISCUSS_FIRST_AGENT"))
    parser.add_argument("--max-turns", type=int, default=int(env_or_none("DISCUSS_MAX_TURNS") or DEFAULT_MAX_TURNS))
    parser.add_argument("--repo-root", default=os.environ.get("REPO_ROOT", str(Path(__file__).resolve().parent.parent)))
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        return 2

    repo_root = Path(args.repo_root)
    selection = pick_topic(repo_root, args.topic)
    topic = selection["topic"]
    first_agent = args.first_agent or selection["first_agent"] or "atlas"
    other = "polaris" if first_agent == "atlas" else "atlas"

    print(f"topic: {topic}")
    print(f"first agent: {first_agent} (vs {other})")
    print(f"max turns: {args.max_turns}")
    print(f"model: {MODEL}\n")

    client = Anthropic()
    identities = {a: load_agent_identity(repo_root, a) for a in AGENT_DIRS}

    thread: list[dict] = []
    ended_by = f"max_turns={args.max_turns}"

    for turn in range(args.max_turns):
        speaker = first_agent if turn % 2 == 0 else other
        listener = other if speaker == first_agent else first_agent
        print(f"--- turn {turn + 1}: {speaker} → {listener} ---")
        user_message = build_user_message(speaker, listener, topic, thread)
        try:
            response = call_agent(client, identities[speaker], user_message)
        except Exception as e:
            print(f"ERROR on turn {turn + 1} ({speaker}): {e}", file=sys.stderr)
            return 3

        if response.strip() == NO_RESPONSE:
            print(f"{speaker} returned {NO_RESPONSE} — ending thread")
            ended_by = f"{NO_RESPONSE} from {speaker}"
            break

        thread.append({"from": speaker, "content": response})
        snippet = response.replace("\n", " ")
        print(snippet[:240] + ("..." if len(snippet) > 240 else "") + "\n")

    if not thread:
        print("nothing said — skipping transcript")
        return 0

    out = write_transcript(repo_root, topic, first_agent, thread, ended_by)
    print(f"transcript saved: {out.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
