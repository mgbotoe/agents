#!/usr/bin/env bash
# One-time Polaris bootstrap for a fresh Mac (or any POSIX machine).
# Mirrors what the Windows box already has. Idempotent — safe to re-run.
#
# Usage:  ./bin/setup-mac.sh
#
# Assumes the repo is cloned at <root>/agents/dev-agent so path derivation
# in the Python hooks/scripts works without configuration.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
cd "$REPO_DIR"

echo "Polaris Mac bootstrap"
echo "  repo: $REPO_DIR"

# 1. Prerequisites ----------------------------------------------------------
for bin in python3 node npm git; do
  if ! command -v "$bin" >/dev/null 2>&1; then
    echo "  MISSING: $bin — install it (brew install $bin) and re-run." >&2
    exit 1
  fi
done
echo "  prereqs: python3 $(python3 --version 2>&1 | awk '{print $2}'), node $(node --version), git ok"

# 2. Secrets file -----------------------------------------------------------
if [ ! -f config/secrets.env ]; then
  cp config/secrets.env.example config/secrets.env
  # Pre-fill the repo path since we know it.
  if grep -q '^POLARIS_DEV_AGENT=$' config/secrets.env; then
    tmp="$(mktemp)"
    sed "s|^POLARIS_DEV_AGENT=$|POLARIS_DEV_AGENT=$REPO_DIR|" config/secrets.env > "$tmp"
    mv "$tmp" config/secrets.env
  fi
  echo "  created config/secrets.env — FILL IN the Slack tokens before using Slack MCP."
else
  echo "  config/secrets.env already exists — leaving it."
fi

# 3. MCP config -------------------------------------------------------------
if [ ! -f .mcp.json ]; then
  cp .mcp.json.example .mcp.json
  echo "  created .mcp.json from template (uses \${POLARIS_DEV_AGENT}/\${*_SLACK_TOKEN})."
else
  echo "  .mcp.json already exists — leaving it."
fi

# 4. Slack MCP deps ---------------------------------------------------------
if [ -d mcp/slack ]; then
  echo "  installing Slack MCP deps..."
  ( cd mcp/slack && npm install --silent )
  echo "  mcp/slack deps installed."
fi

# 5. Python shim ------------------------------------------------------------
# Hooks invoke bare `python`; macOS ships only `python3`. A user-local shim lets
# the committed hook commands resolve without editing them per-machine.
if ! command -v python >/dev/null 2>&1; then
  mkdir -p "$HOME/.local/bin"
  ln -sf "$(command -v python3)" "$HOME/.local/bin/python"
  echo "  created ~/.local/bin/python -> python3 (ensure ~/.local/bin is on PATH)"
else
  echo "  python already on PATH."
fi

# 6. GitHub auth (private claude-skills marketplace) ------------------------
# custom-skills is a PRIVATE repo; cloning/pulling it needs git credentials.
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  echo "  gh auth: ok (private claude-skills clone will work)."
else
  echo "  WARNING: GitHub auth not detected — run 'gh auth login' (or set up an" >&2
  echo "           SSH key / GITHUB_TOKEN), else the claude-skills marketplace won't sync." >&2
fi

# 7. Wire the cross-machine skill-sync hook ---------------------------------
# Claude Code does not auto-pull github marketplaces (issue #44276). Register the
# sync-skills SessionStart hook in the user-level settings.local.json (gitignored,
# per-machine). Idempotent — only adds it if absent. Needs ~/.claude cloned first.
SYNC_HOOK="python3 $HOME/.claude/hooks/sync-skills.py"
set +e
python3 - "$HOME/.claude/settings.local.json" "$SYNC_HOOK" <<'PY'
import json, os, sys
path, cmd = sys.argv[1], sys.argv[2]
data = {}
if os.path.exists(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except Exception:
        data = {}
hooks = data.setdefault("hooks", {})
ss = hooks.setdefault("SessionStart", [])
present = any(h.get("command") == cmd for entry in ss for h in entry.get("hooks", []))
if not present:
    ss.append({"hooks": [{"type": "command", "command": cmd}]})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print("  added sync-skills SessionStart hook to settings.local.json")
else:
    print("  sync-skills hook already present.")
PY
set -e

# 8. Shell profile reminder -------------------------------------------------
cat <<EOF

Next steps:
  1. Edit config/secrets.env and paste POLARIS_SLACK_TOKEN + WDAI_SLACK_TOKEN.
  2. Add to ~/.zshrc so the env vars load for every session:

       set -a; source "$REPO_DIR/config/secrets.env"; set +a

  3. Start a session:  ./bin/start-agent.sh
  4. Verify MCP loaded:  the polaris-slack / wdai-slack servers should connect.

Scheduling note: recurring automation runs via GitHub Actions cloud cron
(agents repo .github/workflows/) and Claude Code hooks — both OS-agnostic.
No local scheduler setup is needed on the Mac.
EOF
