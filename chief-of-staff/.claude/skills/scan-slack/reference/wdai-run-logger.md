---
name: wdai-run-logger
description: "Logs run entries to the WDAI Product Spectrum Run Log Google Doc. Use\
  \ at the end of every run to record findings with reasoning. Writes in plain HTML\
  \ format \u2014 never markdown, never heading styles inside run entries."
---

## Doc Details
ID: 1XYtkrgzuUvUq62r2hn7Y7jD576gdvPQvgTqEMqZ9hro

Append new entries at the BOTTOM using operation: append.
Content format: html

## Critical Formatting Rules
The Google Docs API converts markdown into heading styles.
This breaks the document. Follow these rules exactly:

NEVER use ## or # markdown headings
NEVER use **bold** markdown syntax
NEVER use markdown tables with |---|---|
NEVER use markdown at all

ALWAYS write entries as HTML:
- Use <p><b>text</b></p> for bold labels
- Use <p>text</p> for regular paragraphs
- Use <ul><li>text</li></ul> for bullet lists
- Use <p>---</p> for section dividers
- Content format must always be set to "html"

## Duplicate Run Prevention
Before appending, check if an entry for today's date
already exists in the doc.
If it does — do NOT append a new entry.
Update the existing entry instead.
Never create two entries for the same date.

## Run Entry Format (HTML only)

<p>---</p>
<p><b>[Wednesday/Friday/Monday] Run — [Date]</b></p>
<p>Items added: [n] | Updated: [n] | Catch-all: [n] | Channels scanned: [n]</p>
<p>Channels: [comma-separated list]</p>
<p>Private: [list or "none"]</p>
<p>No access: [list or "none"]</p>
<p>Canvas scanning: limited — manual flags only</p>

<p><b>1. [Name] (@[full-handle]) — [Project Name]</b></p>
<p>#[channel] · [spectrum emoji + label] · [value tier] ([score]) · [recommended action]</p>
<p>🔗 [permalink]</p>
<p>What: [2-3 sentences — what it does, who built it, what problem it solves, current state]</p>
<p>Why: [One sentence — which question triggered classification and key reason]</p>
<p>Madina to decide: [One specific question — or "None"]</p>

[Repeat for each item]

<p><b>Reviewed but not added:</b></p>
<ul>
<li>@[handle] — [one sentence] · #[channel] · 🔗 [link] · Reason: [one sentence]</li>
</ul>
<p>---</p>

## Backfill Entry Format

<p>---</p>
<p><b>Backfill — [Month Year] — [Date executed]</b></p>
<p>[coverage block same as above]</p>
<p>[items same format as above]</p>
<p>Complete: [X] added · [X] updated · [X] skipped</p>
<p>---</p>

## Nothing Found

<p>---</p>
<p><b>[Day] Run — [Date]</b></p>
<p>No new WDAI builds found this run.</p>
<p>[coverage block]</p>
<p>---</p>

Always write an entry regardless of results.
Always use content_format: html when calling the doc tool.
