---
name: Mailchimp API v3 — Reference
type: infrastructure
tags: [mailchimp, email, api, automation, templates]
created: 2026-05-03
updated: 2026-05-03
related: [[projects/samesf-automation]]
---

# Mailchimp API v3 — Reference

Used by: SAME SF content operations (Sage). Account: `samesanfrancisco@gmail.com`, forever_free plan.

Full project reference with account-specific values: `C:\Workspace\SAMESF\memory\mailchimp-api-reference.md`

---

## Plan Roadmap (researched May 2026)

**Critical date — May 31, 2026:**
- Classic Builder editor retired (UI for editing old templates)
- **Custom-coded templates sunset on Essentials plan** (per Mailchimp pricing page)
- Free plan API workaround for custom-coded templates may also close

**Tier recommendations for 1K-2K subscriber accounts:**
| Plan | Custom-coded Templates | Cost @ 1.5K contacts | Notes |
|---|---|---|---|
| Free | API workaround only (fragile) | $0 | Officially 250 contact cap; grandfathered accounts at risk |
| Essentials | **Sunsets 5/31/2026** | ~$25-35/mo | Avoid — workflow breaks |
| Standard | Permanent | ~$30-45/mo | **Recommended** for mc:edit workflows |
| Premium | Permanent | $350/mo | Overkill |

Essentials also caps automation at 4 steps; Standard gets 200 flows + GenAI + custom reports + dynamic content.

## Free Plan — What's Available

| Feature | Free (forever_free) | Essentials | Standard |
|---|---|---|---|
| Automations | Single welcome email only | Flows up to 4 steps | Expanded flows |
| Segmentation | Basic only (does not work for campaigns) | Basic | Advanced |
| A/B testing | No | Yes | Yes |
| Custom-coded templates | No | No | Yes |
| Send limit | Grandfathered — SAME SF sends to 914+ with no block | — | — |

**SAME SF is on a grandfathered forever_free plan.** The current new free plan limits (250 contacts, 500/month) do not apply. Our actual send limit is higher — confirmed by sending to 914 subscribers without issues.

### Welcome Automation Reality (confirmed May 2026)
- **Classic Automations fully retired June 1, 2025.** No UI access. No new contacts enter any classic workflow. API endpoints technically still exist but orphaned — UI never surfaces them.
- **Automation Flows (Customer Journeys)**: visible on Free plan but cannot be activated — paid plan required (Essentials ~$13-20/mo).
- **Free plan has zero automation as of June 2025.**
- **Only free welcome option**: "Final Welcome Email" under Forms → Signup forms — basic editor, not template-based, fires on signup. Not ideal but functional.
- **Recommendation**: Use Final Welcome Email as stopgap, upgrade to Essentials when budget allows for full branded welcome sequence via Automation Flows.

---

## Key Endpoints

### Templates

| Method | Path | Notes |
|---|---|---|
| `GET` | `/templates` | List all templates |
| `POST` | `/templates` | Create — preserves mc:edit sections |
| `PATCH` | `/templates/{id}` | Update — also preserves mc:edit when full HTML provided (confirmed empirically May 2026) |
| `GET` | `/templates/{id}/default-content` | Returns `sections` dict with mc:edit section names and default values |

### Campaigns

| Method | Path | Notes |
|---|---|---|
| `PUT` | `/campaigns/{id}/content` | Set content. Use `{"template": {"id": N, "sections": {...}}}` for template-based campaigns. Raw `{"html": "..."}` does NOT persist on template-based campaigns. |
| `GET` | `/campaigns/{id}/content` | Returns rendered HTML — use to verify section push worked |
| `POST` | `/campaigns/{id}/actions/schedule` | Schedule. Payload: `{"schedule_time": "YYYY-MM-DDTHH:MM:SS+00:00"}` |

### Automations

| Method | Path | Notes |
|---|---|---|
| `GET` | `/automations` | List all — 0 on SAME SF account |
| `POST` | `/automations` | Create workflow |
| `POST` | `/automations/{id}/emails/{email_id}/queue` | Add subscriber manually, bypasses trigger |

---

## mc:edit — Critical Rules

- Apply to block containers: `<td>`, `<div>`, any block element
- Names must be **unique** within a template
- **href attributes are NOT directly editable** — wrap the entire `<a>` tag inside the mc:edit container
- Do NOT nest mc:edit inside mc:edit
- `mc:hideable` — hides/shows block in editor (no value needed)
- `mc:repeatable` — allows duplication in editor

### The cta_button Pattern (SAME SF standard)

The CTA button section wraps the entire `<td>` so both URL and text are API-controllable:

```html
<td mc:edit="cta_button" align="center" ...>
    <!--[if mso]>
    <v:roundrect href="URL" ...><center>Button Text</center></v:roundrect>
    <![endif]-->
    <!--[if !mso]><!-->
    <a href="URL" style="...">Button Text</a>
    <!--<![endif]-->
</td>
```

When pushing via API, provide **full button HTML** (VML + anchor) as the section value. Both URL and text live in the one section.

---

## Template Push Workflow

```python
# Correct pattern for template-based campaigns
payload = {
    "template": {
        "id": TEMPLATE_ID,
        "sections": {
            "eyebrow": "Section text",
            "headline": "Headline text",
            "cta_button": """<!--[if mso]>...<![endif]-->
                            <!--[if !mso]><!-->
                            <a href="REAL_URL" style="...">Button Text</a>
                            <!--<![endif]-->"""
        }
    }
}
# PUT to /campaigns/{id}/content
# Verify with a fresh GET afterward — check URL is present, YOUREVENTURL is gone
```

---

## SAME SF Templates Quick Reference

| Template | ID | mc:edit Sections | Source File |
|---|---|---|---|
| Event Announcement | 11869797 | preview_text, subtitle, event_image, eyebrow, headline, body_copy, event_details, signoff, cta_button, add_to_calendar | `campaigns/05-may-2026/event-announcement-template-v2.html` |
| Event Reminder | 11869798 | preview_text, subtitle, eyebrow, headline, body_copy, event_details, signoff, cta_button, add_to_calendar | `campaigns/05-may-2026/event-reminder-template-v2.html` |
| Know Before You Go | 11869799 | preview_text, subtitle, eyebrow, headline, body_intro, logistics, schedule, what_to_bring, contact, signoff | `campaigns/05-may-2026/kbyg-template-v2.html` |
| Newsletter | 11869800 | welcome_note, spotlight, section2, section3, section4, section5, events_calendar | — |
| Welcome Email | 11869770 | none (hardcoded) | Needs full rebuild |
| Newsletter (legacy) | 11869768 | same as 11869800 — do not use | — |
