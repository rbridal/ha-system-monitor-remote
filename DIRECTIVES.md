# ha-system-monitor-remote — Directives

Home Assistant integration that displays sensors published by the system-monitor-remote host agent.

## Ownership
- **Masta-Rob** owns this home project DIRECTIVES.md. Flag Rob only for policy changes.

## Safety (always wins)
- No host credentials in git; agent auth stays on the box.

## Directives (priority order, highest first)
- Pair with `system-monitor-remote` agent; keep entity naming stable.
- shop-ha and home-ha are both production targets by hardware location.

## Non-goals
- Not a general SSH monitoring suite.

## Standing rules that apply here
- No secrets in git. Deploy/install via MyHACS approve policy.

## Change log
- 2026-11-04 — Masta-Rob — Initial DIRECTIVES.md (Rob's OK: yes, pt1410u).
