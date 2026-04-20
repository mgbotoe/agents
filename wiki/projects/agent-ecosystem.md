# Agent Ecosystem Roadmap

**Living document.** Forward-looking improvements to the Atlas + Polaris ecosystem (and future agents). Parallel to [[projects/wdai-tech-debt|WDAI Tech Debt]] but for our infrastructure.

Both agents can add items here. Updated as work ships. Mark items shipped with ✅ + commit SHA.

---

## Prioritized Backlog

### P0 — Blocks real-time inter-agent conversation

- ✅ **Mirror Atlas's polling on Polaris side** — shipped 2026-04-19. Polaris heartbeat skill now reads `#atlas-cos` since watermark at `dev-agent/.claude/runtime/atlas-last-seen.ts`; SessionStart hook also prompts the read on every spawn. Symmetric with Atlas's `polaris-last-seen.ts` pattern.

### P1 — Scale cleanly when agent #3 joins

- [ ] **Migrate from polling to cross-post + metadata marker.** Current polling model is O(N²) — each agent polls every other agent's channel. At N=3 it gets messy. Replace with: when watcher posts an agent's reply in the origin channel, ALSO cross-post a compact reference to the sender's channel with `metadata: {event_type: "agent_reply_xref", from: <agent>}`. Watcher filters messages with that event_type from re-triggering spawns. O(N) forever, adding a new agent becomes zero-code. Owner: Polaris (watcher.mjs change). Scope: M. Trigger: when a 3rd agent is actually on the table.

### P1 — Development lifecycle coverage

- ✅ **DevOps sub-agent created** — shipped 2026-04-19. `dev-agent/.claude/agents/devops.md`. Owns post-deploy monitoring, incident response, dep maintenance, release coordination. Closes DevOps/SRE/Dep-maintenance gaps. Does NOT write feature code (Builder's lane).
- ✅ **Designer unblocked for direct Builder delegation** — Designer config now has `Agent` tool. Routine "implement what I designed" handoffs skip the Polaris middle-man.
- ✅ **Delegation protocol expanded** — `CLAUDE.md` now documents shift-left pattern (parallel Builder + QA for complex features), security-sensitive tag (threat model before, pen-test after), and delegation-packet convention (file paths + CLAUDE.md sections + out-of-scope + expected report items).
- [ ] **Perf audit skill.** Bundle-size + Lighthouse + N+1 + load-test patterns. WDAI-tech-debt-audit workflow but for performance. Owner: Polaris. Scope: S. Trigger: when a project actually complains about perf — don't build it speculatively.
- [ ] **Deep a11y audit skill.** Designer covers a11y basics. A dedicated WCAG 2.1 AA pass with axe/lighthouse/screen-reader testing deserves its own skill. Owner: Designer. Scope: S. Trigger: before any public-facing release.
- [ ] **Post-ship handoff formalization.** "Builder deployed → DevOps smoke test on prod → all-clear report → close out" loop should be a documented workflow, not implicit. Owner: Polaris. Scope: S (doc edit).

### P1 — Agent UX

- [ ] **Proactive meeting prep (Atlas).** Morning brief pre-loads transcripts + wiki pages once at 6:45 AM. A 3 PM meeting gets stale prep if new context surfaced at 10 AM. Proposed: 30-min pre-meeting spawn that re-pulls wiki + last 3 Granola meetings + open threads for attendees. Owner: Atlas. Scope: M.
- [ ] **Close-loop on recurring flags (Atlas).** McKenzie has been in the morning brief for 4+ weeks with the same "close it or reply" nudge. That's noise, not service. Pattern: detect recurring flag, draft the reply/close-out options, put choices in front of Dina. One decision instead of 30 reminders. Owner: Atlas. Scope: M.
- [ ] **Email triage flow (Atlas).** 201 unread isn't signal. Group by sender/topic, batch-summarize non-critical threads, surface only actionables. Owner: Atlas. Scope: M.
- [ ] **Episodic memory index.** Query by time (e.g., "what did we decide on Apr 15?") not just topic. Each daily log gets indexed with key entities, decisions, and a brief abstract at time of write. Owner: shared (Atlas primary). Scope: M.
- [ ] **Auto-wiki-stub for new people.** First time a new attendee appears on the calendar or in an email, Atlas creates a wiki stub at `wiki/people/<slug>.md` with what's known (email, org, meeting context) so Polaris has context if that person later appears in a code commit or PR. Owner: Atlas. Scope: S.

### P2 — Reliability / DevEx

- [ ] **Proper Windows service wrapper for slack-watcher.** Current setup: Startup-folder `.cmd` with internal restart loop. Fine but: (a) doesn't survive a reboot without user logon, (b) no `WakeToRun` from sleep, (c) no log rotation. Either register a Task Scheduler entry with `WakeToRun + StartWhenAvailable` (requires elevated shell) or wrap with `nssm` / `winsw` as a real Windows service. Owner: Polaris. Scope: S (Task Scheduler) or M (service wrapper).
- [ ] **Distill skill short-circuit.** Scheduled distill runs every 2h at :12. Recent pattern: 5+ consecutive no-op distills with no substantive session work to distill. Short-circuit: skill detects empty-session state and exits early, no log entry. Owner: Polaris. Scope: S.
- [ ] **Watcher log rotation.** `watcher.log` grows unbounded. Add size-based rotation (e.g., roll at 5 MB). Owner: Polaris. Scope: S.
- [ ] **Centralize agent runtime state.** Per-agent `.claude/runtime/*.ts` watermarks, scheduled_tasks.lock, and other transient state should live in a single conventional location with cleanup semantics. Today each agent freelances. Owner: shared. Scope: M.

### P2 — Observability

- [ ] **Agent-ecosystem health dashboard.** Single command / page that shows: watcher uptime, last successful spawn per agent, last-seen ts watermarks, Slack bot health, wiki recency, scheduler drift. Goal: know agents are alive without manually checking multiple files. Owner: shared. Scope: M.
- [ ] **Cross-agent incident log.** When something breaks inter-agent (like tonight's self-loop cascade), log the incident + fix pattern so future-us (and future agents) have the debugging trail. Could live at `wiki/infra/incidents.md`. Owner: shared. Scope: S.

### P3 — Architecture

- [ ] **Shared-schema for agents' local state.** Each agent has `identity/memory.md`, `daily-logs/`, `.claude/runtime/`, `.claude/scheduled_tasks.lock`. No formal schema. A `packages/agent-core` npm module (or equivalent) could encode the conventions. Owner: Polaris. Scope: L.
- [ ] **Agent SDK for spawning sub-agents.** Polaris delegates to Builder/Designer/QA via the Agent tool. Atlas doesn't have sub-agents yet. If she grows any, common spawning semantics would help. Owner: Polaris. Scope: L. Trigger: when Atlas wants her first sub-agent.

---

## Done

- ✅ **slack-watcher reliability fixes** (2026-04-19, commits `f07977c` through `4564724`). Process-level handlers, supervisor loop, per-agent bot tokens, Windows spawn gotchas, self-loop fix, user-ID filter removal. 6 distinct bugs. See `wiki/log.md` for full story.
- ✅ **Polaris → Atlas comm-spec expanded** (commit `b10ec73`). Tiered triggers in `infrastructure.md`.
- ✅ **Atlas hourly heartbeat reads #polaris-tl** (commit `fd315d6`). Polling half of real-time bidirectional.
- ✅ **SessionEnd hook for uncommitted-drift detection** (commit `8d439b0`). Runs `git status` at session close.
- ✅ **Branch protection / stalled PR backlog on WDAI** surfaced (Phase 1 audit at `wiki/projects/wdai-tech-debt.md`).

---

## Rules for this doc

- Keep items concrete and ownable — "who + scope + trigger if deferred."
- Mark done with commit SHA so future-us can reconstruct.
- Don't bury architectural rationale here — put that in ADRs or `wiki/infrastructure.md`; this is a prioritized list.
- If an item grows > 3 paragraphs, promote to its own doc and link.
