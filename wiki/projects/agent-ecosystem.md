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

- ✅ **DevOps sub-agent created** — shipped 2026-04-19. `dev-agent/.claude/agents/devops.md`. Owns post-deploy monitoring, incident response, dep maintenance, release coordination. Closes DevOps/SRE/Dep-maintenance gaps. Does NOT write feature code (Builder's lane). **Note:** sub-agent form is transitional — see P2 promotion triggers for eventual move to standalone.
- ✅ **Designer unblocked for direct Builder delegation** — Designer config now has `Agent` tool. Routine "implement what I designed" handoffs skip the Polaris middle-man.
- ✅ **Delegation protocol expanded** — `CLAUDE.md` now documents shift-left pattern (parallel Builder + QA for complex features), security-sensitive tag (threat model before, pen-test after), and delegation-packet convention (file paths + CLAUDE.md sections + out-of-scope + expected report items).
- ✅ **Security sub-agent created** — shipped 2026-04-19. `dev-agent/.claude/agents/security.md`. Owns threat modeling, OWASP reviews, auth/authz, secrets audits, CVE triage, compliance. Does NOT write feature code (Builder's lane). Fills the general-OWASP gap that `ai-guardrails-audit` skill (AI-specific) left open. Quarterly audit workflow documented.
- [ ] **Perf audit skill.** Bundle-size + Lighthouse + N+1 + load-test patterns. WDAI-tech-debt-audit workflow but for performance. Owner: Polaris. Scope: S. Trigger: when a project actually complains about perf — don't build it speculatively.
- [ ] **Deep a11y audit skill.** Designer covers a11y basics. A dedicated WCAG 2.1 AA pass with axe/lighthouse/screen-reader testing deserves its own skill. Owner: Designer. Scope: S. Trigger: before any public-facing release.
- [ ] **Post-ship handoff formalization.** "Builder deployed → DevOps smoke test on prod → all-clear report → close out" loop should be a documented workflow, not implicit. Owner: Polaris. Scope: S (doc edit).

### P1 — Agent UX

- [ ] **Proactive meeting prep (Atlas).** Morning brief pre-loads transcripts + wiki pages once at 6:45 AM. A 3 PM meeting gets stale prep if new context surfaced at 10 AM. Proposed: 30-min pre-meeting spawn that re-pulls wiki + last 3 Granola meetings + open threads for attendees. Owner: Atlas. Scope: M.
- [ ] **Close-loop on recurring flags (Atlas).** McKenzie has been in the morning brief for 4+ weeks with the same "close it or reply" nudge. That's noise, not service. Pattern: detect recurring flag, draft the reply/close-out options, put choices in front of Dina. One decision instead of 30 reminders. Owner: Atlas. Scope: M.
- [ ] **Email triage flow (Atlas).** 201 unread isn't signal. Group by sender/topic, batch-summarize non-critical threads, surface only actionables. Owner: Atlas. Scope: M.
- [ ] **Episodic memory index.** Query by time (e.g., "what did we decide on Apr 15?") not just topic. Each daily log gets indexed with key entities, decisions, and a brief abstract at time of write. Owner: shared (Atlas primary). Scope: M.
- [ ] **Auto-wiki-stub for new people.** First time a new attendee appears on the calendar or in an email, Atlas creates a wiki stub at `wiki/people/<slug>.md` with what's known (email, org, meeting context) so Polaris has context if that person later appears in a code commit or PR. Owner: Atlas. Scope: S.

### P1 — New standalone agents (Dina's career stack)

Scoped to advance healthtech leadership + DHA. Ordered by leverage.

- [ ] **Research/Analyst agent ("Orion" or TBD).** Outward-facing signal filter: healthtech + AI market intel, competitive scans, DHA field reading, opportunity radar. Own scheduler (daily scan + weekly digest), own memory, own Slack channel. Offloads market awareness from Atlas so CoS stays in-the-moment. Trigger: now — Dina's north star is healthtech leadership; she needs a dedicated signal layer. Owner: Atlas to scaffold + Dina to approve. Scope: M.
- [ ] **Scholar/Tutor agent (DHA companion).** Inward-facing learning accelerator: ingests syllabi + readings, Socratic quizzing, flashcard generation from dense papers, drafts discussion posts in Dina's voice, tracks DHA deadlines against Atlas calendar. Different from Research (market intel) — this is coursework depth. Trigger: DHA program start. Owner: Atlas to scaffold. Scope: M.
- [ ] **Writer/Ghostwriter agent.** LinkedIn thought leadership, WSJ-track content, DHA paper drafting — all in Dina's voice (reuse voice profile from `/draft-email`). Cross-pollinates: DHA capstone → articles → positioning. Compounds career capital. Trigger: after Research + Scholar stand up (needs their output as source material). Owner: Atlas to scaffold. Scope: M.

Deferred / considered-and-skipped:
- **WDAI Ops agent** — Atlas covers it; promote only if WDAI volunteer coordination becomes its own workstream.
- **Finance agent** — tax engine already covers it.
- **Life/Health agent** — Atlas's lane; no split.

### P2 — Sub-agent → standalone promotion

Sub-agent vs standalone is a **scale question**, not a function question. Continuous functions with event arrival ≥ daily benefit from own identity + scheduler + memory. Scoped functions that run in response to Polaris-led tasks are fine as sub-agents. The original "they operate within Polaris-led tasks, so stay sub-agents" reasoning was circular and got pressure-tested out.

**Promotion triggers (document now, execute when triggered):**

| Agent | Promote when |
|---|---|
| **DevOps** | **Strongest near-term candidate.** Promote at the first real SLA commitment OR when post-deploy watch becomes a recurring ask. Agent infra alone (watcher liveness, scheduled tasks health, log rotation, dep bumps across agent repos, incident response when watcher dies — see Apr 19's 25-hour outage) already has enough continuous work to justify it. Current sub-agent only runs when Polaris spawns; infra sits un-watched in between. |
| **Security** | Any project handles payment/PII at scale, OR ≥ 2 prod systems need continuous CVE monitoring, OR compliance regime requires documented quarterly audit cadence. |
| **QA** | Test-infra drift (flaky test triage, test-env management, regression over time) becomes its own workstream independent of feature work. |
| **Builder** | Probably never. Implementation should stay coupled to architecture decisions (Polaris's lane). |
| **Designer** | Multiple public-facing production sites needing continuous design-system evolution. |

- [ ] **Promote DevOps to standalone.** Would parallel Atlas + Polaris. New Slack channel (#devops-ops), own scheduler (30-min heartbeat checks: watcher alive? scheduled tasks fired? deps current? recent alerts?), own memory, own CLAUDE.md. Trigger: any of the above conditions hit. Owner: Polaris to design + Dina to approve. Scope: M (2-3 hour session to scaffold).

### P2 — Reliability / DevEx

- [ ] **Proper Windows service wrapper for slack-watcher.** Current setup: Startup-folder `.cmd` with internal restart loop. Fine but: (a) doesn't survive a reboot without user logon, (b) no `WakeToRun` from sleep, (c) no log rotation. Either register a Task Scheduler entry with `WakeToRun + StartWhenAvailable` (requires elevated shell) or wrap with `nssm` / `winsw` as a real Windows service. Owner: Polaris. Scope: S (Task Scheduler) or M (service wrapper).
- [ ] **Distill skill short-circuit.** Scheduled distill runs every 2h at :12. Recent pattern: 5+ consecutive no-op distills with no substantive session work to distill. Short-circuit: skill detects empty-session state and exits early, no log entry. Owner: Polaris. Scope: S.
- [ ] **Watcher log rotation.** `watcher.log` grows unbounded. Add size-based rotation (e.g., roll at 5 MB). Owner: Polaris. Scope: S.
- [ ] **Centralize agent runtime state.** Per-agent `.claude/runtime/*.ts` watermarks, scheduled_tasks.lock, and other transient state should live in a single conventional location with cleanup semantics. Today each agent freelances. Owner: shared. Scope: M.

### P2 — Observability

- [ ] **Agent-ecosystem health dashboard.** Single command / page that shows: watcher uptime, last successful spawn per agent, last-seen ts watermarks, Slack bot health, wiki recency, scheduler drift. Goal: know agents are alive without manually checking multiple files. Owner: shared. Scope: M.
- [ ] **Cross-agent incident log.** When something breaks inter-agent (like tonight's self-loop cascade), log the incident + fix pattern so future-us (and future agents) have the debugging trail. Could live at `wiki/infra/incidents.md`. Owner: shared. Scope: S.

### P3 — Agent Intelligence

- [ ] **Fully autonomous skill lifecycle (no guardrails).** Current state: agents can *propose* new skills (3+ recurrence trigger) and *flag* deletions — both require Dina confirmation. Hermes-style full autonomy means agents create + delete without asking, guided only by trigger criteria. Prerequisite: 6 months of log data on proposal quality to verify the trigger criteria are tight enough before removing the human checkpoint. Owner: shared (Atlas primary). Scope: S when triggered. **Target: ~Nov 2026.** Note: guardrailed version (propose + confirm) is live as of 2026-05-03 in `self-improve` skill across all 3 agents.

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
