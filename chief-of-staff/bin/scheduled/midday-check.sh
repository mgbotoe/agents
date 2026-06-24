#!/usr/bin/env bash
# Midday Check — 11 AM PT. Silent unless something needs Dina's attention.
# Only pings Slack if there's something actionable. Quiet if nothing's urgent.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTS_ROOT="$(cd "$PROJECT_DIR/.." && pwd)"
LOG_FILE="$PROJECT_DIR/.claude/runtime/scheduled-tasks.log"

mkdir -p "$PROJECT_DIR/.claude/runtime"

Log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] scheduled(midday-check): $1" >> "$LOG_FILE"
}

currentDate="$(date '+%A, %B %-d, %Y at %-I:%M %p')"

PROMPT="$(cat <<EOF
You are Atlas, Dina's Chief of Staff. It's midday. Check if anything needs Dina's attention RIGHT NOW.
CURRENT DATE/TIME: $currentDate PT. Use this as the source of truth for today's date and day of the week.

CONTEXT:
- Dina works at Danaher 7 AM - 3 PM PT.
- Slack channel: C0ASHFXMHM5 (#atlas-cos)
- Dina's tag: <@U094L7RJ9FV>
- Wiki: $AGENTS_ROOT/wiki/
- Skip weekends entirely — exit silently.
- Skip PTO/OOO days — check calendar first.

CHECKS:

1. **Afternoon meetings needing prep:** Use gcal_today. Any meetings between 12-3 PM that have wiki pages or Granola history? If so, flag them with what Dina should know going in.

2. **Time-sensitive emails since morning:** Use gmail_search with "newer_than:6h" across all accounts. Any from real people (not automated) that need a response today? Read the body of anything that looks urgent.

3. **Open action items:** Check if this morning's brief had DO TODAY items. Cross-reference with email/calendar — did any get done? Flag what's still open.

4. **Nala walk at risk:** Check if the Nala Walk event is still on the calendar or if a new meeting was scheduled over it.

5. **Relationship nudge:** Check wiki people pages — anyone important (Martin, Helen, Lauren, Brigitte) that Dina hasn't met with in 2+ weeks? Quick flag.

DECISION:
- If NOTHING is urgent → do NOT send a Slack message. Just log "midday check: all clear" and exit.
- If SOMETHING needs attention → send ONE short Slack message to C0ASHFXMHM5 via slack_send (<1000 chars):

Midday Nudge

[Only the things that actually need attention. No fluff. 2-5 bullets max.]

RULES:
- This is a nudge, not a brief. Keep it tight.
- Only ping if it's genuinely useful. Silent is the default.
- Never send "all clear!" messages — silence IS the all-clear.
EOF
)"

Log "Starting midday check"

# SAFETY GATE — fail closed until Tier-2 permissions are hardened (docs/cross-platform-port-plan.md blocker #1).
# Escalated to CRITICAL by commit security review (prompt-injection -> RCE / file-write fanout over external content).
if [ "${ATLAS_TIER2_HARDENED:-0}" != "1" ]; then
    Log "refusing to run: Tier-2 not hardened. Set ATLAS_TIER2_HARDENED=1 only after scoping --allowedTools + sanitising file writes."
    echo "Atlas Tier-2 daily-driver is permission-gated and NOT yet hardened — refusing to run. See docs/cross-platform-port-plan.md" >&2
    exit 2
fi
cd "$PROJECT_DIR"
# ⚠️ SECURITY: --dangerously-skip-permissions grants full tool access (incl. Bash) to a flow that reads
# external content (email/Granola) -> prompt-injection risk. BLOCKER before launch: scope --allowedTools +
# --disallowedTools Bash. See docs/cross-platform-port-plan.md. Tier-2 offline until fixed.
if ! claude -p "$PROMPT" --dangerously-skip-permissions; then
    Log "Midday check failed"
    exit 1
fi
Log "Midday check complete"
