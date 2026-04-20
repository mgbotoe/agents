# Agent Swarm Playbook

**Living document.** Concrete workflows for how Polaris + sub-agents coordinate on real work. If you want to know "how does the swarm actually dance on X," this is where to look.

Companion to [[projects/agent-ecosystem|Agent Ecosystem Roadmap]] (which tracks gaps + future work) and `dev-agent/CLAUDE.md` (which defines roles).

---

## The swarm, in one diagram

```
                       ┌─────────────┐
                       │    DINA     │   (the boss)
                       └──────┬──────┘
                              │  scopes work
                              ▼
                       ┌─────────────┐
         ┌─────────────│   POLARIS   │─────────────┐
         │             │  Tech Lead  │             │
         │             └──┬───────┬──┘             │
         │                │       │                │
    delegates         delegates  delegates      delegates
         │                │       │                │
         ▼                ▼       ▼                ▼
  ┌──────────┐     ┌──────────┐ ┌─────┐    ┌──────────┐
  │ DESIGNER │◄───►│ BUILDER  │ │ QA  │    │ SECURITY │
  └──────────┘     └────┬─────┘ └─────┘    └──────────┘
  (can spawn              │                       │
   Builder for                                    │
   impl handoff)                                  │
                         │                        │
                         ▼                        │
                    ┌──────────┐                  │
                    │  DEVOPS  │◄─────────────────┘
                    └──────────┘
                    (post-deploy watch,
                     incident response,
                     dep triage)
```

**Who reports to whom:**
- All sub-agents report back to Polaris (structured format per their config).
- Designer can spawn Builder directly for "implement this design" handoffs.
- Builder can spawn other Builder sessions for parallel subtasks.
- QA and Security don't spawn others (they report findings, Polaris routes fixes).
- DevOps can spawn Builder for hotfix work during incident response.

---

## Scenario 1 — Implementing a feature in an existing project

**When to use this playbook:** you're adding a new feature, enhancement, or non-trivial change to a project that already exists.

### Phase 1 — Scope (Polaris)
1. Read target repo's `CLAUDE.md` end-to-end
2. Write a **feature brief**: description, acceptance criteria, in-scope, out-of-scope
3. Classify:
   - Is it **security-sensitive**? (touches auth, payments, credentials, PII, webhooks, admin routes)
   - Is it **UI-bearing**? (new screen, component, interaction)
   - Is it **complex enough for shift-left**? (>1 day of work, tricky edge cases)
4. Identify open questions → ask Dina OR decide + document ADR

### Phase 2 — Pre-work (parallel where possible)

| If... | Delegate to | Packet includes |
|---|---|---|
| Security-sensitive | **Security** (threat model) | feature brief + relevant CLAUDE.md sections + auth/data model context |
| UI-bearing | **Designer** (component design) | feature brief + existing component inventory + design-language notes from CLAUDE.md |
| Complex | **QA** (test plan, in parallel with Builder) | feature brief + acceptance criteria + risk areas |

**What comes back:**
- Security: attack vectors + required mitigations + residual risk
- Designer: component specs / mockups / prop contracts
- QA: test plan ready to run when Builder's code lands

### Phase 3 — Implementation (Builder)

**Polaris's delegation packet:**
```
**Task:** <feature brief>
**Scope:** <files to touch — exact paths>
**Out of scope:** <what NOT to do>
**CLAUDE.md sections already identified:** <cite headings>
**Upstream work:** <Designer output / Security threat model attached>
**Trade-offs already ruled out:** <what decisions not to re-litigate>
**Expected report:** <what Builder reports back>
```

**Builder's job:**
- Read target CLAUDE.md end-to-end (blocking requirement)
- Implement, write tests during, document as they go
- Report back in structured format with **CLAUDE.md sections cited**

### Phase 4 — Review (Polaris)

1. Read Builder's diff
2. Check: architecture fit, correctness, maintainability, CLAUDE.md citations real
3. If security-sensitive → delegate **post-impl review to Security** (pen-test mindset)
4. If findings: bounce to Builder with specifics. Not "fix this" but "at X:Y, the pattern should be Z because [reason]"

### Phase 5 — Testing (QA)

**Polaris's delegation packet:**
```
**Spec:** <feature brief + acceptance criteria>
**Diff:** <Builder's changes>
**Test plan (if shift-left):** <QA's earlier plan>
**Focus areas:** <risk surfaces>
```

**QA's job:**
- Happy path first, then edge cases, then regression sweep
- Report bugs with severity + repro steps OR clear-to-ship

**If QA finds critical/high:** back to Builder with repro. Repeat phases 3-5.

### Phase 6 — Ship (Builder + DevOps)

1. Builder commits + pushes (per-push authorization rules apply)
2. Polaris approves deploy
3. Builder deploys
4. **DevOps watchdog** kicks in:
   - Pulls last 15-60 min of error rates, deploy logs, latency
   - Reports: healthy / degraded / incident
   - If regression: **rollback immediately** + notify Polaris

### Phase 7 — Done

- Feature merged to main + deployed
- Post-deploy window clean
- Polaris updates memory / wiki log
- Any carry-over items → next session or roadmap

---

## Scenario 2 — Spinning up a new app

**When to use this playbook:** starting a fresh project in a new or existing workspace.

### Phase 1 — Architecture (Polaris)

1. **Stack selection.** Decide: framework, language, data store, auth, hosting. Consider constraints — solo-dev, AI-native, scale target. Document each major choice as an ADR.
2. **Skills assessment** (per the template in user's global `CLAUDE.md`): which sub-agents + skills apply to this project? Decide which auto-invoke.
3. **Initialize the repo.** Create baseline directory structure, `.gitignore` (honest scope — not overbroad), `package.json` / `pyproject.toml` / `go.mod` / etc. First commit.
4. **Write the project's CLAUDE.md.** Stack, conventions, critical patterns, testing approach, deploy target, agent delegation rules specific to this project.

### Phase 2 — Base scaffolding (Builder)

**Delegation packet:**
```
**Task:** scaffold <project name> per CLAUDE.md spec
**Stack:** <explicit list — don't assume>
**Acceptance:** project compiles clean, linter passes, test harness runs empty test, one-command dev mode works
**Out of scope:** any features — this is skeleton only
```

**Builder returns:** working skeleton, build/lint/test/dev commands confirmed.

### Phase 3 — Design system (Designer) [if UI app]

**Delegation packet:**
```
**Task:** establish initial design tokens + component primitives
**Tokens:** colors, type scale, spacing, radii, shadows — enough to build against
**Primitives:** Button, Input, Card, Modal (or equivalent) — project's MVP UI vocabulary
**Reference:** any design-language preferences from CLAUDE.md; aesthetic direction from Dina
```

**Designer returns:** tokens file + MVP component library + usage examples.

### Phase 4 — DevOps baseline (DevOps)

**Delegation packet:**
```
**Task:** set up deploy pipeline + observability baseline for <project>
**Deploy target:** <Vercel / Netlify / Cloudflare / self-hosted / Task Scheduler / etc.>
**Observability minimums:** error tracking (Sentry or equivalent), deploy logs, uptime signal
**Env vars:** list of required secrets (document in README, not in repo)
**Alert thresholds:** what triggers a ping
```

**DevOps returns:** working deploy pipeline, monitoring live, alerting configured, rollback procedure documented.

### Phase 5 — Security baseline (Security)

**Delegation packet:**
```
**Task:** establish security posture for <project>
**Data classification:** <public / user-scoped / PII / payment / health>
**Compliance commitments:** <GDPR / CCPA / HIPAA / PCI / none>
**Auth model:** <decided in Phase 1>
**Initial threat surfaces to review:** auth flow, any public APIs, admin routes, third-party integrations
```

**Security returns:** initial threat model, baseline OWASP posture check, required setup (rate limits, CORS, headers, secrets handling).

### Phase 6 — First feature

Follow [Scenario 1 playbook](#scenario-1--implementing-a-feature-in-an-existing-project). By now: scaffolding, design system, deploy, and security baseline are all in place. Features land on a working foundation.

### Phase 7 — Done (with the app; scenario 1 repeats for each feature thereafter)

---

## Scenario 3 — Bug fix (< 20 lines of code)

**Polaris does it alone.** No delegation. Per the "When NOT to delegate" rule in `CLAUDE.md`. Quick bug fixes don't benefit from the swarm — orchestration overhead exceeds the work.

- Exception: if the bug is security-sensitive, delegate to Security for post-fix review.

---

## Scenario 4 — Security-sensitive change

Use Scenario 1 but with the **security-sensitive tag** active from the start:

1. Polaris scopes + flags security-sensitive
2. **Security** (threat model BEFORE Builder) — returns attack vectors + mitigations
3. Polaris adds threat model to Builder's packet
4. Builder implements with defenses baked in
5. Builder finishes
6. **Security** (post-impl review) — pen-test mindset review
7. If findings critical/high → bounce to Builder, repeat 4-6
8. Polaris makes ship/no-ship call
9. **DevOps** wires specific monitoring for the new attack surface

---

## Scenario 5 — Post-ship watch (deploy → all-clear)

Formalizing the post-ship handoff (currently implicit):

1. Builder reports: "deploy shipped at <time>"
2. Polaris delegates to **DevOps** with watch window (15 min for low-traffic, 60+ for higher)
3. DevOps pulls signals (errors, latency, deploy logs, any alerts)
4. DevOps reports at window end: healthy / degraded / incident
5. If incident → rollback immediately (rollback is cheap; debugging a bad prod isn't) → Polaris takes incident lead
6. If healthy → close the loop, Polaris notes in memory/wiki log

---

## Handoff Artifacts — what each agent leaves for the next

When one sub-agent's output feeds another, the artifact needs to be durable + addressable, not just "Polaris knows from the prior report."

| Handoff | Artifact |
|---|---|
| Designer → Builder | Design file path (Figma/markdown/component spec) + prop contracts in a doc, not chat |
| Security → Builder | Threat model markdown (attack vectors + mitigations table), referenced in Builder's packet |
| Builder → QA | Diff + test plan (QA's earlier plan if shift-left) + file:line notes for Builder's "concerns" |
| QA → Builder (bugs found) | Structured bug report: severity, repro steps, expected vs actual, files touched |
| Builder → DevOps | Deploy summary: what shipped, what monitoring to watch, rollback command |
| DevOps → Polaris (incident) | Severity, impact, trigger, contained, fix status, postmortem link |

**Rule:** if an artifact only lives in Polaris's head, the handoff is fragile. Durable artifacts let sub-agents pick up context without Polaris re-briefing.

---

## Parallel Delegation Rules

When multiple sub-agents work concurrently:

1. **Clear ownership per artifact.** If Designer and Builder are both working, Designer owns the design file, Builder owns the code. No overlap on who writes what.
2. **Merge happens at Polaris.** Parallel outputs converge at my review. I resolve conflicts, not the sub-agents.
3. **No upstream waits.** If Builder is blocked on Designer's output, either (a) start with what's known, (b) block at Polaris, don't have Builder wait on Designer directly.
4. **Shift-left specifically:** Builder + QA in parallel. QA writes test plan against acceptance criteria while Builder codes. Test plan is ready when code lands.

---

## Escalation Paths

**Sub-agents escalate to Polaris when:**
- They hit a decision that crosses their scope boundary (Builder hits architecture, Designer hits backend, QA finds something outside the tested scope)
- They find a blocker they can't resolve with their tools
- Something contradicts their CLAUDE.md reading

**Polaris escalates to Dina when:**
- Security-sensitive decision with user-impact trade-off
- Money / external commitments
- Anything crossing `.claude/rules/` boundaries
- Production incident requiring user communication
- Cross-project scope change (e.g., "this WDAI work also affects personal project X")

**Atlas → Polaris handoffs** covered in `infrastructure.md` (separate doc).

---

## Log

- **2026-04-19 (Polaris)** — Playbook created. Covers feature dev, new app, bug fix, security-sensitive, post-ship watch. Handoff artifacts + parallel rules + escalation documented.
