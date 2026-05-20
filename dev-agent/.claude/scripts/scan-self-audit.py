#!/usr/bin/env python3
"""SessionStart hook — surface Polaris's own slip patterns.

Reads recent git history + daily logs to detect behavioral patterns
that contradict learned lessons. Flags at SessionStart so I can't
ignore my own data when proposing/answering.

Detected patterns (over last 7 days):
  1. RULE WITHOUT MECHANISM
     A commit touched .claude/rules/ but NOT .claude/scripts/ on the
     same day. Rules ship without mechanical enforcement.

  2. ARCHITECTURE WITHOUT ADVISOR
     A commit touched .claude/rules/, identity/SOUL.md, or settings.json
     but the day's daily log shows no advisor() call.

  3. COMMIT INCOHERENCE
     >=4 commits in dev-agent in one day. Possible muddied scope or
     "many small bundles" anti-pattern.

  4. DELEGATION SCANNER MISS (already covered by scan-missed-delegations.py
     — don't duplicate; just note overlap exists)

Always exits 0. Pure analysis, no LLM. Quiet by default — only prints
when something flags.
"""

import re
import subprocess
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = REPO_ROOT / "daily-logs"
WINDOW_DAYS = 7


def run(cmd: list[str]) -> str:
    try:
        r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True,
                           timeout=10, encoding="utf-8", errors="replace")
        return r.stdout
    except Exception:
        return ""


def get_recent_commits() -> list[dict]:
    """Return commits in last WINDOW_DAYS days, with date + changed paths."""
    since = (date.today() - timedelta(days=WINDOW_DAYS)).isoformat()
    raw = run(["git", "log", f"--since={since}", "--pretty=format:%H|%aI|%s",
               "--name-only"])
    commits = []
    cur = None
    for line in raw.splitlines():
        if "|" in line and line.count("|") >= 2 and len(line.split("|")[0]) == 40:
            if cur:
                commits.append(cur)
            sha, iso, subj = line.split("|", 2)
            cur = {"sha": sha, "date": iso[:10], "subject": subj, "files": []}
        elif line.strip() and cur is not None:
            cur["files"].append(line.strip())
    if cur:
        commits.append(cur)
    return commits


def daily_log_text(d: str) -> str:
    p = LOG_DIR / f"{d}.md"
    if not p.exists():
        return ""
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def detect_patterns():
    commits = get_recent_commits()
    if not commits:
        return []

    # Group commits by date
    by_day = defaultdict(list)
    for c in commits:
        by_day[c["date"]].append(c)

    flags = []
    for day, day_commits in sorted(by_day.items(), reverse=True):
        all_files = [f for c in day_commits for f in c["files"]]
        touched_rules = any("dev-agent/.claude/rules/" in f or
                            f.startswith(".claude/rules/") for f in all_files)
        touched_soul = any(f.endswith("identity/SOUL.md") or
                           f.endswith("settings.json") for f in all_files)
        touched_scripts = any("dev-agent/.claude/scripts/" in f or
                              f.startswith(".claude/scripts/") for f in all_files)

        log_text = daily_log_text(day)
        has_advisor = bool(re.search(r"\badvisor\(\)", log_text))

        # Pattern 1: rule without mechanism
        if touched_rules and not touched_scripts:
            flags.append({
                "date": day,
                "type": "RULE WITHOUT MECHANISM",
                "detail": "rules/ modified, no scripts/ change same day",
            })

        # Pattern 2: architecture-flavored change without advisor signal
        if (touched_rules or touched_soul) and not has_advisor:
            flags.append({
                "date": day,
                "type": "ARCH CHANGE WITHOUT ADVISOR",
                "detail": "rules/SOUL/settings touched, no advisor() in daily log",
            })

        # Pattern 3: commit incoherence (many small commits in dev-agent)
        dev_agent_commits = [c for c in day_commits
                             if any(f.startswith("dev-agent/") for f in c["files"])]
        if len(dev_agent_commits) >= 4:
            flags.append({
                "date": day,
                "type": "COMMIT INCOHERENCE",
                "detail": f"{len(dev_agent_commits)} dev-agent commits in one day "
                          f"(possible muddied scope)",
            })

        # Pattern 4: implementation shipped + external pattern named, no delta justification
        # KNOWN STRUCTURAL LIMIT: this regex scans daily-log PROSE. Daily logs are sparse
        # (often 4-9 lines, mostly commit metadata). Will false-negative until session-snapshot
        # or /distill-session writes substantive prose into the daily log. Effectively only
        # fires on days with rich distill content — until that upstream signal is denser,
        # treat zero flags as "no signal" not "no slips."
        external_pattern_mentioned = bool(re.search(
            r"\b(openclaw|cline|cursor|aider|langchain|crewai|autogen|"
            r"github\.com/|public\s+(repo|pattern|framework)|prior\s+art)\b",
            log_text, re.IGNORECASE,
        ))
        ships_implementation = any(
            f.endswith(".py") or f.endswith(".ts") or f.endswith(".tsx")
            or "scripts/" in f or "skills/" in f
            for f in all_files
        )
        delta_acknowledged = bool(re.search(
            r"\b(delta:|improvement\s+over|we\s+changed|match(ing)?\s+prior\s+art|"
            r"different\s+from|extends?\s+\w+\s+by|no\s+delta)\b",
            log_text, re.IGNORECASE,
        ))
        if external_pattern_mentioned and ships_implementation and not delta_acknowledged:
            flags.append({
                "date": day,
                "type": "DELTA UNNAMED",
                "detail": "shipped implementation citing external pattern, "
                          "but no delta/improvement justification in daily log",
            })

    return flags


def main() -> int:
    flags = detect_patterns()
    if not flags:
        return 0

    # Deduplicate by (date, type)
    seen = set()
    unique = []
    for f in flags:
        key = (f["date"], f["type"])
        if key not in seen:
            seen.add(key)
            unique.append(f)

    print(f"[self-audit] {len(unique)} behavioral pattern flag(s) in last {WINDOW_DAYS}d:")
    for f in unique[:8]:
        print(f"  - {f['date']}: {f['type']} — {f['detail']}")
    print("[self-audit] Cross-check before proposing similar approaches.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[self-audit] error: {e}\n")
        sys.exit(0)
