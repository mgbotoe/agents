#!/bin/bash
# Deterministic context gathering for the heartbeat.
# Runs BEFORE Claude reasons — no LLM calls here.

PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
NOW="$(date '+%Y-%m-%d %H:%M %Z')"
TODAY="$(date '+%Y-%m-%d')"

echo "# Heartbeat Context Snapshot"
echo "Generated: $NOW"
echo ""

echo "## Pending Items from identity/memory.md"
if [ -f "$PROJECT_DIR/identity/memory.md" ]; then
  grep -i -E "follow.?up|pending|todo|deadline|reminder|urgent|overdue" "$PROJECT_DIR/identity/memory.md" 2>/dev/null || echo "No pending items found."
else
  echo "No identity/memory.md found."
fi
echo ""

echo "## Today's Daily Log ($TODAY)"
DAILY_LOG="$PROJECT_DIR/daily-logs/$TODAY.md"
if [ -f "$DAILY_LOG" ]; then
  wc -l < "$DAILY_LOG" | xargs printf "%s lines logged today\n"
  echo "Last 10 lines:"
  tail -10 "$DAILY_LOG"
else
  echo "No log for today yet."
fi
echo ""

echo "## Scheduled Tasks (recent runs)"
TASK_LOG="$PROJECT_DIR/.claude/runtime/scheduled-tasks.log"
if [ -f "$TASK_LOG" ]; then
  echo "Last 5 task runs:"
  tail -5 "$TASK_LOG" 2>/dev/null || echo "Could not read task log."
else
  echo "No scheduled-tasks.log found."
fi
echo ""

echo "## Git Status"
cd "$PROJECT_DIR"
if git rev-parse --git-dir > /dev/null 2>&1; then
  BRANCH=$(git branch --show-current 2>/dev/null)
  UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | xargs)
  LAST_COMMIT=$(git log -1 --format='%h %s (%cr)' 2>/dev/null)
  echo "Branch: $BRANCH"
  echo "Uncommitted changes: $UNCOMMITTED files"
  echo "Last commit: $LAST_COMMIT"
else
  echo "Not a git repository."
fi
echo ""

echo "## Discord Bot Health"
DISCORD_SESSION="$PROJECT_DIR/.claude/runtime/discord-sessions"
if [ -d "$DISCORD_SESSION" ]; then
  SESSION_COUNT=$(ls "$DISCORD_SESSION"/*.json 2>/dev/null | wc -l | xargs)
  echo "Discord session files: $SESSION_COUNT"
  for f in "$DISCORD_SESSION"/*.json; do
    [ -f "$f" ] && echo "  $(basename "$f"): $(wc -c < "$f") bytes"
  done
else
  echo "No Discord session directory found."
fi
DISCORD_LOG="$PROJECT_DIR/.claude/runtime/discord-watcher.log"
if [ -f "$DISCORD_LOG" ]; then
  echo "Last Discord watcher entry:"
  tail -3 "$DISCORD_LOG" 2>/dev/null
fi
echo ""

echo "## Recent File Changes (last 2 hours)"
find "$PROJECT_DIR" -not -path '*/.git/*' -not -path '*/.claude/runtime/*' -not -path '*/.claude/memory.db*' -not -path '*/node_modules/*' -type f -mmin -120 2>/dev/null | head -10 || echo "No recent changes."
echo ""
