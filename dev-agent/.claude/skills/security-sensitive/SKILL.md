---
name: security-sensitive
description: Security-sensitive change workflow following Agent Swarm Playbook Scenario 4. AUTO-INVOKED when Dina mentions auth flow, login, signup, password reset, payment integration, Stripe, Clerk, admin route, webhook handler, API key, credentials, PII, personal data, secrets, OAuth, tokens, user data, encryption, security review, threat model. Adds threat-model-before-impl and pen-test-mindset post-impl passes to the normal feature-dev flow.
---

Execute Scenario 4 (Security-sensitive change) from `wiki/projects/agent-swarm-playbook.md`.

This is NOT a replacement for `/feature-dev` — it's `/feature-dev` with the security-sensitive tag active from the start. The phases are the same; the difference is Security sub-agent is mandatory in Phases 2 and 4 (instead of optional).

## Before starting

Confirm scope:
- Is this a new feature that touches security? → run `/feature-dev` and this skill together (this skill's guidance overrides where they conflict)
- Is this a security audit of existing code? → don't use this skill; use `/security-review` (branch-level review) or delegate to Security sub-agent directly for an audit
- Is this a security-sensitive bug fix? → delegate to Security for triage first, then route the fix

## Steps (delta vs /feature-dev)

**Phase 0 — Classify (always).** Confirm the security-sensitive trigger is genuine:
- Touches auth / session management / identity
- Handles payment flows or payment credentials
- Stores, processes, or transmits PII / health / financial data
- Exposes admin-only functionality
- Accepts webhooks from external systems
- Manages secrets, credentials, tokens, or API keys
- Handles file uploads or user-generated content that's rendered as HTML

If yes → this skill stays active. If no → standard `/feature-dev` flow is enough.

**Phase 1 — Scope.** Same as `/feature-dev`, with additional capture:
- Data classification (what's the blast radius if this goes wrong?)
- Regulatory scope (GDPR user data? PCI cardholder data? HIPAA PHI?)
- Pre-existing threats (what attacks is this system already mitigating?)

Save brief to `.claude/tmp/artifacts/<date>/<slug>/brief.md`.

**Phase 2 — MANDATORY Threat Model (Security).**
Spawn Security sub-agent:
```
**Task:** threat model for <feature>
**Scope:** <files / routes / data flows involved>
**Data classification:** <from Phase 1>
**Compliance scope:** <from Phase 1>
**CLAUDE.md sections to reference:** Security Checklist, Auth, Webhook Idempotency, etc.
**Expected output:** attack vectors table + mitigations + residual risk
**Save to:** .claude/tmp/artifacts/<date>/<slug>/threat-model.md
```

Wait for threat model before proceeding. **Do not delegate to Builder without it.**

**Phase 3 — Implementation (Builder).**
Delegation packet includes the threat model as primary context:
```
**Task:** <feature brief>
**Security threat model:** <path to threat-model.md> — READ FIRST
**Required mitigations:** <list from threat model>
**Non-negotiables:** input validation at every boundary, authz checks uniform, idempotency for webhooks, no secrets in logs, proper error messages
**Scope:** <files>
**CLAUDE.md sections to apply:**
```

**Phase 4 — MANDATORY Post-impl Security Review.**
Before review by Polaris:
```
**Task:** pen-test-mindset review of <diff>
**Threat model:** <path> — verify each mitigation is present
**Focus:** input validation, authz consistency, idempotency, secrets hygiene, error messages
**Expected output:** findings per severity (critical/high/medium/low)
**Save to:** .claude/tmp/artifacts/<date>/<slug>/security-review.md
```

If critical/high findings: mandatory back to Builder. No shipping until clean.

**Phase 5 — QA.** Same as `/feature-dev` but with security-specific test cases:
- Unauthenticated request → proper rejection
- Wrong-role request → proper 403
- Malformed payload → no info leak in error
- Webhook with invalid signature → rejection + no state change

**Phase 6 — Ship + DevOps monitoring.**
DevOps adds **specific monitoring for the new attack surface**:
```
**New alerts required:**
- Anomalous auth failure rates on <new endpoint>
- Webhook signature verification failures (rate + source IP)
- Admin-route access from unexpected users
- Error-rate spike on <new surface>
```

**Phase 7 — Done.**
1. All mitigations from threat model verified present.
2. Monitoring live for the new attack surface.
3. Document the feature + its threat model in the target repo's security section of CLAUDE.md if appropriate.
4. Feed findings back to the project's security posture doc.

## Escalation

- **Any critical finding that can't be mitigated in-scope** → escalate to Dina. She owns the call on whether to narrow scope or defer.
- **Compliance boundary crossed mid-implementation** → stop, threat-model again, re-plan.
- **New attack vector discovered post-ship** → run this skill retroactively on the affected surface.
