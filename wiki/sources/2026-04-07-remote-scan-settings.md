---
name: Remote Scan Settings Plan — LBS
source_type: transcript
meeting_type: strategy
date: 2026-04-07
tags: [danaher, lbs, scanner, product-architecture, smart-scan, san-diego]
participants: [Madina Gbotoe]
---

# Remote Scan Settings Plan — LBS

Technical product architecture session at LBS San Diego covering scanner capabilities, Smart Scan system, and remote manual scan development.

## APQ Flexibility & Scanner Capabilities

- APQ needs asymmetrical use path capability — ability to change best focus layer dynamically
- 3 minus 3 separation requirement from customer partner analyzing thicker tissue slides
- Anticipating future plus 5 minus 5 request in couple years
- Need practical limits to prevent objective jamming into slide
- MF limits provide scanner self-protection; UI should translate and display maximum capabilities

## Smart Scan System Architecture

- Currently Elite-only feature (licensable, comes free with Elite purchase)
- Enables protocol setup with metadata-based filters from work orders
- Workflow: Common Case service queries LIS through Case Connect -> metadata creates filter -> scanner reads barcode -> gets info -> applies protocol rules -> automatic parameter selection
- Replaces manual rack-level configuration
- Imperial Bridge Data Broker (ABDB) acts as caching intermediary — handles scanner-to-Case Connect communication
- Message bus integrated into data broker

## Remote Manual Scan Development

- Product management directive: "must be able to set manual scan settings remotely"
- Need controlled API for external users (future IQC compatibility)
- User interaction limitations: one user at a time (remote or local), avoid race conditions
- Console notifications required for remote access
- Regulatory considerations: maintain equivalence to local user capabilities
- Queue/priority refactoring opportunity for scan setting preservation

## Protocol Management

- Smart scan copy protocol rules implementation
- New filters requiring dynamic interface
- One-time setup approach: configure rules once, copy protocols
- UI complexity concerns for large topology counts (Quest: 260 topologies)
- Workflow efficiency: mixed slide batches without manual sorting

## Next Steps

- Workshop next morning (9 AM, bring laptops)
- Multiple scanners on SAM testing needed
- AUTH Server integration for annual release
- Prototype development with Nikolai
- Requirements documentation and safety/security assessment

## Key Sources

- [[sources/2026-04-08-ai-code-review-strategy|AI Code Review Strategy (Apr 8)]]
- [[sources/2026-04-08-budget-cap-backend|Budget Cap & Backend (Apr 8)]]
