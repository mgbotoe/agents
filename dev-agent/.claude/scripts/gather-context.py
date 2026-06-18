#!/usr/bin/env python3
"""Deterministic context gathering for the heartbeat. Cross-platform port of
gather-context.ps1 (Windows-only PowerShell original).

Runs BEFORE Claude reasons — no LLM calls here. Emits a markdown snapshot the
heartbeat skill reads, then acts on. Silent-friendly: only the skill decides
whether anything is actionable.

Designed to run identically on Windows and macOS:
  python .claude/scripts/gather-context.py

Path-derived (no hardcoded drive), so it works wherever the repo is cloned.
Adapted from unclaw (github.com/shahshrey/unclaw).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from shutil import disk_usage

# __file__ = <root>/agents/dev-agent/.claude/scripts/gather-context.py
PROJECT_DIR = Path(__file__).resolve().parents[2]   # dev-agent
AGENTS_ROOT = PROJECT_DIR.parent                     # agents (git root)

MEM_FILE = PROJECT_DIR / "identity" / "memory.md"
RUNTIME_LOG = PROJECT_DIR / ".claude" / "runtime" / "scheduled-tasks.log"
WATCHER_PID = AGENTS_ROOT / "slack-watcher" / "watcher.pid"
WIKI_CHECK = PROJECT_DIR / ".claude" / "scripts" / "check-wiki-inbox.py"

PENDING_RE = re.compile(
    r"follow.?up|pending|todo|deadline|reminder|urgent|thinking on it|"
    r"decision pending|open question",
    re.IGNORECASE,
)


def safe_print(text: str = "") -> None:
    """Print with fallback for Windows cp1252 consoles (emoji/unicode hazard)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))


def git(args: list[str], cwd: Path) -> str:
    try:
        r = subprocess.run(["git", *args], cwd=cwd, capture_output=True,
                           text=True, timeout=5, encoding="utf-8", errors="replace")
        return r.stdout.strip()
    except Exception:
        return ""


def pid_alive(pid: int) -> bool:
    """Cross-platform liveness check. NEVER use os.kill(pid, 0) on Windows —
    Python maps non-CTRL signals to TerminateProcess, which would KILL the
    target. POSIX: signal 0 is a safe existence probe."""
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        STILL_ACTIVE = 259
        k32 = ctypes.windll.kernel32
        h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not h:
            return False
        try:
            code = wintypes.DWORD()
            if k32.GetExitCodeProcess(h, ctypes.byref(code)):
                return code.value == STILL_ACTIVE
            return True
        finally:
            k32.CloseHandle(h)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def main() -> int:
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    safe_print("# Heartbeat Context Snapshot")
    safe_print(f"Generated: {now.strftime('%Y-%m-%d %H:%M')}")
    safe_print("")

    # Pending items from hot memory
    safe_print("## Pending Items from identity/memory.md")
    if MEM_FILE.exists():
        text = MEM_FILE.read_text(encoding="utf-8", errors="replace")
        hits = [ln.strip() for ln in text.splitlines() if PENDING_RE.search(ln)]
        if hits:
            for ln in hits:
                safe_print(ln)
        else:
            safe_print("No pending items found.")
    else:
        safe_print("No identity/memory.md found.")
    safe_print("")

    # Memory staleness
    safe_print("## Memory Staleness")
    if MEM_FILE.exists():
        mtime = datetime.fromtimestamp(MEM_FILE.stat().st_mtime)
        hours = round((now - mtime).total_seconds() / 3600, 1)
        safe_print(f"Last modified: {mtime:%Y-%m-%d %H:%M} ({hours} hours ago)")
        if hours > 48:
            safe_print("WARNING: Memory is stale (>48 hours)")
    safe_print("")

    # Today's daily log
    safe_print(f"## Today's Daily Log ({today})")
    log_file = PROJECT_DIR / "daily-logs" / f"{today}.md"
    if log_file.exists():
        lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()
        safe_print(f"{len(lines)} lines logged today")
        safe_print("Last 10 lines:")
        for ln in lines[-10:]:
            safe_print(ln)
    else:
        safe_print("No log for today yet.")
    safe_print("")

    # Wiki inbox (delegate to the dedicated checker)
    safe_print("## Wiki Inbox")
    out = ""
    if WIKI_CHECK.exists():
        try:
            r = subprocess.run([sys.executable, str(WIKI_CHECK)], capture_output=True,
                               text=True, timeout=15, encoding="utf-8", errors="replace")
            out = r.stdout.strip()
        except Exception:
            out = ""
    safe_print(out if out else "No new technical items.")
    safe_print("")

    # Git status (single monorepo at AGENTS_ROOT)
    safe_print("## Git Status")
    if (AGENTS_ROOT / ".git").exists():
        branch = git(["branch", "--show-current"], AGENTS_ROOT) or "?"
        uncommitted = len(git(["status", "--porcelain"], AGENTS_ROOT).splitlines())
        last = git(["log", "-1", "--format=%h %s (%cr)"], AGENTS_ROOT)
        safe_print(f"agents: branch={branch}, uncommitted={uncommitted}, last={last}")
    else:
        safe_print("No git repo found.")
    safe_print("")

    # Channel health (slack-watcher) — PID file is canonical, liveness is safe-probed
    safe_print("## Channel Health")
    if WATCHER_PID.exists():
        try:
            pid = int(WATCHER_PID.read_text(encoding="utf-8").strip())
        except (ValueError, OSError):
            pid = 0
        if pid and pid_alive(pid):
            safe_print(f"slack-watcher: RUNNING (pid {pid})")
        else:
            safe_print(f"slack-watcher: NOT RUNNING (stale PID file - PID {pid} not found)")
    else:
        safe_print("slack-watcher: NOT RUNNING (no PID file)")
    safe_print("")

    # Recent errors in runtime log
    safe_print("## Recent Errors")
    if RUNTIME_LOG.exists():
        err_re = re.compile(r"error|fail|exception", re.IGNORECASE)
        errs = [ln for ln in RUNTIME_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
                if err_re.search(ln)]
        if errs:
            for ln in errs[-5:]:
                safe_print(ln)
        else:
            safe_print("No recent errors.")
    else:
        safe_print("No runtime log found.")
    safe_print("")

    # System — disk free on the volume holding the repo (fixes the old 0GB bug)
    safe_print("## System")
    try:
        free_gb = round(disk_usage(str(AGENTS_ROOT)).free / 1024**3, 1)
        safe_print(f"Disk: {free_gb}GB free")
        if free_gb < 10:
            safe_print("WARNING: Low disk space")
    except Exception:
        safe_print("Disk: unavailable")
    safe_print("")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as e:
        sys.stderr.write(f"[gather-context] error: {e}\n")
        raise SystemExit(0)
