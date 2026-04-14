#!/usr/bin/env bash
# Start a Polaris (Tech Lead) agent session.
# Usage: ./bin/start-agent.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Source config
set -a
source "$PROJECT_DIR/config/agent.env"
set +a

echo "Starting Polaris (Tech Lead) session..."
echo "Working directory: $PROJECT_DIR"
echo "Session name: $AGENT_SESSION_NAME"

cd "$PROJECT_DIR"
claude --model opus
