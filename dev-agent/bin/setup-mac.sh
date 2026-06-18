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

# 5. Shell profile reminder -------------------------------------------------
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
