---
title: Google OAuth — Testing → Production
status: done
owner: Dina
added: 2026-04-21
closed: 2026-04-25
tags: [auth, gcp, atlas, infra]
---

> **2026-04-25 — Shipped.** App published to Production in `atlas-493123`. All 6 tokens (3 Gmail + 3 GCal) re-issued at 10:15–10:18 PDT. 7-day expiry cycle is now gone. Atlas is unblocked.

# Google OAuth — Push Atlas's App to Production

## Why this exists

Atlas's Gmail + GCal MCP servers auth through a Google OAuth app that's still in **Testing** mode. In Testing mode, refresh tokens expire every **7 days** — which is why Atlas has gone blind 3 times in the last 2 weeks and needed manual re-auth.

Publishing the app to **Production** in GCP Console removes the 7-day limit. But because the app uses restricted/sensitive scopes, Google verification is required to actually get the benefit.

---

## The short version

**Scopes Atlas requests:**
- `https://www.googleapis.com/auth/gmail.modify` — **RESTRICTED** (most sensitive tier)
- `https://www.googleapis.com/auth/calendar` — **SENSITIVE**
- `https://www.googleapis.com/auth/calendar.events` — **SENSITIVE**

**Publishing states:**

| State | Refresh token lifetime | User cap | Verification needed | Cost |
|-------|------------------------|----------|---------------------|------|
| Testing | **7 days** (current pain) | 100 test users | No | Free |
| Production, unverified | **No expiry** | 100 users | No — but OAuth flow shows "unverified app" warning | Free |
| Production, verified | No expiry | Unlimited | Yes — CASA for restricted scopes | $500–$4,500/yr (CASA) |

**For Dina's case (single user, personal use), the permanent fix is Production + unverified.** Publish the app, click through the "unverified app" warning once during re-auth, and the 7-day token expiry goes away. No CASA needed until/unless the app goes public or >100 users.

Google's own policy: apps under 100 users qualify for the personal-use exception — users see a warning screen but can proceed, and refresh tokens don't get the 7-day cap.

---

## Path A — Publish to Production, stay unverified (RECOMMENDED)

This is the fix for Dina's case. Free, permanent, 10 minutes.

1. Go to https://console.cloud.google.com/apis/credentials/consent
2. Select the project Atlas's OAuth client lives in (check `chief-of-staff/mcp/gmail/.env` for `GOOGLE_CLIENT_ID` and match it in the console's Credentials tab)
3. On the **OAuth consent screen** page, click **PUBLISH APP**
4. Confirm the dialog — status should flip to "In production"
5. Re-auth all 6 accounts one more time:
   ```
   cd C:\Workspace\agents\chief-of-staff
   cd mcp/gmail && bun run src/auth.ts personal
   bun run src/auth.ts business
   bun run src/auth.ts nonprofit
   cd ../google-calendar && bun run src/auth.ts personal
   bun run src/auth.ts business
   bun run src/auth.ts nonprofit
   ```
6. During each browser auth, you'll see a **"Google hasn't verified this app"** warning. Click **Advanced** → **Go to [app name] (unsafe)** → **Continue**. This is expected for unverified apps. One-time per account.
7. Tokens now persist until revoked. No more 7-day cycle.

**Why this works:** Google's personal-use exception allows unverified production apps with <100 users to function normally — users just acknowledge the warning once. The 7-day refresh token cap is a Testing-mode restriction, not a production-unverified restriction.

---

## Path B — Full verification (only if scaling beyond personal use)

Needed if: app will have 100+ users, or you want to remove the "unverified app" warning for a polished public experience.

Requires CASA security assessment by an App Defense Alliance approved lab:
- Cost: **$500–$4,500/yr** for typical tiers (restricted-scope apps)
- Timeline: 4–6 weeks
- Annual renewal

Not needed for personal-use Atlas. Skip unless the product changes shape.

---

## Path C — Automate the re-auth (old fallback, no longer recommended)

Only useful if Path A somehow fails (e.g., Google revokes the personal-use exception for this specific app). Keeps the 7-day cycle, adds a weekly reminder so Atlas doesn't go blind mid-week.

---

## Recommendation

**Path A.** Free, permanent, no verification needed for personal use. The only cost is clicking past an "unverified app" warning once per account during re-auth — which you're doing anyway tonight to unblock.

---

## Checklist (Dina action items)

- [ ] Identify the exact GCP project (`chief-of-staff/mcp/gmail/.env` → `GOOGLE_CLIENT_ID`)
- [ ] GCP Console → OAuth consent screen → **PUBLISH APP**
- [ ] Re-auth all 6 accounts (3 Gmail + 3 GCal) — click through "unverified app" warning once per account
- [ ] Confirm Atlas reports clean Gmail + GCal access in next brief
- [ ] (Optional) DM me to wire a 6-day pre-expiry watchdog as belt-and-suspenders in case Google's policy shifts

---

## References

- [Google OAuth verification FAQ](https://support.google.com/cloud/answer/9110914)
- [Restricted scopes list](https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification)
- [CASA assessment overview](https://appdefensealliance.dev/casa)
- Atlas's auth code: `chief-of-staff/mcp/gmail/src/auth.ts`, `chief-of-staff/mcp/google-calendar/src/auth.ts`
