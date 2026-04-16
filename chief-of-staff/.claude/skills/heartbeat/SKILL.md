---
name: heartbeat
description: Proactive check-in with pre-gathered context. Run automatically via Task Scheduler (meeting-prep task, every 30 min).
disable-model-invocation: true
allowed-tools: Bash Read Write
---

Proactive heartbeat — gather context first, then reason:

1. **Gather context** (deterministic, no reasoning yet):
   ```bash
   bash .claude/scripts/gather-context.sh
   ```

2. **Read the output** and assess:
   - Are there pending/follow-up items with passed or imminent deadlines?
   - Are there uncommitted changes that have been sitting for a long time?
   - Any patterns in today's log that suggest an unfinished thread?

3. **Act** based on what you find:
   - If there are urgent pending items -> send a notification and summarize what needs attention
   - If there are stale uncommitted changes -> suggest committing or stashing
   - If nothing needs attention -> do nothing (don't generate output for the sake of it)

4. **Only notify if something is actionable.** Silent heartbeats are good. Don't be noisy.

## Notes
- The Slack bot handles channel communication — post to #atlas-cos (C0ASHFXMHM5) via slack_send if needed
- Scheduled tasks are managed by Windows Task Scheduler (folder: `\Atlas\`)
- If a scheduled task appears to have missed its run, check `.claude/runtime/scheduled-tasks.log`
