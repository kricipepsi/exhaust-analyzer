# Prep Report: cluster3.md

**Date:** 2026-07-01
**Input size:** 58107 bytes / 864 lines
**Output size:** 24632 bytes / 248 lines
**Token delta:** ~14,000 → ~8,200 (raw copy + citation noise removed)

## Root problem
The source file contained its **entire content twice**:
- Lines 1–656: a raw export dump — plain-text title (no `#`), two ASCII box-drawing flowcharts, broken subscripts (`V ref` split across lines), and ~39 search-result citation stubs (`Opens in a new window / slideshare.net …`).
- Lines 657–864: a clean Markdown copy with proper heading hierarchy.

The dedupe was **not** a straight "keep the clean copy" — the clean copy had silently lost data (see R5/R6 below). The prepped file uses the clean copy's structure but restores the missing content from the raw copy.

## Changes applied

| Rule | Description | Count |
|---|---|---|
| R1 Frontmatter | Injected YAML block (title, tokens, concepts, TOC) | 1 |
| R2 Headings | Verified max-3-level, no skips; H1 now single | 0 promotions needed |
| R3 Text layout | No sentence rewrites needed in clean copy | 0 |
| R4 Math | Inline expressions kept as-is (simple, LLM-safe) | 0 |
| R5 Tables | Rebuilt corrupted Quantitative Signature table; restored 7 numeric thresholds + correct tiers | 1 |
| R6 Diagrams | Converted 2 ASCII box-flowcharts to Mermaid | 2 |
| R7 Code fences | All fences language-tagged (`mermaid`); escaped literal `|` in table cells | — |
| Dedupe | Removed entire raw duplicate copy (lines 1–656) | 1 |
| Noise | Removed ~39 search-citation stubs | 39 |

## Critical fix — data recovered from the discarded copy
The clean copy's **Quantitative Diagnostic Signature Mapping** table was broken: the absolute-value bars (`|λ_OBD − λ_tailpipe|`, `|P_MAP − P_BARO|`) collided with Markdown's `|` column delimiters, shifting every column and **dropping all seven threshold numbers**. These were recovered from the raw copy (lines 309–413) and re-inserted with the bars escaped as `\|`:

- Gas-to-OBD divergence: Δλ ≥ 0.05
- Adaptive fuel trim: LTFT ≥ +25% or ≤ −25%
- KOEO MAP-vs-BARO: ≥ 5 kPa
- DLC signal ground drop: ΔV_gnd > 0.20 V
- Ground path voltage drop: > 0.10 V (joint) / > 0.20 V (wire)
- Active override response: O2 delta < 0.1 V
- Harness resistance: > 2.0 Ω (faulty) / > 10.0 Ω (broken)

Both ASCII flowcharts (4-step diagnostic sequence; ECU-ground-degradation cascade) were **absent from the clean copy** and are restored as Mermaid.

## Skipped (judgment call)
- The ground-degradation cascade diagram partly restates the prose in "Sensor Ground Offset and Closed-Loop Divergence." Kept as Mermaid anyway — md-prep Rule 6 converts diagrams rather than dropping them, and it is faithful to what the author drew. Low cost, zero info loss.
- Inline math (e.g. `V_meas = V_sensor + ΔV_gnd`) left as plain text — simple enough to be LLM-safe; no ASCII fraction layout present, so no LaTeX blocks were required.

## Output
- `cluster3_prepped.md` (original `cluster3.md` left untouched)
- `cluster3_PREP_REPORT.md`
