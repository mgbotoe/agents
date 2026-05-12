# Pass 1 · Data architecture

**Part of the Pass 1 split.** See `01-system-context.md` for framing, the 7 Pass-3 design questions, and the C4 system overview. This file is one of the supplementary surfaces.

**Important framing:** "team-OS" throughout these documents refers to a **proposed future federation** that Pass 3 will design. It does not exist today. Phrasings like "Pass 3 must X" mean "X is a constraint surfaced by current state."

---

## Data architecture

### Data flow / data residency (#2)

Where member PII flows. Honest about what I don't know.

```mermaid
flowchart LR
    Member([Member])

    Member -->|signup form| Clerk
    Member -->|payment| Stripe
    Member -->|profile photo + bio| Portal
    Member -->|messages| Slack
    Member -->|events| Luma
    Member -->|emails| Mailchimp

    Clerk -->|webhook · email/name/auth meta| SupabaseUser[Supabase User]
    Stripe -->|webhook · subscription| SupabaseMembership[Supabase Membership]
    Portal -->|saves| SupabaseProfile[Supabase profile fields]
    Slack -->|invite click| AuditLog
    Luma -->|RSVP| SupabaseRsvp[Supabase EventRsvp]

    SupabaseUser -.legacy.-> AirtableMembers[Airtable members]

    SupabaseProfile -->|profile complete| Newswire[Newswire post to #intros]
    Newswire --> SlackHistory[Slack channel history]

    GoogleMeet[Google Meet recordings] -->|Wit pipeline| Vimeo
    Vimeo -->|recap link| Mailchimp

    HelenG[Helen Granola] -. private to Helen .-> HelenSecondBrain[Helen LLM second brain]
    MadinaG[Madina Granola] -. private to Madina .-> MadinaWiki[wiki/sources/]

    classDef person fill:#fef3c7,stroke:#a16207
    classDef extSink fill:#fee2e2,stroke:#b91c1c
    classDef ownedDB fill:#dcfce7,stroke:#166534
    classDef legacy fill:#f3f4f6,stroke:#6b7280
    classDef privCtx fill:#dbeafe,stroke:#1e40af

    class Member,HelenG,MadinaG person
    class Clerk,Stripe,Slack,Luma,Mailchimp,GoogleMeet,Vimeo,LinkedIn extSink
    class Portal,SupabaseUser,SupabaseMembership,SupabaseProfile,SupabaseRsvp,AuditLog,Newswire,SlackHistory ownedDB
    class AirtableMembers legacy
    class HelenSecondBrain,MadinaWiki privCtx
```

**Member PII lives in at least 8 systems** (Stripe, Clerk, Supabase, Mailchimp, Slack, Luma, Vimeo, Airtable). Plus per-user Granola transcripts that may include member voices on cohort calls.

**GDPR exposure (rough):**
- UK chapter members exist (`geo-london`, `uk-hackathon-*` channels)
- Right-to-delete would have to touch all 8 systems
- No documented retention policy for any of them (open question)

**Knowns about retention:**
- AuditLog: indefinite (no purge job visible)
- Mailchimp: kept until manually unsubscribed
- Supabase: indefinite
- Slack: workspace retention setting (unknown — probably default)

**Unknowns (open questions):**
- Mailchimp retention policy
- Granola retention (per-account)
- Vimeo retention for cohort recordings
- LinkedIn-side data (WDAI org page posts)
- Stripe retention (legally bounded for PCI but specifics not documented)
- Recording consent flow — do members opt in to Vimeo upload?

### Data model — Prisma entity relationships (#12)

22 entities in `wdai-foundation-platform/web/prisma/schema.prisma`. Names known; full FK relationships not 100% verified from the audit (would need a schema dump). Inferred groupings:

```mermaid
flowchart TB
    subgraph Identity[Identity + auth]
        User
        UserConsent
        ClerkWebhookEvent
    end

    subgraph Billing[Billing]
        Membership
        StripeWebhookEvent
    end

    subgraph Content[Content + courses]
        LessonContent
        LessonProgress
        CourseEnrollment
        Resource
        ResourceSave
        SavedPrompt
    end

    subgraph Events[Events + RSVPs]
        EventRsvp
        CohortRsvp
        CachedEvent
        EventMeeting
        RecordingUpload
    end

    subgraph Agents[Agent / system tables]
        AuditLog
        ContentChangeBatch
        ContentChangeProposal
        Announcement
        Slack
    end

    subgraph Legacy[Legacy]
        LegacyApprovedEmail
    end

    User --> Membership
    User --> CourseEnrollment
    User --> EventRsvp
    User --> CohortRsvp
    User --> ResourceSave
    User --> SavedPrompt
    User --> UserConsent
    User --> RecordingUpload
    User --> Slack

    Membership --> StripeWebhookEvent
    User --> ClerkWebhookEvent

    CourseEnrollment --> LessonProgress
    LessonProgress --> LessonContent

    EventRsvp --> CachedEvent
    CachedEvent --> EventMeeting
    EventMeeting --> RecordingUpload

    ContentChangeBatch --> ContentChangeProposal

    classDef id fill:#dbeafe,stroke:#1e40af
    classDef bill fill:#dcfce7,stroke:#166534
    classDef cont fill:#fef3c7,stroke:#a16207
    classDef evt fill:#fde68a,stroke:#92400e
    classDef agt fill:#bbf7d0,stroke:#15803d
    classDef leg fill:#f3f4f6,stroke:#6b7280

    class User,UserConsent,ClerkWebhookEvent id
    class Membership,StripeWebhookEvent bill
    class LessonContent,LessonProgress,CourseEnrollment,Resource,ResourceSave,SavedPrompt cont
    class EventRsvp,CohortRsvp,CachedEvent,EventMeeting,RecordingUpload evt
    class AuditLog,ContentChangeBatch,ContentChangeProposal,Announcement,Slack agt
    class LegacyApprovedEmail leg
```

**Inferred — needs schema verification.** I read the entity *names* in deep-dive prep; the explicit relationships (FK names, cascade rules, indexes) require reading the schema file. Flagged as open question.

**What this surfaces:** `User` is the hub. Six concerns radiate from it. Pass 3 must respect this if any federation design ever touches member records — and per the out-of-scope boundary, it shouldn't.

---
