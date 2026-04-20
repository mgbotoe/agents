---
name: new-app
description: Guided new-app scaffolding workflow following the Agent Swarm Playbook Scenario 2. AUTO-INVOKED when Dina mentions spinning up a new app, starting a new project, scaffolding new, creating new project, new repo, new codebase, bootstrap a project, "let's build X app", "start a new", fresh project. Executes the full architecture → scaffolding → design system → deploy → security baseline sequence.
---

Execute Scenario 2 (New app spin-up) from `wiki/projects/agent-swarm-playbook.md`.

## Before starting

Confirm with Dina:
- Target workspace (`Personal Projects`, `Webdesign Business`, or new workspace?)
- App name / purpose
- Any stack constraints (e.g., "must be Next.js" vs "you pick")
- Deploy target preference (Vercel, self-hosted, static, Task Scheduler for local, etc.)
- Data classification if known (public-only, user-scoped, PII, payment)

Create a task list with `TaskCreate` covering all 7 phases.

## Steps

**Phase 1 — Architecture (me, as Polaris).**
1. Stack selection. Consider: solo-dev, AI-native collaboration, scale target, existing patterns in Dina's other projects.
2. Document each major choice as an ADR at `docs/adr/001-stack.md` (or whatever the project convention becomes).
3. Skills assessment using the template in user's global `CLAUDE.md`. Decide which auto-invoke skills apply.
4. Initialize the repo: directory structure, `.gitignore` (honest scope), initial commit.
5. **Write the project's `CLAUDE.md`.** Stack, conventions, critical patterns, testing, deploy target, per-project agent delegation rules. Save it BEFORE spawning any sub-agent — they need it.

**Phase 2 — Base scaffolding (Builder).**
Spawn Builder with:
```
**Task:** scaffold <project name> per CLAUDE.md spec
**Stack:** <explicit list>
**Acceptance:** project compiles clean, linter passes, test harness runs empty test, one-command dev mode works
**Out of scope:** any features — this is skeleton only
**CLAUDE.md:** <path>
```

**Phase 3 — Design system (Designer) [if UI app].**
Skip if it's a CLI/API-only project.
```
**Task:** establish initial design tokens + component primitives
**Tokens:** colors, type scale, spacing, radii, shadows
**Primitives:** Button, Input, Card, Modal (or equivalent MVP)
**Reference:** design preferences from CLAUDE.md; aesthetic direction from Dina
```
Save output to `.claude/tmp/artifacts/<date>/<slug>/design-system.md`.

**Phase 4 — DevOps baseline (DevOps).**
```
**Task:** set up deploy pipeline + observability baseline
**Deploy target:** <Vercel / Netlify / Cloudflare / self-hosted / Task Scheduler / etc.>
**Observability minimums:** error tracking, deploy logs, uptime signal
**Env vars:** list of required secrets (documented in README, NOT in repo)
**Alert thresholds:** what triggers a ping
**Rollback procedure:** documented
```

**Phase 5 — Security baseline (Security).**
```
**Task:** establish security posture for <project>
**Data classification:** <public / user-scoped / PII / payment / health>
**Compliance commitments:** <GDPR / CCPA / HIPAA / PCI / none>
**Auth model:** <from Phase 1>
**Initial threat surfaces:** auth flow, public APIs, admin routes, third-party integrations
```

**Phase 6 — First feature.**
Hand off to `/feature-dev` skill (Scenario 1). By now the foundation is in place.

**Phase 7 — Wrap.**
1. Update `wiki/index.md` + `wiki/projects/` with a project page (if persistent project worth tracking).
2. Update hot memory with pointer.
3. First commit + push per the push rules.

## Handoff discipline

- Each phase has a durable artifact (CLAUDE.md, ADR, design system, deploy pipeline, threat model). None live in chat only.
- Skip UI-only phases for non-UI projects; skip payment-specific security review for non-payment apps.
- Don't combine phases. Each phase has a distinct output and success criterion.

## When this skill should NOT fire

- Adding a feature to an existing app (`/feature-dev` instead)
- Forking an existing app (that's a migration, different flow)
- Creating a one-off script or gist (just write it)
