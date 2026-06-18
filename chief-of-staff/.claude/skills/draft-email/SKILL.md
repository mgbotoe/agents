---
name: draft-email
description: Draft or reply to emails in Dina's voice. Use when Dina says "draft", "reply to", "write an email", "respond to this", or forwards an email thread for response.
---

Draft an email in Dina's voice as her Chief of Staff.

## Voice Reference

Read `wiki/sources/dina-email-voice-profile.md` (repo root) before drafting. This is the source of truth for her tone, patterns, vocabulary, and structure. Key rules:

- Match opening to relationship: Hello (formal) → Hi (warm) → Hey (casual) → none (close)
- Get to the point in sentence 1-2. No filler openings.
- Shorter than you think. Her default is brief.
- Use HER phrases: "I have capacity", "swift responses", "Please let me know", "Totally possible I'm missing something"
- AVOID: "I hope this email finds you well", "Absolutely!", "Great question!", "Per my last email", "Circle back", "Touch base"
- Don't correct her grammar patterns ("I will like to", comma splices) — they're her voice
- Closing: "Best, Madina" (professional), "Thanks, Madina" (standard), "Thank you!" (quick)
- Emojis only with people she's casual with

## Steps

1. **Identify context** — who is the recipient? What's the relationship? Check wiki for people pages. Check gmail for recent thread context if replying.
2. **Determine register** — formal (first contact, institution), professional (known contact), warm (referral/introduced), casual (established), ultra-casual (close friends/family)
3. **Draft** — write the email following the voice profile. Match length to the situation:
   - Quick reply: 1-2 sentences
   - Standard: 3-5 sentences
   - Outreach/inquiry: 1-2 paragraphs with structure
4. **Present** — show the draft to Dina. Don't send without explicit approval.
5. **Revise if needed** — adjust based on feedback, then confirm before sending.
6. **Send** — use `gmail_draft` to save as draft, or `gmail_send` only if Dina explicitly says "send it."

## Account Selection

- **Danaher:** Cannot send (no access to madina.gbotoe@danaher.com). Draft the text and Dina copies it.
- **Business:** madina@gbotoe.com — client work, Gbotoe Co.
- **Nonprofit:** madina@womendefiningai.org — WDAI
- **Personal:** mgbotoe@gmail.com — everything else

## Rules

- **Never send without explicit approval.** Always draft first, show Dina, wait for "send it" or equivalent.
- **Never fabricate facts.** If you don't know a detail (date, number, name), leave a [PLACEHOLDER] and flag it.
- **Check the thread.** If replying, read the full thread first via `gmail_get_thread` so the reply is contextually accurate.
- **Recruiter emails:** Frame from strength, ask pointed questions before committing to calls, never sound eager.
- **Client emails:** Reference specific things discussed, show homework was done, give the client space.
- **Academic emails:** Most formal register. Use First/Second/Lastly structure for multi-part inquiries.
