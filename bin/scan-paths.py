#!/usr/bin/env python3
"""Cross-platform path-leak guard (Bucket 1.5 of the cross-platform port plan).

Fails when a hardcoded absolute OS path (a Windows drive path or a macOS home
path) is present in CODE files. Run it in CI against the files a PR changed so
it catches NEW leaks without choking on pre-existing debt that's still ported.

  python bin/scan-paths.py [file ...]        # scan given files (CI: PR diff)
  python bin/scan-paths.py                    # scan all tracked code files
  python bin/scan-paths.py --check-hooks      # also report per-agent injector hook (warn)

Exit 1 if any leak is found in a scanned code file; 0 otherwise. A line may opt
out with a trailing `# path-ok` / `// path-ok` comment (use sparingly, e.g. the
derive-fallback example). *.example files are skipped (they show sample paths).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

CODE_EXT = {".py", ".json", ".mjs", ".js", ".ts", ".sh", ".yml", ".yaml"}
# Dirs whose content is historical/append-only or vendored — never scanned.
SKIP_DIRS = {".git", "node_modules", "__pycache__", "tmp", "daily-logs",
             "archive", "discussions"}
# Drive letter must be standalone (lookbehind excludes word:\n / re:\s escape
# sequences). Second alt matches a macOS per-user home path.
LEAK_RE = re.compile(r"(?<![A-Za-z])[A-Za-z]:\\|/Users/[^/\s\"']+/")  # path-ok
ALLOW = re.compile(r"#\s*path-ok|//\s*path-ok")
AGENTS = ["chief-of-staff", "dev-agent", "research-analyst"]


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def tracked_code_files() -> list[Path]:
    root = repo_root()
    try:
        out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True,
                             text=True, encoding="utf-8").stdout
    except Exception:
        return []
    return [root / f for f in out.splitlines()]


def should_scan(p: Path) -> bool:
    if p.suffix not in CODE_EXT:
        return False
    if p.name.endswith(".example") or ".example." in p.name:
        return False
    parts = set(p.parts)
    return not (parts & SKIP_DIRS)


def _display(f: Path) -> str:
    try:
        return f.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return f.as_posix()


def scan(files: list[Path]) -> list[str]:
    findings = []
    for f in files:
        f = f.resolve()
        if not f.exists() or not should_scan(f):
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        # Formatting findings must NOT be inside the read try/except, or a path
        # error would silently swallow real leaks (caught in testing 2026-06-18).
        for i, line in enumerate(lines, 1):
            if LEAK_RE.search(line) and not ALLOW.search(line):
                findings.append(f"{_display(f)}:{i}: {line.strip()[:100]}")
    return findings


def check_hooks() -> None:
    """Non-fatal: report which agents register the context-injector
    (decision-scan / prior-art) UserPromptSubmit hook. 'all agents' is only real
    once each agent's settings.json has it — promote to hard-fail when true."""
    root = repo_root()
    print("[hook-presence] context-injector (decision-scan) per agent:")
    for a in AGENTS:
        s = root / a / ".claude" / "settings.json"
        if not s.exists():
            print(f"  - {a}: no settings.json")
            continue
        has = "context-injector" in s.read_text(encoding="utf-8", errors="replace")
        print(f"  - {a}: {'OK' if has else 'MISSING (Atlas lane — flag, not fail)'}")


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if "--check-hooks" in argv:
        check_hooks()
    files = [Path(a) for a in args] if args else tracked_code_files()
    findings = scan(files)
    if findings:
        print(f"[scan-paths] {len(findings)} hardcoded absolute path(s) in code:")
        for f in findings:
            print(f"  {f}")
        print("Fix: derive from __file__/$0, or read a per-machine config "
              "(see _workspace.py / workspace.local.json). Intentional? add `# path-ok`.")
        return 1
    print(f"[scan-paths] clean — {len([f for f in files if should_scan(f)])} code file(s) scanned.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
