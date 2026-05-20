#!/usr/bin/env python3
"""repo-aware: scan a repo's actual file inventory and surface drift vs documented claims.

Run before producing substantive analysis about a repo's state (roadmaps,
ADRs, pending-review trackers, design docs). The PreToolUse hook
`repo-aware-hook.py` enforces invocation before Edit/Write on those paths.

Usage:
    python .claude/scripts/repo-aware.py <repo-path>

Outputs:
- Markdown report to stdout (file counts by category, top-level tree,
  drift between docs and reality)
- JSON cache to .claude/state/repo-aware-cache.json keyed by repo path

Cache key: absolute repo path (resolved). Cache freshness window: 30 min.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from collections import defaultdict

DEV_AGENT_ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_PATH = DEV_AGENT_ROOT / ".claude" / "state" / "repo-aware-cache.json"
CACHE_FRESHNESS_SECONDS = 30 * 60  # 30 minutes

# Files that make claims about repo state and require awareness
CLAIM_BEARING_PATTERNS = [
    r"roadmap.*\.md$",
    r"pending-.*\.md$",
    r"design-doc.*\.md$",
    r"decisions/[^/]+\.md$",
    r"docs/repos\.md$",
    r"docs/conventions/.*\.md$",
]

CATEGORY_RULES = [
    ("Skills", lambda p: ".claude/skills/" in p.as_posix()),
    ("Hooks/Scripts", lambda p: ".claude/scripts/" in p.as_posix() or ".claude/hooks/" in p.as_posix()),
    ("GitHub config", lambda p: ".github/" in p.as_posix()),
    ("ADRs / decisions", lambda p: "decisions/" in p.as_posix() or "docs/adr/" in p.as_posix()),
    ("Conventions / playbooks", lambda p: "docs/conventions/" in p.as_posix()),
    ("Design docs", lambda p: "design-doc" in p.name.lower()),
    ("Roadmap / planning", lambda p: "roadmap" in p.name.lower() or "pending-" in p.name.lower()),
    ("Observability", lambda p: "docs/observability/" in p.as_posix()),
    ("Team onboarding", lambda p: "team/" in p.as_posix() and "ingest" in p.name or "team/onboarding" in p.as_posix() or "team/github" in p.as_posix()),
    ("Other team", lambda p: p.parts and p.parts[0] == "team"),
    ("Other docs", lambda p: p.parts and p.parts[0] == "docs"),
    ("Root config", lambda p: p.parent.as_posix() == "."),
    ("Placeholders", lambda p: p.name == ".gitkeep"),
    ("Source code", lambda p: p.suffix in {".ts", ".tsx", ".js", ".jsx", ".py", ".rb", ".go", ".rs", ".java"}),
    ("Tests", lambda p: "test" in p.as_posix().lower() and p.suffix in {".ts", ".tsx", ".js", ".jsx", ".py"}),
]


def list_files(repo: Path) -> list[Path]:
    """Return relative paths of all files in the repo's working tree.

    Combines tracked + untracked-not-ignored so that files on the current
    branch + uncommitted additions are all visible. Falls back to os.walk
    if not a git repo.
    """
    if (repo / ".git").exists():
        try:
            out = subprocess.run(
                ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                cwd=str(repo),
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            seen: set[str] = set()
            paths: list[Path] = []
            for line in out.stdout.splitlines():
                line = line.strip()
                if line and line not in seen:
                    seen.add(line)
                    paths.append(Path(line))
            return paths
        except (subprocess.SubprocessError, OSError):
            pass

    # Fallback: walk excluding common noise
    skip_dirs = {".git", "node_modules", ".next", "dist", "build", "__pycache__", ".venv", "venv"}
    result = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
        for f in files:
            full = Path(root) / f
            try:
                rel = full.relative_to(repo)
                result.append(rel)
            except ValueError:
                continue
    return result


# Template-placeholder tokens that should NOT count as real path claims
PLACEHOLDER_TOKENS = (
    "YYYY", "MM-DD", "MM", "DD", "WW", "QN", "NN",
    "NNNN", "<", "[name]", "[", "*", "{",
)


def is_placeholder_path(p: str) -> bool:
    """True if a path string is clearly a template, not a real claim."""
    if not p:
        return True
    return any(tok in p for tok in PLACEHOLDER_TOKENS)


def categorize(files: list[Path]) -> dict[str, list[Path]]:
    buckets: dict[str, list[Path]] = defaultdict(list)
    for f in files:
        placed = False
        for name, predicate in CATEGORY_RULES:
            try:
                if predicate(f):
                    buckets[name].append(f)
                    placed = True
                    break
            except Exception:
                continue
        if not placed:
            buckets["Uncategorized"].append(f)
    return dict(buckets)


def find_claim_bearing(files: list[Path]) -> list[Path]:
    """Files whose content makes claims about repo state."""
    claim_files = []
    for f in files:
        posix = f.as_posix()
        for pattern in CLAIM_BEARING_PATTERNS:
            if re.search(pattern, posix, re.IGNORECASE):
                claim_files.append(f)
                break
    return claim_files


# Regex for extracting file-like references from markdown
PATH_REF_RE = re.compile(
    r"""(?x)
    (?:
      \[[^\]]+\]\(   # markdown link text
        ([^)\s#]+)   # captured path (no fragment / no spaces / closing paren)
      \)
    |
      `([^`]*?\.(?:md|py|ts|tsx|js|jsx|yml|yaml|json|toml))`   # backtick file ref
    |
      \b(\.{1,2}/[^\s)`,;]+\.(?:md|py|ts|tsx|js|jsx|yml|yaml|json|toml))\b   # relative path
    )
    """
)

ADR_REF_RE = re.compile(r"\bADR-(\d{3,4})\b")


def extract_claims(repo: Path, claim_files: list[Path]) -> dict:
    """Walk claim-bearing files, extract file path + ADR references."""
    referenced_paths: set[str] = set()
    referenced_adrs: set[str] = set()
    for cf in claim_files:
        try:
            text = (repo / cf).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in PATH_REF_RE.finditer(text):
            for grp in m.groups():
                if grp and not grp.startswith(("http://", "https://", "mailto:")):
                    # Normalize relative-to-file references
                    candidate = grp.lstrip("./")
                    referenced_paths.add(candidate)
        for m in ADR_REF_RE.finditer(text):
            referenced_adrs.add(m.group(1).zfill(4))
    return {"paths": referenced_paths, "adrs": referenced_adrs}


def find_drift(repo: Path, files: list[Path], claims: dict) -> dict:
    file_set = {f.as_posix() for f in files}
    file_names = {f.name for f in files}

    # Claimed paths that don't exist
    claimed_missing = []
    for p in claims["paths"]:
        # Skip section anchors / urls / template placeholders
        if "#" in p or "://" in p or is_placeholder_path(p):
            continue
        # Match by basename or full posix
        bn = Path(p).name
        if p not in file_set and bn not in file_names:
            # Also try ignoring leading directory traversal
            if not any(f.endswith(bn) for f in file_set):
                claimed_missing.append(p)

    # ADRs claimed but no file
    adr_files = [f for f in files if re.match(r"(decisions|docs/adr)/\d{4}-", f.as_posix())]
    adr_nums = set()
    for f in adr_files:
        m = re.match(r".*?/(\d{4})-", f.as_posix())
        if m:
            adr_nums.add(m.group(1))
    missing_adrs = sorted(claims["adrs"] - adr_nums)

    # Substantive files present but never referenced anywhere
    referenced_basenames = {Path(p).name for p in claims["paths"]}
    substantive = [
        f for f in files
        if f.suffix == ".md"
        and f.name not in {"README.md", ".gitkeep"}
        and "team/onboarding" not in f.as_posix()  # onboarding files cross-link mostly internally
    ]
    unreferenced = [
        f.as_posix() for f in substantive
        if f.name not in referenced_basenames and f.as_posix() not in claims["paths"]
    ]

    return {
        "claimed_missing": claimed_missing[:20],  # cap output
        "missing_adrs": missing_adrs,
        "unreferenced_substantive": unreferenced[:20],
        "claimed_missing_total": len(claimed_missing),
        "unreferenced_total": len(unreferenced),
    }


def render_tree(files: list[Path], max_depth: int = 2) -> list[str]:
    seen = set()
    lines = []
    for f in sorted(files, key=lambda p: p.as_posix()):
        parts = f.parts
        for d in range(min(len(parts), max_depth)):
            prefix = "/".join(parts[: d + 1])
            if prefix in seen:
                continue
            seen.add(prefix)
            indent = "  " * d
            tail = "/" if d < len(parts) - 1 else ""
            lines.append(f"{indent}{parts[d]}{tail}")
    return lines


def last_commit_info(repo: Path) -> str:
    if not (repo / ".git").exists():
        return "(not a git repo)"
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%h %s (%cr)"],
            cwd=str(repo),
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        return out.stdout.strip() or "(no commits)"
    except (subprocess.SubprocessError, OSError):
        return "(unknown)"


def render_report(repo: Path, buckets: dict, drift: dict, last_commit: str, total_files: int) -> str:
    lines = []
    lines.append(f"# repo-aware: {repo.name}")
    lines.append("")
    lines.append(f"**Path:** `{repo}`")
    lines.append(f"**Last commit:** {last_commit}")
    lines.append(f"**Total tracked files:** {total_files}")
    lines.append("")

    lines.append("## Inventory by category")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---|")
    for cat in sorted(buckets.keys(), key=lambda k: -len(buckets[k])):
        lines.append(f"| {cat} | {len(buckets[cat])} |")
    lines.append("")

    # Show substantive categories in detail (skip Placeholders, Uncategorized noise)
    detail_categories = [
        "ADRs / decisions",
        "Skills",
        "Conventions / playbooks",
        "Roadmap / planning",
        "Design docs",
        "GitHub config",
        "Hooks/Scripts",
    ]
    for cat in detail_categories:
        if cat in buckets and buckets[cat]:
            lines.append(f"### {cat}")
            for f in sorted(buckets[cat], key=lambda p: p.as_posix()):
                lines.append(f"- `{f.as_posix()}`")
            lines.append("")

    # Drift section
    lines.append("## Drift analysis")
    lines.append("")
    if not (drift["claimed_missing"] or drift["missing_adrs"] or drift["unreferenced_substantive"]):
        lines.append("No drift detected. Claims match reality.")
    else:
        if drift["claimed_missing"]:
            lines.append(f"### Claimed but missing ({drift['claimed_missing_total']} total, showing up to 20)")
            for p in drift["claimed_missing"]:
                lines.append(f"- `{p}` referenced but not found in repo")
            lines.append("")
        if drift["missing_adrs"]:
            lines.append(f"### Broken ADR references")
            for n in drift["missing_adrs"]:
                lines.append(f"- ADR-{n} referenced but `decisions/{n}-*.md` not found")
            lines.append("")
        if drift["unreferenced_substantive"]:
            lines.append(f"### Substantive files never referenced ({drift['unreferenced_total']} total, showing up to 20)")
            lines.append("(may indicate docs that exist but aren't linked from the roadmap/ADRs/conventions)")
            for f in drift["unreferenced_substantive"]:
                lines.append(f"- `{f}`")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("_Cache written. Subsequent edits to roadmap/decisions/conventions in this repo will pass the PreToolUse hook for the next 30 minutes._")

    return "\n".join(lines)


def update_cache(repo: Path, payload: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    cache: dict = {}
    if CACHE_PATH.exists():
        try:
            cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            cache = {}
    cache[str(repo)] = payload
    CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: repo-aware.py <repo-path>", file=sys.stderr)
        return 1

    try:
        repo = Path(argv[1]).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        print(f"Could not resolve repo path: {exc}", file=sys.stderr)
        return 1
    if not repo.is_dir():
        print(f"Not a directory: {repo}", file=sys.stderr)
        return 1

    files = list_files(repo)
    buckets = categorize(files)
    claim_files = find_claim_bearing(files)
    claims = extract_claims(repo, claim_files)
    drift = find_drift(repo, files, claims)
    last_commit = last_commit_info(repo)

    report = render_report(repo, buckets, drift, last_commit, len(files))
    print(report)

    update_cache(
        repo,
        {
            "scanned_at": time.time(),
            "total_files": len(files),
            "categories": {k: len(v) for k, v in buckets.items()},
            "drift_counts": {
                "claimed_missing": drift["claimed_missing_total"],
                "missing_adrs": len(drift["missing_adrs"]),
                "unreferenced": drift["unreferenced_total"],
            },
        },
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
