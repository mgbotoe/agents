#!/usr/bin/env python3
"""SessionStart hook — scan all known workspaces for git state.

Walks fixed workspace roots, finds git repos, prints compact digest:

  [Personal Projects]
    media-theater         master  2h ago  "feat: redesign"       3M
    tax-projection-engine main    3d ago  "fix: bracket calc"    clean (^1)
  [Women Defining AI]
    wdai-foundation       master  1h ago  "feat: matcher"        clean

Uses only local git state (no network fetch). Bounded by depth=2 from
workspace root. Per-repo git command timeout: 3s. Total time budget: ~15s.

Always exits 0. Hook failure must never block session.
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

LAST_SCAN_FILE = Path(__file__).resolve().parent.parent / "state" / "last-workspace-scan.json"

WORKSPACES = [
    (r"C:\Workspace\Personal Projects", "Personal Projects"),
    (r"C:\Workspace\Webdesign Business", "Webdesign Business"),
    (r"C:\Workspace\Webdesign Business\projects", "Webdesign Business / projects"),
    (r"C:\Workspace\Women Defining AI", "Women Defining AI"),
    (r"C:\Workspace\Women Defining AI\projects", "WDAI / projects"),
    (r"C:\Workspace\agents", "agents"),
]
MAX_DEPTH = 2
GIT_TIMEOUT = 3
NAME_WIDTH = 28


def run(cmd: list[str], cwd: Path) -> str:
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=GIT_TIMEOUT, encoding="utf-8", errors="replace")
        return r.stdout.strip()
    except Exception:
        return ""


def find_repos(root: Path, depth: int = 0) -> list[Path]:
    if not root.exists() or depth > MAX_DEPTH:
        return []
    if (root / ".git").exists():
        return [root]
    out = []
    try:
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith(".") or child.name in ("node_modules", "venv", "__pycache__"):
                continue
            out.extend(find_repos(child, depth + 1))
    except (PermissionError, OSError):
        pass
    return out


def humanize_age(iso: str) -> str:
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except Exception:
        return "?"
    delta = datetime.now(timezone.utc) - dt
    s = delta.total_seconds()
    if s < 3600:
        return f"{int(s/60)}m ago"
    if s < 86400:
        return f"{int(s/3600)}h ago"
    return f"{int(s/86400)}d ago"


def get_state(repo: Path) -> dict:
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], repo) or "?"
    last = run(["git", "log", "-1", "--pretty=format:%aI|%s"], repo)
    age = subj = ""
    if "|" in last:
        iso, subj = last.split("|", 1)
        age = humanize_age(iso)
        subj = subj[:38]

    dirty_lines = run(["git", "status", "--porcelain"], repo).splitlines()
    if dirty_lines:
        dirty = f"{len(dirty_lines)}M"
    else:
        dirty = "clean"

    # ahead/behind based on local upstream ref only (no fetch)
    ab = run(["git", "rev-list", "--count", "--left-right", "@{upstream}...HEAD"], repo)
    ahead_behind = ""
    if ab and "\t" in ab:
        behind, ahead = ab.split("\t")
        parts = []
        if int(ahead) > 0:
            parts.append(f"^{ahead}")
        if int(behind) > 0:
            parts.append(f"v{behind}")
        if parts:
            ahead_behind = " (" + " ".join(parts) + ")"

    return {"branch": branch, "age": age, "subj": subj,
            "dirty": dirty + ahead_behind}


def load_last_scan() -> set:
    if not LAST_SCAN_FILE.exists():
        return set()
    try:
        d = json.loads(LAST_SCAN_FILE.read_text(encoding="utf-8"))
        return set(d.get("repos", []))
    except Exception:
        return set()


def save_scan(repos: set) -> None:
    LAST_SCAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    LAST_SCAN_FILE.write_text(
        json.dumps({"repos": sorted(repos), "scanned_at": time.time()}, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    all_repos_this_run = set()
    any_output = False

    # Pre-pass: collect ALL repos across workspaces for new-repo detection
    for root_str, _ in WORKSPACES:
        root = Path(root_str)
        if not root.exists():
            continue
        for r in find_repos(root):
            if r.is_relative_to(root):
                all_repos_this_run.add(str(r.resolve()))

    last_repos = load_last_scan()
    new_repos = all_repos_this_run - last_repos
    if new_repos and last_repos:  # don't flag on first run (would dump everything)
        print("[workspace-scan] NEW REPOS DETECTED since last session:")
        for r in sorted(new_repos):
            print(f"  + {r}")
        print("  Action: read each repo's CLAUDE.md, add memory/projects.md entry.")
        print("")
    save_scan(all_repos_this_run)

    for root_str, label in WORKSPACES:
        root = Path(root_str)
        if not root.exists():
            continue
        repos = find_repos(root)
        # dedupe (e.g., nested workspace overlap)
        repos = [r for r in repos if r.is_relative_to(root)]
        if not repos:
            continue

        printable = []
        for repo in repos:
            try:
                s = get_state(repo)
                # only show repos with activity worth surfacing
                if s["dirty"] == "clean" and s["age"].endswith("d ago"):
                    try:
                        days = int(s["age"].split("d")[0])
                        if days > 14 and "^" not in s["dirty"] and "v" not in s["dirty"]:
                            continue  # skip stale-clean repos
                    except ValueError:
                        pass
                printable.append((repo.name, s))
            except Exception:
                continue

        if not printable:
            continue

        if not any_output:
            print("[workspace-scan]")
            any_output = True
        print(f"  [{label}]")
        for name, s in printable:
            print(f"    {name:<{NAME_WIDTH}} {s['branch']:<10} {s['age']:<8} "
                  f'"{s["subj"]}"  {s["dirty"]}')

    if not any_output:
        print("[workspace-scan] no active repos found")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[workspace-scan] error: {e}\n")
        sys.exit(0)
