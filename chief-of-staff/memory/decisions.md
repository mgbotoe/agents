# Decisions — Cold Memory

Key decisions with reasoning. The "why" matters more than the "what."

## 2026-03-30: Dina chose holistic CPO role at WDAI <!-- added 2026-04-13 -->
- **Decision:** Took the broad VP/CPO-like role owning AI-native framework across all WDAI pillars, not just the platform repo
- **Why:** Wants strategic growth, not just IC coding. Helen offered two paths — focused IC or holistic strategy. Dina chose strategy.
- **Context:** Madina<>Helen 1:1, Mar 30. Bi-weekly 1:1s established with project pipeline review format.

## 2026-04-13: Product radar outputs to Discord, not Slack <!-- added 2026-04-13 -->
- **Decision:** Use Discord #product-radar channel for scan outputs instead of WDAI Slack
- **Why:** Gumloop bot can't post to new Slack channels (token issue) and DMs route to Helen instead of Dina. Discord works reliably.
- **Context:** Tested multiple approaches — private channel, public channel, DM. All failed on Slack side.

## 2026-04-13: Atlas owns product signal scanning, dev agent owns code work <!-- added 2026-04-13 -->
- **Decision:** Signal detection/classification is CoS work (Atlas). Building/deploying/verifying code is dev agent work.
- **Why:** Clear lane separation. Atlas was doing both and Dina called it out — Atlas said it's not a dev agent but was verifying code anyway.
- **Context:** Discussion about whether to build signal detector as a standalone agent (option A) or Atlas skill (option B). Chose B short-term, A for dev work later.

## 2026-04-13: Keep Build Radar with Atlas, retire Gumloop radar <!-- added 2026-04-13 -->
- **Decision:** Atlas owns the Build Radar entirely. Do not move back to Gumloop.
- **Why:** Atlas has full context (registry, wiki, Granola, memory, Helen's feedback). Gumloop runs blind — can't pull from 1:1s, can't adapt mid-run, can't capture top-down priorities. Task Scheduler handles the Wed+Fri cadence.
- **Context:** Dina asked whether to move back to Gumloop or keep with Atlas. Atlas recommended staying. Add missed-scan heartbeat as safety net.

## 2026-04-13: GDrive MCP MIME type fix <!-- added 2026-04-13 -->
- **Decision:** Fixed gdrive_upload in local MCP to detect file extension and set correct MIME type (pptx, xlsx, docx, etc.)
- **Why:** Uploads were appearing as zip files in Google Drive because no MIME type was set on the API call.
- **Context:** Fixed in mcp/google-drive/src/index.ts. Added MIME_MAP lookup for common file types. Both pptx and xlsx now open correctly in Google Slides/Sheets.
