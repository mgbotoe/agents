---
name: post-ship-watch
description: Post-deployment watchdog workflow following Agent Swarm Playbook Scenario 5. AUTO-INVOKED when Dina mentions just deployed, just shipped, merged to main, deploy is out, pushed to production, went live, shipped to prod, deploy complete, after deploy, post-deploy, is it up. Formalizes the Builder → DevOps handoff so every deploy gets watched instead of trust-falling.
---

Execute Scenario 5 (Post-ship watch) from `wiki/projects/agent-swarm-playbook.md`.

## When this fires

Any time code has been deployed to an environment Dina cares about:
- Vercel prod deploy
- Self-hosted app restart after push
- Agent infra changes that went live (e.g., watcher restart, scheduler change)
- Static site rebuild
- Cron job activation

Applies whether deploy was manual or via CI.

## Steps

**Phase 1 — Classify the deploy.**
1. What shipped? (feature / fix / config / dep bump / infra)
2. Blast radius? (one user-facing feature / whole site / background service)
3. Traffic profile? (high / low / agent-only)
4. Window length? 15 min for low-traffic or infra-only; 30-60 min for user-facing; 60+ for payment/auth changes
5. Rollback command ready? (MUST exist before watch starts)

**Phase 2 — Delegate to DevOps.**
Spawn DevOps:
```
**Task:** post-ship watch on <what shipped>
**Commit:** <SHA>
**Deploy target:** <Vercel / self-hosted / etc.>
**Window:** <15 / 30 / 60 min>
**Baseline comparison:** prior 24h same window
**Signals to pull:**
  - Error rate (Sentry if available, else Vercel logs)
  - Latency (p50, p95, p99)
  - Throughput (requests/min)
  - Deploy logs (build warnings, runtime errors in first N min)
  - Any alerts triggered
**Rollback command:** <one-line>
**Save report to:** .claude/tmp/artifacts/<date>/<slug>/post-ship-watch.md
**Expected report:** healthy / degraded / incident (with evidence)
```

**Phase 3 — Wait for DevOps report.**
While DevOps watches, I (Polaris):
- Stay accessible if DevOps needs help interpreting a signal
- Don't start new substantive work on the same project (context switch risk)
- Can work on unrelated projects

**Phase 4 — Triage DevOps report.**

**If healthy:**
- Close the task list
- Note in hot memory: "Shipped <feature>, post-ship clean"
- Update wiki/log.md if deploy was notable
- Done.

**If degraded:**
- DevOps identifies the degradation
- I (Polaris) decide: roll back now, patch forward, or monitor longer
- If rolling back: DevOps executes rollback command, I spawn Builder for the fix
- If patching forward: Builder + new deploy + `/post-ship-watch` again on the patch

**If incident:**
- DevOps rolls back IMMEDIATELY (rollback is cheap; debugging a bad prod is not)
- I take incident lead:
  - Notify Dina if user-impacting
  - Spawn Security if breach suspected
  - Start postmortem draft at `.claude/tmp/artifacts/<date>/<slug>/postmortem.md`
- Spawn Builder for root-cause fix
- After fix: `/security-sensitive` (if the incident had a security dimension) or `/feature-dev` re-ship

**Phase 5 — Close the loop.**
1. Artifact saved to `.claude/tmp/artifacts/<date>/<slug>/post-ship-watch.md`
2. If incident: postmortem is a first-class doc, linked from wiki/log.md
3. Feed learnings back: anything that caused this regression → add to DevOps's pre-deploy checklist for next time

## What NOT to skip

- **Rollback command.** If nobody knows how to undo this deploy, the watch is theater.
- **Baseline comparison.** "Errors are up" only matters against a baseline. DevOps pulls 24h prior same window.
- **Window length scaled to stakes.** Auth/payment changes need 60+ min. Don't close early.
- **Silent health is the norm.** Don't chat for the sake of updates. DevOps reports once at window close OR immediately if incident.

## When this skill should NOT fire

- Local dev changes (not a deploy)
- Feature-branch pushes (not user-facing yet)
- Dep-bump PRs not yet merged
- Draft PRs
