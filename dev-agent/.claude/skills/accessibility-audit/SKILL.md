---
name: accessibility-audit
description: Web accessibility audit against WCAG 2.2 Level AA — the standard required by ADA Title III (US), UK Equality Act 2010, European Accessibility Act (EAA, deadline passed June 2025), and California Unruh Act. AUTO-INVOKED when Dina says accessibility audit, a11y audit, accessibility check, accessibility review, WCAG, screen reader, keyboard navigation, ADA compliance, or before shipping any new public-facing page or auth/payment flow in WDAI.
---

# Accessibility Audit

WDAI has global users (US + UK + EU) and is subject to:
- **ADA Title III** (US) — WCAG 2.1 AA floor, courts increasingly cite 2.2. 3,117 federal suits filed in 2025, no size exemption.
- **UK Equality Act 2010** — "reasonable adjustments" for disabled users, WCAG 2.1 AA benchmark.
- **European Accessibility Act (EAA)** — deadline **already passed June 28, 2025**. EN 301 549 = WCAG 2.1 AA. EAA also requires a public Accessibility Statement page.
- **California Unruh Act** — $4,000 per violation in statutory damages on top of federal ADA.

**Target standard: WCAG 2.2 Level AA** — satisfies all four simultaneously. WCAG 2.2 adds 9 criteria beyond 2.1 — all required.

---

## Phase 1 — CI & Tooling Setup (do once, verify on every audit)

Automated checks only catch ~30–40% of WCAG issues. But they catch the same issues every sprint if not wired into CI. Verify these are in place before running any manual audit:

### 1a — Lint-time (pre-commit, catches issues before they ship)
Verify `eslint-plugin-jsx-a11y` is configured in the project ESLint config. If WDAI uses Biome instead, note that Biome's a11y rules are incomplete vs. the ESLint plugin — both should be checked.

```bash
# Check if jsx-a11y is installed
grep -r "jsx-a11y" package.json
```

If missing, flag as P1 gap — add to remediation backlog.

### 1b — Component test-time (jest-axe)
Verify `jest-axe` is used in component tests for any component with interactive UI:
```bash
grep -r "jest-axe\|toHaveNoViolations" --include="*.test.*" .
```

### 1c — E2E test-time (@axe-core/playwright)
This is the primary automated scan tool. Use the installed package, not CDN injection — CDN injection fails on pages with strict CSP (Stripe, Clerk both have CSP).

```bash
# Verify package is installed
grep "axe-core\|@axe-core/playwright" package.json
```

If not installed: `pnpm add -D @axe-core/playwright`

**Run axe scan via Playwright** on each critical path page:
```typescript
import { checkA11y, injectAxe } from '@axe-core/playwright';

// In your Playwright test or Polaris's Playwright MCP session:
await page.goto(url);
await page.waitForLoadState('networkidle');
await injectAxe(page);
await checkA11y(page, undefined, {
  detailedReport: true,
  detailedReportOptions: { html: true },
});
```

**Pages to audit in priority order (WDAI critical paths):**
1. Homepage / landing page (public, highest traffic)
2. Sign-up / membership flow — ADA violation here = discrimination against disabled users trying to join
3. Login (Clerk) — including MFA, session timeout warnings (WCAG 2.2.1)
4. Pricing / checkout (Stripe) — payment inaccessibility = highest legal exposure
5. Course/LMS pages — educational content explicitly named in EAA
6. Member directory
7. Resource library (check any PDFs — see Out of Scope section)

For each page, capture:
- Full-page screenshot
- axe violations list (id, impact, description, nodes affected, HTML snippet)
- Console errors related to ARIA

---

## Phase 2 — Manual WCAG 2.2 AA Checklist

Automated tools miss keyboard traps, focus management, screen reader announcements, logical reading order, and meaningful context. These require human testing.

### 2a — Keyboard Navigation
- [ ] Every interactive element reachable via Tab (no orphaned controls)
- [ ] Focus order is logical — follows visual reading order
- [ ] Focus indicator visible on ALL interactive elements (WCAG 2.4.11 — new in 2.2, ≥2px, sufficient contrast)
- [ ] Focused element not fully hidden by sticky header/footer (WCAG 2.4.12 — new in 2.2)
- [ ] No keyboard traps — can Tab out of modals, dropdowns, date pickers, Clerk widget
- [ ] Modals: focus moves in on open, returns to trigger on close
- [ ] Skip navigation link present, visible on focus, functional
- [ ] All functionality available without drag — pointer drags have single-pointer alternative (WCAG 2.5.7 — new in 2.2)

### 2b — Screen Reader Testing Matrix
Test critical paths (sign-up, login, checkout, one course) against this matrix — single-tool testing misses browser/AT combo bugs:

| AT + Browser | Platform | Priority |
|---|---|---|
| NVDA + Firefox | Windows | P0 — most common desktop combo |
| JAWS + Chrome | Windows | P0 — enterprise/institutional users |
| VoiceOver + Safari | macOS | P1 |
| VoiceOver + Safari | iOS | P1 — mobile members |
| TalkBack + Chrome | Android | P2 |

For each combo, verify:
- [ ] Page `<title>` is unique and descriptive on every route
- [ ] Headings hierarchy: one `<h1>` per page, logical nesting (h1→h2→h3), no skipped levels
- [ ] All images have meaningful `alt` text; decorative images use `alt=""`
- [ ] Form inputs have associated `<label>` or `aria-label` — AT announces correctly
- [ ] Error messages are announced live (`role="alert"` or `aria-live="assertive"`)
- [ ] Buttons have accessible names — icon-only buttons need `aria-label`
- [ ] Links have descriptive text — "click here" / "read more" fail SC 2.4.6
- [ ] Dynamic content updates announced via `aria-live` regions (member search, course progress, etc.)
- [ ] Page language declared (`<html lang="en">`) — WCAG 3.1.1

### 2c — Color & Contrast
- [ ] Normal text ≥ 4.5:1 contrast ratio (WCAG 1.4.3)
- [ ] Large text (18pt / 14pt bold) ≥ 3:1 contrast ratio
- [ ] UI components and focus indicators ≥ 3:1 against adjacent color (WCAG 1.4.11)
- [ ] Information not conveyed by color alone — error states, required fields, status badges

### 2d — Forms (Sign-up, Login, Checkout — highest legal exposure)
- [ ] Required fields indicated beyond color — asterisk + label text, not just red border
- [ ] Error messages identify the specific field AND describe the fix (not just "error occurred")
- [ ] Labels remain visible when field is populated — no label-as-placeholder pattern
- [ ] Personal data fields declare input purpose via `autocomplete` attribute (WCAG 1.3.5)
- [ ] Accessible authentication — no cognitive test (CAPTCHA) required to log in without alternative (WCAG 3.3.8 — new in 2.2)
- [ ] Don't ask for same info twice in a form session (WCAG 3.3.7 — new in 2.2)
- [ ] Time limit warning for session timeouts — warn user before expiry, allow extension (WCAG 2.2.1)
- [ ] Session timeout doesn't lose form data (WCAG 2.2.2)

### 2e — WCAG 2.2 New Criteria (all 9 — mandatory for AA compliance)
- [ ] **2.4.11 Focus Appearance** — Focus indicator ≥ 2px, sufficient contrast vs. adjacent color
- [ ] **2.4.12 Focus Not Obscured (Minimum)** — Focused element not fully hidden by sticky UI chrome
- [ ] **2.4.13 Focus Not Obscured (Enhanced)** — AAA, but worth noting if sticky header is aggressive
- [ ] **2.5.3 Dragging Movements** — Any drag UI has a non-drag alternative (relevant for course reordering)
- [ ] **2.5.7 Dragging Movements (AA)** — Single-pointer alternative exists for all drag operations
- [ ] **2.5.8 Target Size Minimum** — Tap targets ≥ 24×24px, or adequate spacing around smaller targets
- [ ] **3.2.6 Consistent Help** — Help / contact links in same location across all pages
- [ ] **3.3.7 Redundant Entry** — Users not asked to re-enter info already submitted in same session
- [ ] **3.3.8 Accessible Authentication (Minimum)** — No cognitive test to authenticate without alternative
- [ ] **3.3.9 Accessible Authentication (Enhanced)** — No cognitive test at all (aim for this with Clerk)

### 2f — Motion, Media & Video (critical for course platform)
WCAG 1.2.x applies to all pre-recorded and live media. EAA explicitly names educational content.

- [ ] All pre-recorded video has synchronized captions (WCAG 1.2.2 AA) — caption file in VTT format
- [ ] All pre-recorded video has a text transcript published (WCAG 1.2.3 / 1.2.8)
- [ ] Videos with visual-only content (demos, screen recordings) have audio description track (WCAG 1.2.5 AA)
- [ ] Captions are accurate — auto-generated captions alone do not satisfy 1.2.2
- [ ] Live video streams have live captions if used for events (WCAG 1.2.4)
- [ ] Audio-only content (podcasts, recordings) has text transcript (WCAG 1.2.1)
- [ ] Animations respect `prefers-reduced-motion` CSS media query
- [ ] No content flashes more than 3 times/second (seizure risk — WCAG 2.3.1)

### 2g — Zoom & Responsive (display independence)
- [ ] Content readable and functional at 200% browser zoom without loss of functionality (WCAG 1.4.4)
- [ ] No horizontal scroll at 320px viewport width (WCAG 1.4.10 Reflow) — different failure mode from zoom
- [ ] Touch targets ≥ 44×44px on mobile (Apple/Google guideline; 24px is WCAG floor per 2.5.8)
- [ ] Pinch-zoom not disabled — `user-scalable=no` in viewport meta is a WCAG 1.4.4 violation
- [ ] Text spacing adjustable without breaking layout (WCAG 1.4.12 — line height ≥1.5, letter spacing ≥0.12em)

### 2h — Page Language & Internationalization
- [ ] `<html lang="en">` declared on every page (WCAG 3.1.1)
- [ ] Any content in other languages uses `lang` attribute on that element (WCAG 3.1.2)

---

## Phase 3 — Third-Party Widgets (Clerk, Stripe)

WCAG holds the host site responsible for accessibility even when the barrier is in an embedded widget. Document separately — these require vendor configuration, not code fixes.

**Clerk (auth):**
- Test keyboard nav through sign-in, sign-up, MFA flows
- Test CAPTCHA alternative (if any) — WCAG 3.3.8 requires an accessible alternative
- Check Clerk's `appearance` prop for customization of focus indicators and contrast
- Clerk accessibility docs: https://clerk.com/docs/customization/overview

**Stripe (checkout):**
- Stripe Elements are generally accessible; verify keyboard nav through card entry
- Verify error announcements in Stripe form fields
- Stripe has CSP — axe CDN injection fails here; use `@axe-core/playwright` package only

**Luma (events):**
- External embed — document accessibility gaps as vendor responsibility
- Provide accessible alternative (direct link to Luma event page)

---

## Phase 4 — Severity Matrix & Remediation Plan

| Severity | Criteria | Examples | Action |
|----------|----------|---------|--------|
| **P0 — Block ship** | Prevents access to core flow for a disability class | Sign-up form unusable via keyboard; Stripe checkout unreachable without mouse | Fix before any deploy |
| **P1 — Critical** | WCAG AA violation that discriminates | Missing form labels; no focus indicators; missing captions on course video; no session timeout warning | Fix this sprint |
| **P2 — High** | WCAG AA violation, not immediately blocking | Color contrast failure; WCAG 2.2 new criteria gaps; missing `lang` attribute | Fix within 2 sprints |
| **P3 — Medium** | Best practice / WCAG A gap | Missing skip nav; vague link text; inconsistent help location | Backlog with due date |
| **P4 — Low** | Enhancement | AAA criteria; minor UX polish | Nice to have |

Group findings by component (e.g., "Clerk sign-in widget", "CourseCard", "MemberDirectorySearch") so fixes can be batched.

---

## Phase 5 — Delegation

**Designer** — color contrast, focus indicator styling, layout reflow at 320px/200% zoom, touch target sizing, motion/animation, consistent help placement.

**Builder** — semantic HTML, heading hierarchy, ARIA attributes, label associations, `autocomplete` attributes, `aria-live` regions, skip nav, keyboard trap fixes, `lang` attributes, `prefers-reduced-motion` CSS, time-limit warnings, caption/transcript integration.

**QA** — re-run axe scan after each fix batch, keyboard-only test of all critical paths, screen reader test with NVDA+Firefox and VoiceOver+Safari (minimum), verify no regressions.

**Content/Program team** — caption files (VTT) and transcripts for all course videos. This is not a code fix — it's a content workflow. Needs a process, not just a PR.

Delegation packet must include:
- File path(s) containing the violation
- WCAG success criterion (e.g., "SC 1.2.2 Captions (Prerecorded)")
- Severity level
- Reproduction steps (keyboard sequence, AT combo used, or screen recording)
- Expected vs actual behavior

---

## Phase 6 — Accessibility Statement Page (EAA Required)

EAA mandates a public Accessibility Statement. UK Equality Act also expects one. Verify this page exists at `/accessibility` or `/accessibility-statement`.

Required content:
- Conformance status (fully / partially / non-conformant with WCAG 2.2 AA)
- Known accessibility issues and planned fix dates
- Contact method for users to report accessibility barriers (email or form)
- Date of last accessibility review
- Link to relevant enforcement body (for EU users: their national authority)

If the page doesn't exist — create it as part of the remediation plan, not after everything else is fixed. The statement should reflect current state honestly, including known gaps.

---

## Phase 7 — Documentation & Report

Save report to:
```
.claude/tmp/artifacts/YYYY-MM-DD/a11y-audit/report.md
```

Report structure:
```markdown
# Accessibility Audit — WDAI [Date]
## Scope: [pages audited] | Standard: WCAG 2.2 Level AA
## AT/Browser combos tested: [list]

### Executive Summary
- Automated scan: X violations found across Y pages
- Manual findings: X additional (P0: N, P1: N, P2: N, P3: N, P4: N)
- EAA compliance status: [at risk / partially compliant / compliant]
- ADA Title III litigation risk: [high / medium / low]
- Accessibility Statement exists: [yes / no — required by EAA]
- CI tooling in place: [eslint-plugin-jsx-a11y: yes/no | jest-axe: yes/no | @axe-core/playwright: yes/no]

### Critical Path Status
| Path | Keyboard | Screen Reader | Axe Clean | Verdict |
|------|----------|---------------|-----------|---------|

### Findings by Severity
[P0 → P4, grouped by component]

### Third-Party Widget Gaps
[Clerk / Stripe / Luma — vendor responsibility items]

### Video/Media Compliance Status
[List of course videos with caption/transcript status]

### Remediation Backlog
[Ordered by severity, assigned to Designer/Builder/Content/Vendor]

### Retest Checklist
[Items to verify after fixes — include AT combos for each]

### VPAT Note
If WDAI pursues institutional partnerships (universities, government, enterprise),
buyers will request a VPAT (Voluntary Product Accessibility Template) / ACR.
Retain this audit report — it's the source data for generating an ACR.
```

Update `wiki/projects/wdai-tech-debt.md` — accessibility is a legal liability line item.

---

## Out of Scope (document, don't skip)

- **Email (Mailchimp)** — email accessibility is real ADA exposure but requires a separate workflow. Document gap; flag for future skill.
- **PDF / downloadable resources** — tagged PDFs and reading order are WCAG 1.3.1 / 1.3.2 scope. Document any PDFs found in the resource library as a separate backlog item.
- **Native mobile apps** — WDAI is web-only; not applicable.

---

## Rules

- **Never report "compliant" without running both automated AND manual checks.** Axe catches ~30-40% of WCAG issues. Manual keyboard + AT testing is mandatory for any P0/P1 sign-off.
- **Never use CDN axe-core injection.** It fails on pages with CSP (Stripe, Clerk). Use `@axe-core/playwright` package only.
- **EAA deadline has passed.** Every sprint without fixing P1+ findings is ongoing EU legal exposure. Treat them as urgent, not backlog.
- **Third-party widget violations still count.** Document Clerk/Stripe gaps and flag vendor configuration options or accessible alternatives.
- **Video captions are not optional.** WCAG 1.2.2 is Level AA — required, not best practice. Auto-generated captions don't satisfy it.
- **Retest after every fix batch.** Accessibility regressions are common.
- **Don't fix during audit.** Finish the full audit scope first. Partial fixes during investigation miss related issues.
- **Accessibility Statement must reflect reality.** Don't publish a statement claiming full conformance when gaps exist — that's worse than no statement.
