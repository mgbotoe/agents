---
name: feature-dev
description: Guided feature implementation workflow following the Agent Swarm Playbook Scenario 1. AUTO-INVOKED when Dina mentions implementing a feature, building a feature, adding a feature, shipping X, "let's build", "let's add", "new functionality", "can you add", feature request, enhancement, new capability. Executes the full Polaris → sub-agent delegation sequence with phase gates so the playbook actually gets followed instead of improvised.
---

Execute Scenario 1 (Feature dev in existing project) from `wiki/projects/agent-swarm-playbook.md`. The playbook is the spec; this skill is the executor.

## Before starting — make sure you understand

Ask yourself: did Dina actually describe a feature? If she said "fix a typo" or "look at this bug," that's probably NOT a feature — it's a quick fix (`< 20 lines`, do it yourself per the "When NOT to delegate" rule). Only run this skill for actual features that warrant the swarm.

If ambiguous, ask Dina one clarifying question before executing.

## Steps

**Phase 0 — Classify.** Determine:
- Target project (which workspace / repo)
- **Security-sensitive?** (auth, payments, credentials, PII, webhooks, admin routes → YES)
- **UI-bearing?** (new screen, component, interaction → YES)
- **Complex?** (>1 day of work, tricky edge cases, shift-left worth it → YES)

Create a task list with `TaskCreate` covering the phases that apply. Skip phases that don't.

**Phase 1 — Scope (me, as Polaris).**
1. Read target repo's `CLAUDE.md` end-to-end.
2. Write a feature brief: description, acceptance criteria, in-scope, out-of-scope.
3. Save the brief to `.claude/tmp/artifacts/<date>/<slug>/brief.md` so it's durable — not just in my head.

**Phase 2 — Pre-work (parallel, only what applies).**
Spawn in parallel (single message, multiple Agent calls):
- **Security** if security-sensitive → threat model → save to `.claude/tmp/artifacts/<date>/<slug>/threat-model.md`
- **Designer** if UI-bearing → component specs → save to `.claude/tmp/artifacts/<date>/<slug>/design.md`
- **QA** if complex and shift-left worth it → test plan → save to `.claude/tmp/artifacts/<date>/<slug>/test-plan.md`

If none apply, skip directly to Phase 3.

**Phase 3 — Implementation (Builder).**
Spawn Builder with the delegation packet format. Include:
```
**Task:** <feature brief content>
**Scope:** <exact file paths>
**Out of scope:** <what NOT to do>
**CLAUDE.md sections to apply:** <cited headings from target repo>
**Upstream artifacts:** <paths to brief + threat-model + design + test-plan>
**Trade-offs already ruled out:** <decisions not to re-litigate>
**Expected report:** per Builder's report-back format (include CLAUDE.md citation)
```

**Phase 4 — Review (me).**
1. Read Builder's diff.
2. Verify CLAUDE.md citations match real headings.
3. Check architecture fit, correctness, maintainability.
4. If security-sensitive → spawn **Security** for post-impl review → save findings to `.claude/tmp/artifacts/<date>/<slug>/security-review.md`.
5. If findings exist: bounce to Builder with specifics (file:line + rationale). Loop until clean.

**Phase 5 — Testing (QA).**
Spawn QA with:
```
**Spec:** <brief content>
**Diff:** <Builder's changes>
**Test plan (if shift-left):** <path to QA's earlier plan>
**Focus areas:** <risk surfaces from brief>
```
If QA finds critical/high → back to Builder. Repeat Phases 3-5 until clean.

**Phase 6 — Ship (Builder + DevOps).**
1. Confirm commit strategy with Dina (explicit per-push OK required for master/main).
2. Builder commits + pushes.
3. Builder deploys (if deploy is part of the feature scope).
4. Spawn **DevOps** for post-ship watchdog with:
```
**Deploy:** <what shipped, when>
**Window:** <15 min low-traffic / 30-60 min higher>
**Focus:** <new attack surfaces / new monitoring thresholds>
**Rollback command:** <one-line>
```

**Phase 7 — Done.**
1. DevOps reports healthy/degraded/incident.
2. If healthy: close task list, update hot memory with a one-liner, optionally add wiki log entry.
3. If degraded/incident: escalate to me as lead, coordinate fix.

## Handoff discipline

- **Artifacts are files, not chat.** Every phase output lives at `.claude/tmp/artifacts/<date>/<slug>/` as markdown.
- **Delegation packets use the template above.** Don't cold-prompt sub-agents.
- **CLAUDE.md citations mandatory.** Sub-agent report without citations = bounce back.
- **Task list drives progress.** Mark phases complete; don't advance without artifact in place.

## When this skill should NOT fire

- Bug fixes under 20 lines (do yourself)
- Refactors with no functional change (`/simplify` is the right tool)
- Copy/text edits
- Dependency bumps (DevOps lane)
- "Just quickly look at this" style asks

If you're unsure, ask Dina: "Is this a feature (full swarm flow) or a quick fix (I do it directly)?"
