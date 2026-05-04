---
name: heartbeat
description: Proactive check-in with pre-gathered context. Runs every 30 minutes via CronCreate loop started at session open.
allowed-tools: Bash Read Write mcp__atlas-slack__slack_read mcp__atlas-slack__slack_send
---

Proactive heartbeat — gather context first, then reason:

1. **Gather context** (deterministic, no reasoning yet):
   ```bash
   bash .claude/scripts/gather-context.sh
   ```

2. **Check #polaris-tl for new messages** (inter-agent inbox):
   - Read `.claude/runtime/polaris-last-seen.ts` (plain text, holds the last-seen Slack ts). If missing, default to "1h ago".
   - `slack_read` channel `C0ASYTE8PB4` (#polaris-tl) limit 10
   - Surface ONLY messages where ts > last-seen AND one of:
     - sender is `U0ASQ2AGMRQ` (Polaris bot) responding to a prior Atlas message
     - text mentions `<@U0ASWSMUQLW>` (Atlas)
     - sender is Dina (`U094L7RJ9FV`) tagging Atlas
   - After processing, write the newest ts from the batch back to `.claude/runtime/polaris-last-seen.ts`.

3. **Assess**:
   - Any urgent Polaris replies waiting on Atlas action?
   - Pending/follow-up items with passed or imminent deadlines?
   - Uncommitted changes sitting for a long time?
   - Patterns in today's log suggesting an unfinished thread?

4. **Act** based on what you find:
   - Urgent Polaris reply -> surface in-terminal (or Slack to #atlas-cos if Dina is idle)
   - Urgent pending items -> notify + summarize
   - Stale uncommitted changes -> suggest committing or stashing
   - Nothing actionable -> silent. Don't output for the sake of it.

5. **Only notify if something is actionable.** Silent heartbeats are good. Don't be noisy.
   **Zero terminal output when silent.** If nothing is actionable, produce absolutely no output to the conversation — no "heartbeat complete", no summaries, no follow-up questions. The heartbeat is invisible unless something needs attention.

6. **Distill session** — only if something new was accomplished since the last distill entry in today's log. Check the last `## [HH:MM] Session Distill` timestamp — if no new work happened since then, skip entirely (no ghost entry, no output). If there IS new work, execute the distillation steps inline (do NOT use the Skill tool — `distill-session` has `disable-model-invocation`). Read `.claude/skills/distill-session/SKILL.md` and follow the steps directly in this context. Write to the daily log silently — no confirmation message, no output to the conversation.

## Notes
- The Slack bot handles channel communication — post to #atlas-cos (C0ASHFXMHM5) via slack_send if needed
- Polaris inbox is #polaris-tl (C0ASYTE8PB4). Atlas bot user ID: U0ASWSMUQLW. Polaris bot user ID: U0ASQ2AGMRQ. Dina user ID: U094L7RJ9FV.
- Scheduled tasks are managed by Windows Task Scheduler (folder: `\Atlas\`)
- If a scheduled task appears to have missed its run, check `.claude/runtime/scheduled-tasks.log`
