#!/usr/bin/env python3
"""UserPromptSubmit hook — auto-inject relevant context before Polaris responds.

Two content sources, both triggered by prompt content:

1. WIKI PROJECT PAGES
   When the user's prompt mentions a topic that has a wiki/projects/*.md
   page, inject that page's content. Topic names derived from filename
   stems (e.g., "team-os", "agent-ecosystem", "wdai-tech-debt").

2. RELEVANT FEEDBACK / PAST LEARNINGS
   When the user's prompt contains proposal-shaped triggers ("propose",
   "let's add", "rule for", "improve", "discipline", "convention",
   "how can I make sure"), grep memory/*.md and identity/memory.md for
   relevant feedback memories, inject top matches.

Per-session deduplication: same content not re-injected in same conversation.
State: .claude/state/injected-context.json keyed by session_id.

Output goes to stdout — Claude Code adds it as additional context for the
model. No JSON wrapper needed for UserPromptSubmit (stdout becomes context).

Always exits 0. Hook failure must never block prompt.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

# Windows stdout defaults to cp1252; wiki content has em-dashes/arrows
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_ROOT = REPO_ROOT.parent / "wiki"
PROJECTS_DIR = WIKI_ROOT / "projects"
# Two memory sources: repo cold memory + Claude Code auto-memory
MEMORY_DIRS = [
    REPO_ROOT / "memory",
    Path.home() / ".claude" / "projects" / "C--Workspace-agents" / "memory",
]
HOT_MEMORY = REPO_ROOT / "identity" / "memory.md"
STATE_FILE = REPO_ROOT / ".claude" / "state" / "injected-context.json"

# Triggers that suggest a behavioral / architectural proposal is forming
PROPOSAL_TRIGGERS = re.compile(
    r"\b(propose|propos\w+|let'?s\s+add|let'?s\s+build|rule\s+for|"
    r"how\s+(can|do|should)\s+(i|we|you)\s+make\s+sure|"
    r"discipline|convention|best\s+practice|improve\s+\w+|"
    r"\bguardrails?\b|enforce|reinforce|always\s+\w+\s+when)",
    re.IGNORECASE,
)

# Triggers for substantive implementation/pattern decisions — surface prior-art reminder.
# Broader than PROPOSAL_TRIGGERS: any "how should we build/structure/design X" question.
SUBSTANTIVE_DECISION_TRIGGERS = re.compile(
    r"\b(how\s+(should|do|can)\s+(we|i|you)\s+(build|design|structure|implement|architect|approach|do|handle)|"
    r"what'?s?\s+the\s+best\s+way\s+to|"
    r"what\s+pattern\s+for|"
    r"should\s+(we|i)\s+(use|build|do|adopt)|"
    r"choose\s+between|"
    r"thinking\s+about\s+\w+ing|"
    r"considering\s+\w+ing|"
    r"is\s+there\s+a\s+better\s+way|"
    r"how\s+do\s+(others|people|repos|projects)\s+do|"
    r"what\s+does\s+the\s+(community|industry)\s+do|"
    r"\bprior\s+art\b)",
    re.IGNORECASE,
)

# Triggers for survey/inventory/landscape/diagram requests — fire BEFORE
# producing diagrams or tables claiming what's in a repo. Per inventory-repo skill.
SURVEY_INVENTORY_TRIGGERS = re.compile(
    r"\b(current\s+state|inventory|landscape|"
    r"map\s+(of|the|all)|"
    r"diagram\s+(of|for|the)|"
    r"\bmermaid\b|"
    r"what'?s?\s+(in|inside)\s+(the|our|all)\s+(repo|repos|codebase)|"
    r"what\s+does\s+\w+\s+(have|contain|use)|"
    r"survey\s+(of|the|across|our)|"
    r"audit\s+(the|of|all|our)|"
    r"scan\s+(across|all|each|every|our)|"
    r"identify\s+current|"
    r"workflows?\s+(across|in\s+all|in\s+each)|"
    r"compare\s+(the|all|across)\s+(repos|repositories))",
    re.IGNORECASE,
)

# Feedback files most relevant to "rules vs mechanisms" debates
RULE_EFFECTIVENESS_KEYWORDS = re.compile(
    r"\b(rule|enforce|discipline|hook|mechanism|advisor|verify|"
    r"branch.check|push.rule|delegation|cite|citation)\b",
    re.IGNORECASE,
)

STALE_SECONDS = 24 * 3600  # session state stale after 24h


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def prune_stale(state: dict) -> dict:
    now = time.time()
    return {k: v for k, v in state.items() if now - v.get("last_seen", 0) < STALE_SECONDS}


def list_wiki_topics() -> dict:
    """Map topic-name -> file path for wiki/projects/*.md files."""
    if not PROJECTS_DIR.exists():
        return {}
    topics = {}
    for p in PROJECTS_DIR.glob("*.md"):
        # normalize: strip .md, lowercase, both with hyphens preserved
        name = p.stem.lower()
        topics[name] = p
    return topics


def find_wiki_matches(prompt: str, topics: dict) -> list[Path]:
    """Return wiki project paths matching topics in the prompt."""
    p_lower = prompt.lower()
    matches = []
    for topic, path in topics.items():
        # word-boundary check, also allow underscore/hyphen variants
        variants = {topic, topic.replace("-", " "), topic.replace("-", "_")}
        for v in variants:
            if re.search(rf"\b{re.escape(v)}\b", p_lower):
                matches.append(path)
                break
    return matches


def find_relevant_feedback(prompt: str) -> list[Path]:
    """If prompt has proposal triggers, find feedback memories about rule-effectiveness."""
    if not PROPOSAL_TRIGGERS.search(prompt):
        return []
    candidates = []
    for src_dir in MEMORY_DIRS:
        if not src_dir.exists():
            continue
        for f in src_dir.glob("feedback_*.md"):
            try:
                content = f.read_text(encoding="utf-8")
                if RULE_EFFECTIVENESS_KEYWORDS.search(content):
                    candidates.append(f)
            except Exception:
                continue
    return candidates


def truncate(text: str, max_lines: int = 60) -> str:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    return "\n".join(lines[:max_lines]) + f"\n... ({len(lines) - max_lines} more lines truncated)"


def build_injection(session_id: str, prompt: str, state: dict) -> str:
    entry = state.get(session_id) or {"injected": [], "prior_art_marker_shown": False, "inventory_marker_shown": False}
    already = set(entry["injected"])
    prior_art_shown = entry.get("prior_art_marker_shown", False)
    inventory_shown = entry.get("inventory_marker_shown", False)

    topics = list_wiki_topics()
    wiki_matches = [p for p in find_wiki_matches(prompt, topics) if str(p) not in already]
    feedback_matches = [p for p in find_relevant_feedback(prompt) if str(p) not in already]
    needs_prior_art = (not prior_art_shown
                       and SUBSTANTIVE_DECISION_TRIGGERS.search(prompt) is not None)
    needs_inventory = (not inventory_shown
                       and SURVEY_INVENTORY_TRIGGERS.search(prompt) is not None)

    if not wiki_matches and not feedback_matches and not needs_prior_art and not needs_inventory:
        # Still update last_seen so prune works
        entry["last_seen"] = time.time()
        state[session_id] = entry
        save_state(state)
        return ""

    parts = []
    for path in wiki_matches:
        try:
            content = path.read_text(encoding="utf-8")
            parts.append(f"--- WIKI PAGE: wiki/projects/{path.name} ---\n{truncate(content)}\n")
            already.add(str(path))
        except Exception:
            continue

    if feedback_matches:
        parts.append("--- RELEVANT PAST LEARNINGS (you've encountered this pattern before) ---")
        for path in feedback_matches[:5]:  # cap at 5 to avoid bloat
            try:
                content = path.read_text(encoding="utf-8")
                parts.append(f"\n[{path.name}]\n{truncate(content, max_lines=25)}")
                already.add(str(path))
            except Exception:
                continue
        parts.append("\n--- END PAST LEARNINGS ---")

    if needs_prior_art:
        parts.append(
            "\n>>> [PRIOR ART CHECK PENDING] <<<\n"
            "Dina asked a substantive implementation question. Before forming an opinion:\n"
            "  1. Invoke /survey-prior-art skill OR run WebSearch + GitHub search for current patterns.\n"
            "  2. Produce the four-section digest: observations, criticism, our context, proposed delta.\n"
            "  3. Bring evidence and explicit delta justification BEFORE proposing.\n"
            "  4. If no delta — say so. Matching prior art is acceptable when honest.\n"
            "Per .claude/rules/personal.md research rule. Skipping this is a self-audit flag.\n"
            ">>> END MARKER <<<\n"
        )
        entry["prior_art_marker_shown"] = True

    if needs_inventory:
        parts.append(
            "\n>>> [INVENTORY CHECK PENDING] <<<\n"
            "Dina asked for a survey / inventory / landscape / diagram / 'current state' of one or more repos.\n"
            "BEFORE producing the answer (diagram, table, summary):\n"
            "  1. Invoke the inventory-repo skill against EACH target repo:\n"
            "     python .claude/scripts/inventory-repo.py \"<absolute-repo-path>\"\n"
            "  2. Read the structured output. It includes workflow TRIGGERS (not just names), full deps\n"
            "     categorized, monorepo packages, deploy + DB markers, CLAUDE.md presence.\n"
            "  3. Draw the diagram / table / summary from THAT output, not from shallow ls + grep.\n"
            "  4. Cite the source. If you infer a relationship the script didn't observe, flag it as inferred.\n"
            "Producing diagrams from shallow scans is the failure mode in\n"
            "feedback_verify_plan_against_code.md. The inventory-repo skill exists to make the\n"
            "deep read one command instead of a temptation to skip.\n"
            ">>> END MARKER <<<\n"
        )
        entry["inventory_marker_shown"] = True

    entry["injected"] = list(already)
    entry["last_seen"] = time.time()
    state[session_id] = entry
    save_state(state)

    return "\n".join(parts)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    prompt = payload.get("prompt") or ""
    session_id = payload.get("session_id") or "unknown"
    if not prompt:
        return 0

    state = prune_stale(load_state())
    injection = build_injection(session_id, prompt, state)

    if injection:
        # UserPromptSubmit additional context goes to stdout
        print(injection)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[context-injector] error: {e}\n")
        sys.exit(0)
