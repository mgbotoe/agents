"""Single source of truth for this machine's workspace map.

Hooks/scripts that need to know "what repos live where" (workspace-scan,
log-commit) import this instead of hardcoding a Windows drive-rooted topology
that only exists on one machine.

Resolution order:
  1. $POLARIS_WORKSPACE_CONFIG — explicit path to a workspace.local.json
  2. <agent_root>/.claude/workspace.local.json — per-machine, gitignored
  3. Derive from repo location (parent of the agents repo) — keeps a fresh
     machine working before its local config is written.

Config schema: {"workspaces": [{"path": "...", "label": "..."}, ...]}
Returns: list[(Path, label)].
"""
from __future__ import annotations

import json
import os
from pathlib import Path


def _agent_root() -> Path:
    # this file: <agent_root>/.claude/scripts/_workspace.py
    return Path(__file__).resolve().parents[2]


def _config_path() -> Path | None:
    env = os.environ.get("POLARIS_WORKSPACE_CONFIG")
    if env:
        return Path(env)
    p = _agent_root() / ".claude" / "workspace.local.json"
    return p if p.exists() else None


def _derive() -> list[tuple[Path, str]]:
    """Fallback when no config exists: assume the historical sibling layout
    under the parent of the agents repo (the Windows drive-rooted workspace)."""
    agents_repo = _agent_root().parent          # <root>/agents
    root = agents_repo.parent                    # <root>
    return [
        (root / "Personal Projects", "Personal Projects"),
        (root / "Webdesign Business", "Webdesign Business"),
        (root / "Webdesign Business" / "projects", "Webdesign Business / projects"),
        (root / "Women Defining AI", "Women Defining AI"),
        (root / "Women Defining AI" / "projects", "WDAI / projects"),
        (agents_repo, "agents"),
    ]


def load_workspaces() -> list[tuple[Path, str]]:
    cfg = _config_path()
    if cfg and cfg.exists():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            out: list[tuple[Path, str]] = []
            for e in data.get("workspaces", []):
                p = e.get("path")
                if p:
                    out.append((Path(p), e.get("label") or p))
            if out:
                return out
        except Exception:
            pass
    return _derive()
