# Prep Report: cardiagnosis.md

**Date:** 2026-06-08
**Input:** cardiagnosis.md (265,259 bytes, 6,670 lines after CRLF strip)
**Output:** cardiagnosis_prepped.md (267,630 bytes, 6,676 lines)
**Archetype:** CLEAN (diagnose_wall: no wall-of-text, no box-drawing)

## Changes applied

| Rule | Description | Count |
|---|---|---|
| Encoding | CRLF -> LF | 6,670 |
| Encoding | 0x0B (vertical-tab OCR glitch) -> capital N | 70 |
| Encoding | "2etwork" -> "Network" | 1 |
| R1 Frontmatter | Injected YAML block + H1 | 1 |
| R2 Headings | Injected chapter/section headings at body anchors (max depth ###) | 36 |
| Noise | Standalone page-number lines removed | 139 |

## Logical-chunk index (read these line ranges in cardiagnosis_prepped.md)

Chunks follow the book's own chapter structure. Marked [IN] = in 4DLab petrol
diagnostic scope, [OUT] = out of scope (non-engine / hardware / security / mods).

| # | Chunk | Scope |
|---|---|---|
| C0 | Front matter & Contents | ref |
| C1 | Electronic Engine Management (fundamentals; lambda/O2 = truth vs ECU = perception) | [IN] |
| C2 | Diagnosing engine failure without devices | [IN] (partial) |
| C3 | SRS diagnostics / ABS diagnostics / service-interval reset | [OUT] |
| C4 | OBD I — K/L lines, KL diagnostics, interface install | [IN] (protocol context) |
| C5 | OBD II — software/interface, handheld scanners, new vehicles, Pending codes | [IN] |
| C6 | The most common causes of trouble codes (per-sensor) | [IN] core |
| C7 | EVAP system | [IN] |
| C8 | ECU Flashing and Mapping | [OUT] (modification) |
| C9 | Immobilizer / anti-theft | [OUT] (security) |
| C10 | Radio decoding / parking sensors | [OUT] |
| C11 | ECM/PCM repair, transistor/resistor/capacitor testing | [OUT] (hardware) |
| C12 | Cruise control / Start-Stop / Regenerative braking / HHO | [OUT] |

## Items requiring manual review

- Two-column OCR flattening: some prose sentences interleave across the original
  column break. Technical values (voltages, ppm, lambda) read correctly; narrative
  ordering is occasionally scrambled. Flagged, not auto-fixed (no info loss vs source).
- A handful of OCR letter glitches remain in prose (e.g. "Marin" vs "Marić" on
  cover). None affect the numeric/diagnostic content used for analysis.

## Skipped (judgment call)

- TOC dotted leaders (`....`) kept inside C0 — they ARE the table of contents.
- No table->JSON or ASCII-equation conversion needed: source has no Markdown
  tables and no multi-line ASCII equations (formula content is inline prose).
