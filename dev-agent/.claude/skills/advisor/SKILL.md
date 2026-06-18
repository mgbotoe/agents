---
name: advisor
description: Outside-read pressure-test BEFORE committing to an architectural approach. Spawns an independent fork subagent to attack your premises adversarially. Use when any advisor() trigger in rules/personal.md fires — schema/auth/payments/new-service/cross-repo changes, hard-to-reverse infra, plans touching >3 files in unfamiliar code, or executing Dina's framing without an independent technical opinion. Cross-platform (uses the built-in fork subagent, no external CLI).
---

# Advisor — outside read before you commit

The `advisor()` rule (`rules/personal.md`, `SOUL.md`) is mandatory but has no
forcing mechanism — it relies on you noticing. This skill is the *worker* that
does the read; the `context-injector` hook surfaces `[EXISTING DECISION?]` and
the prior-art markers that should trigger you to invoke it. Call it BEFORE the
plan crystallizes — after you've written the plan, you've already anchored.

## When to invoke (any one fires)
- Schema / data-model change; auth / authz / payments / webhooks / admin surfaces
- New service, integration, queue, cron, or sync↔async choice
- Hard-to-reverse infra (DB engine, platform, framework, ORM, language)
- Cross-repo / cross-workspace changes
- Plan touches >3 files in unfamiliar code
- You're executing Dina's framing without an independent technical opinion
- A `[EXISTING DECISION?]` or `[PRIOR ART CHECK PENDING]` marker fired this turn

NOT for: bug fixes <20 lines, single-file edits in known patterns, code review,
or following an existing ADR's prescribed pattern.

## How to run it
Spawn a `fork` subagent (inherits your full transcript, so it sees the real
problem — not a summary you'd bias). Give it this contract:

> You are my advisor — an adversarial outside read with my full transcript. Attack
> the premises of the approach I'm about to commit to, not the polish.
> 1. **SDK baseline first** (mandatory per feedback_claude_agent_sdk_blind_spot):
>    what does the Claude Agent SDK / Claude Code natively offer for this? Am I
>    hand-rolling a shipped primitive? Cite specifics.
> 2. **Wrong premises (2–3):** where is this design fooling itself?
> 3. **Verdict:** proceed-as-is / proceed-with-changes / reconsider.
> 4. **Single highest-risk item.**
> Be terse, bullets, no preamble. If "the simple thing is fine / the SDK already
> does this," say so.

Use `Agent` with `subagent_type: "fork"`. For non-agent-architecture decisions,
drop the SDK-baseline line.

## Acting on the verdict
- **proceed-as-is** → proceed; cite the confirmation in the plan/ADR (auditable).
- **proceed-with-changes** → adopt the changes; note what you changed and why.
- **reconsider** → do NOT silently switch. Surface the conflict to Dina with both
  reads. If running unattended, STOP and leave it for her.

Verifying the advisor's own claims is still your job — it can be wrong about
library/tool semantics (e.g. it suggested `os.kill(pid,0)` for liveness, which
is a Windows footgun). Check load-bearing claims against docs before adopting.
