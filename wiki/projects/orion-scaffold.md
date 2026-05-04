# Orion Scaffold — Handoff Spec for Polaris

**Status:** Identity seeded by Atlas 2026-04-19. Awaiting Slack app creation (Dina) + infra scaffold (Polaris).

Third standalone agent after Atlas (chief-of-staff) and Polaris (dev-agent). Mandate: healthtech + AI research/analyst. Reports to Atlas.

**Naming convention:** folder name = role (`research-analyst`). Agent persona = Orion. Matches `chief-of-staff` pattern; `dev-agent` is inconsistent (see open question).

---

## What's Already Done (Atlas)

- Directory: `C:\Workspace\agents\research-analyst\` with `identity/`, `memory/`, `daily-logs/`, `.claude/rules/`
- `identity/SOUL.md` — soul + voice + scope boundaries
- `identity/user.md` — Dina's context through the research lens
- `identity/memory.md` — hot memory seed with mandate + source tiers
- `memory/sources.md` — curated source list v1

## What Dina Does

1. Create Slack app "Orion" at https://api.slack.com/apps
2. Enable Socket Mode, generate App-Level Token (xapp-...)
3. Bot Token Scopes:
   - `chat:write`, `chat:write.public`
   - `channels:read`, `channels:history`, `channels:join`
   - `im:write`, `im:history`
   - `app_mentions:read`
   - `reactions:write`, `reactions:read`
4. Install to DaFudge workspace → copy Bot Token (xoxb-...)
5. Create channel `#orion-intel`, invite Orion bot
6. Drop tokens into a note for Polaris (not committed to git)

## What Polaris Does

### Config & watcher

- Add `orion` entry to `slack-watcher/config.json`:
  - Agent name, working dir, channel ID for #orion-intel, bot user ID, tokens from env
- Add `ORION_BOT_TOKEN` + `ORION_APP_TOKEN` to `slack-watcher/.env`
- Verify watcher spawns Orion session on @orion mention

### Agent plumbing

- `research-analyst/CLAUDE.md` — mirror Atlas's structure (identity bootstrap, rules, memory arch, scheduling, wiki)
- `research-analyst/.claude/rules/personal.md` — AI safety (copy from Atlas, adjust for research scope)
- `research-analyst/.claude/rules/security.md` — prompt-injection defense (critical for Orion — it reads external content constantly)
- `research-analyst/.claude/rules/domain.md` — research standards (source attribution, no fabrication, how to rank signals)
- `research-analyst/.claude/rules/communication.md` — analyst brief voice
- `research-analyst/.claude/hooks/` — SessionStart hook reads #orion-intel for mentions since last-seen watermark (mirror Atlas's pattern)
- `research-analyst/.claude/runtime/atlas-last-seen.ts` — watermark for Atlas→Orion messages
- `research-analyst/bin/scheduled/run-task.cmd` — scheduled task entry point

### Skills

- `daily-scan` — iterate Tier 1 sources, classify by S1/S2/S3 taxonomy, post S1s + 5-bullet S2 summary to #orion-intel
- `weekly-digest` — Sunday 5 PM, synthesize the week's signals into themes, post to #orion-intel with @atlas mention for WeeklyReview pickup
- `deep-dive <topic>` — on-demand research for specific questions, writes to wiki/sources/ as researchable doc
- `heartbeat` — hourly check-in while session active, reads #orion-intel for Dina mentions
- `distill-session` — copy from Atlas, adjusted for research outputs

### Scheduled tasks (Windows Task Scheduler, `\ResearchAnalyst\` folder)

| Task | Schedule | Action |
|---|---|---|
| `ResearchAnalyst\DailyScan` | Daily 6:00 AM | Run daily-scan skill → #orion-intel |
| `ResearchAnalyst\WeeklyDigest` | Sunday 5:00 PM | Run weekly-digest skill before Atlas's WeeklyReview at 6 PM |
| `ResearchAnalyst\Distill` | Every 2 hours | Save session context to daily logs |
| `ResearchAnalyst\Promote` | Daily 11:30 PM | Extract learnings → memory |
| `ResearchAnalyst\IndexLogs` | Daily 11:45 PM | Rebuild daily log search index |

### Wiki integration

- Orion writes research docs to `wiki/sources/` when Dina requests deep-dive. Routing tag optional (default: `routing: research`, Atlas picks up for context).
- Orion reads wiki broadly but writes narrowly — avoid trampling Atlas's entity pages. If Orion surfaces a new person or org, flag it to Atlas to stub; Atlas owns entity pages.

### Inter-agent comms

- Atlas → Orion: post to #orion-intel or wiki/log.md with `**Atlas:**` prefix
- Orion → Atlas: post to #atlas-cos or wiki/log.md with `**Orion:**` prefix
- Orion → Polaris: rarely needed; go through Atlas

## Verification Checklist (before declaring done)

- [ ] `@orion hello` in #orion-intel spawns a session and gets a reply
- [ ] Manually trigger `ResearchAnalyst\DailyScan` — verifies skill runs end-to-end
- [ ] Test wiki write from Orion session — confirm it doesn't stomp Atlas files
- [ ] Heartbeat reads #orion-intel for Atlas mentions, responds correctly
- [ ] SessionStart hook loads identity + recent mentions
- [ ] WeeklyDigest post appears in #orion-intel Sunday 5 PM — Atlas's Sunday 6 PM WeeklyReview includes it

## Open Questions for Dina

- Channel name: `#orion-intel` OK, or prefer something else?
- Should Orion have read-only wiki access initially, or full write like Atlas/Polaris? (Default proposal: full write, but narrowly to `wiki/sources/` and `wiki/log.md`.)
- Email feeds: several Tier 1 sources are newsletters. Want Orion to have its own Gmail label, or pipe through Dina's existing inbox?
- **Rename `dev-agent/` → `tech-lead/`?** Matches the role-named pattern (`chief-of-staff`, `research-analyst`). Touches: `slack-watcher/config.json`, scheduled task paths, any hardcoded refs in Polaris's skills + hooks + run-task.cmd. Needs a Polaris-executed migration, not a pure rename. Defer or bundle with this scaffold?

## Not In Scope For v1 (park for later)

- Writer agent integration (Orion outputs → Writer drafts LinkedIn posts)
- Scholar agent integration (Orion feeds field reading into DHA companion)
- Paid data sources (Pitchbook, Crunchbase Pro) — revisit if v1 signal quality is low

---

**Owner:** Polaris executes infra. Atlas supports on voice/output calibration. Dina: Slack app + final approval.
**Target:** First production daily scan within 1-2 sessions of Polaris work.
