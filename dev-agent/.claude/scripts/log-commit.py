#!/usr/bin/env python3
"""PostToolUse hook — appends one-liner to today's daily log when HEAD
advances in any tracked repo.

Mechanism:
  1. Maintain a list of known repos in .claude/state/known-repos.json
     (auto-discovered on first run, refreshed weekly).
  2. State file .claude/state/last-commits.json maps {repo_path: last_head}.
  3. On each call, get current HEAD for every tracked repo. If different
     from last_head, append entry to today's daily log:
        - HH:MM UTC [repo-name] `abc1234` <subject> [+lines/-lines, N files]
  4. First-run primes state without logging (no backfill).

Always exits 0. Hook failures must never block tool calls.

Performance: 17 repos x ~30ms rev-parse = ~500ms. Acceptable for
PostToolUse on Bash. Heavy commit-stat lookup only runs when HEAD
actually advanced.
"""

import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_DIR = REPO_ROOT / ".claude" / "state"
HEADS_FILE = STATE_DIR / "last-commits.json"
REPOS_FILE = STATE_DIR / "known-repos.json"
LOG_DIR = REPO_ROOT / "daily-logs"

# Workspace roots come from the shared per-machine loader (no hardcoded C:\).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _workspace import load_workspaces  # noqa: E402

WORKSPACE_ROOTS = [p for p, _ in load_workspaces()]
MAX_DEPTH = 2
REPOS_CACHE_TTL = 7 * 86400  # weekly refresh


def run(cmd: list[str], cwd: Path) -> str:
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=3, encoding="utf-8", errors="replace")
        return r.stdout.strip()
    except Exception:
        return ""


def discover_repos() -> list[str]:
    """Walk workspace roots, find dirs containing .git."""
    found = []
    seen = set()

    def walk(root: Path, depth: int = 0):
        if depth > MAX_DEPTH or not root.exists():
            return
        if (root / ".git").exists():
            resolved = str(root.resolve())
            if resolved not in seen:
                seen.add(resolved)
                found.append(resolved)
            return
        try:
            for child in sorted(root.iterdir()):
                if not child.is_dir():
                    continue
                if child.name.startswith(".") or child.name in ("node_modules", "venv", "__pycache__"):
                    continue
                walk(child, depth + 1)
        except (PermissionError, OSError):
            pass

    for root in WORKSPACE_ROOTS:
        walk(root)
    return found


def load_known_repos() -> list[str]:
    if REPOS_FILE.exists():
        try:
            data = json.loads(REPOS_FILE.read_text(encoding="utf-8"))
            ts = data.get("refreshed_at", 0)
            if time.time() - ts < REPOS_CACHE_TTL:
                return data.get("repos", [])
        except Exception:
            pass
    # rediscover
    repos = discover_repos()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    REPOS_FILE.write_text(json.dumps({"refreshed_at": time.time(), "repos": repos}, indent=2),
                          encoding="utf-8")
    return repos


def load_heads() -> dict:
    if not HEADS_FILE.exists():
        return {}
    try:
        return json.loads(HEADS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_heads(heads: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    HEADS_FILE.write_text(json.dumps(heads, indent=2), encoding="utf-8")


def get_commit_info(repo: Path, sha: str) -> dict:
    pretty = run(["git", "log", "-1", "--pretty=format:%h|%s|%aI", sha], repo)
    if not pretty or "|" not in pretty:
        return {}
    short, subject, iso = pretty.split("|", 2)
    stats = run(["git", "diff-tree", "--no-commit-id", "--numstat", sha], repo)
    files = adds = dels = 0
    for line in stats.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            files += 1
            try:
                adds += int(parts[0])
                dels += int(parts[1])
            except ValueError:
                pass
    return {"short": short, "subject": subject, "iso": iso,
            "files": files, "adds": adds, "dels": dels}


def append_entries(entries: list[tuple[str, dict]]) -> None:
    if not entries:
        return
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    hhmm = datetime.now(timezone.utc).strftime("%H:%M")
    log_path = LOG_DIR / f"{today}.md"
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    lines_to_add = []
    for repo_name, info in entries:
        lines_to_add.append(
            f"- {hhmm} UTC [{repo_name}] `{info['short']}` {info['subject']} "
            f"[+{info['adds']}/-{info['dels']}, {info['files']} files]"
        )

    if not log_path.exists():
        body = f"# {today}\n\n## Commits\n" + "\n".join(lines_to_add) + "\n"
        log_path.write_text(body, encoding="utf-8")
        return

    text = log_path.read_text(encoding="utf-8")
    if "## Commits" not in text:
        suffix = "" if text.endswith("\n") else "\n"
        log_path.write_text(text + suffix + "\n## Commits\n" + "\n".join(lines_to_add) + "\n",
                            encoding="utf-8")
        return

    lines = text.splitlines()
    out = []
    inserted = False
    i = 0
    while i < len(lines):
        out.append(lines[i])
        if not inserted and lines[i].strip() == "## Commits":
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                out.append(lines[j])
                j += 1
            out.extend(lines_to_add)
            inserted = True
            i = j
            continue
        i += 1
    log_path.write_text("\n".join(out) + ("\n" if not text.endswith("\n") else ""),
                        encoding="utf-8")


def main() -> int:
    repos = load_known_repos()
    if not repos:
        return 0

    heads = load_heads()
    is_first_run = not heads

    new_entries = []
    new_heads = dict(heads)

    for repo_str in repos:
        repo = Path(repo_str)
        if not repo.exists():
            continue
        head = run(["git", "rev-parse", "HEAD"], repo)
        if not head:
            continue
        prev = heads.get(repo_str)
        new_heads[repo_str] = head
        if is_first_run:
            continue
        if prev and prev != head:
            info = get_commit_info(repo, head)
            if info:
                new_entries.append((repo.name, info))

    save_heads(new_heads)
    append_entries(new_entries)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[log-commit] error: {e}\n")
        sys.exit(0)
