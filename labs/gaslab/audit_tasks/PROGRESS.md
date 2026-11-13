# gasa — Progress Ledger (GASLab audit fix rows: `audit/FIX_PLAN.md` T-AUD-5)

**Tasks dir:** `labs/gaslab/audit_tasks/` · **Mode:** STRICT · **ID prefix:** `T-GASA-` (ceiling 99)
**Scope:** T-AUD-5 (P2, GASLab ontology and rules back to the wiki: F-C2-1…15; F-D2-22…24).
**Placement ruling 2026-11-13 (Windows Cowork):** a new folder, not `labs/gaslab/tasks/`, which holds older-format task
files. Same ruling as the coma pack. Lost: one task folder per lab.
**Branch rule:** one `fix/<ID>` branch per row. T-GASA-1 is cut from `fix/T-COMA-30` (`7034d64`); each later row from
the previous accepted row. Never `main`.
**Order:** the HIGH findings first (F-C2-1, 2, 5, 6), each measured on the v7 corpus before it is authored.
**Last updated:** 2026-11-13 (Windows Cowork: pack opened; T-GASA-1 inline, difficulty 1).

Gate blocks go in `progress_notes/<ID>.md`. Cells stay under 120 characters and never contain `|`.

## Task log

**Cap: 25 KB.**

| ID | Task file | Status | Blocked by | Date | Score | Note |
|---|---|---|---|---|---|---|
| T-GASA-1 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | — | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 99, t=15/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-1.md`.** F-C2-1 (HIGH): low-triangle leak route needs CO + CO2 > 6 % (wiki §4.2); diluted sample is INVALID |
| T-GASA-2 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-1 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 99, t=12/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-2.md`.** F-C2-2 (HIGH): collision rule keeps the triangle gate's validity; 2 pins re-stated; T-GASA-1 docstring nit |
| T-GASA-3 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-2 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 97, t=14/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-3.md`.** F-C2-5 (HIGH) first half: valve-seal route idle band 75-500 (wiki 06A v1/v2 severities); 3 band pins; residual f5b (v2 reach) with F-C2-14 |
| T-GASA-4 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-3 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 96, t=22/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-4.md`.** F-C2-6 (HIGH): cam rule opens at the 06B idle floors (ADVANCED 250, MAF 300) on a 2500 RPM confirmation; HC > 1000 path unchanged |
| T-GASA-5 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-4 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 98, t=20/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-5.md`.** F-C2-7 (HIGH): rich MAP fallback needs λ rise + CO fall (resolution.py parity) |
| T-GASA-6 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-5 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 100, t=14/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-6.md`.** F-C2-8 (MEDIUM): CoC overrides (v112 λ, co_low_idle) only at confidence HIGH |
| T-GASA-7 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-6 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 98, t=16/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-7.md`.** F-C2-9 (MEDIUM): collision tier_max by has_catalyst (0.45 / 1.5, vocab §10.2); vocab note replaced |
| T-GASA-8 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-7 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 98, t=18/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-8.md`.** F-C2-10 (MEDIUM): wideband O2_SENSOR_BIASED_LOW CO2 window from the triangle gate (5.7-11.0); one sum-21 pin restated |
| T-GASA-F11 | (not authored: design row) | deferred | — | 2026-11-13 | — | F-C2-11 (MEDIUM): carbon rail. Measured and rejected inline: CO + CO2 > 16 => INVALID moved 15 of 314 corpus verdicts to SAMPLE_INVALID (family accuracy 221 -> 225, +5 -1), broke 3 reachability pins, and contradicts the wiki's own GASWIKI-06B CAM_TIMING_RETARDED_MAP idle vector (CO 7.0 + CO2 10.5 = 17.5). Needs a wiki carbon-rail ruling (rich-mixture carbon totals) before code |
| T-GASA-9 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-8 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 98, t=24/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-9.md`.** F-C2-12 (MEDIUM): masking rule has no cylinder-count gate; old pin restated (1-16); DLD/LLD follow |
| T-GASA-10 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-9 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 98, t=20/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-10.md`.** F-C2-13 (MEDIUM): collision audit counts only filtering edges; 2 EGR_DILUTION pairs named KNOWN_UNRESOLVED_V1 |
| T-GASA-F13 | (not authored: design row) | deferred | T-GASA-10 | 2026-11-13 | — | EGR_DILUTION_MISFIRE overlaps RICH_MISFIRE (0.99) and INCOMPLETE_COMBUSTION (0.985) with no filtering path: its gate `requires_dtc` is not consumed in v1 (GASWIKI-06B). Needs a DTC-evidence input or a wiki-stated differentiator; then remove the pairs from `test_validators` KNOWN_UNRESOLVED_V1 |
| T-GASA-11 | (inline, Cowork; difficulty 1, docs row, no task file: roster 2026-11-13) | done | T-GASA-10 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 100, t=12/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-11.md`.** F-C2-14 (MEDIUM, doc-drift): vocab §6 and GASWIKI-02 §2.3 state the implemented λ; the printed Hcv formula is marked as not a definition |
| T-GASA-F14 | (not authored: design row, difficulty 4-5) | deferred | T-GASA-11 | 2026-11-13 | — | Adopt the full Brettschneider λ (Hcv 1.85, normalised denominator) or keep HC_FACTOR 0.0025: the current HC weighting puts high-HC atlas vectors rich of their stated λ (WORN_VALVE_SEALS v2 idle: code 0.914 vs wiki 0.96; feeds F-C2-4 and the F-C2-5 residual). Moves every verdict: needs a corpus measurement and a plan gate |
| T-GASA-12 | (inline, Cowork; difficulty 1, comment-only docs row: roster 2026-11-13) | done | T-GASA-11 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 100, t=8/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-12.md`.** F-C2-15 (LOW): CoC λ clamps 0.85 / 1.15 cite GASWIKI-06A / GASWIKI-05 atlas limits |
| T-GASA-F4 | (not authored: design row, difficulty 4-5) | deferred | T-GASA-F14 | 2026-11-13 | — | F-C2-4 (HIGH): TIMING_RETARDED box is pre-v2 and holds a healthy idle. Measured inline and rejected: re-boxing to the GASWIKI-05 idle vector moved 66 of 314 corpus verdicts (46 TIMING_RETARDED -> WORN_PISTON_RINGS, whose box also holds a healthy idle), family accuracy 221 -> 217, broke 2 unit pins, and the wiki vector stays unreachable (mostly triangle-invalid: sum max 14.65; code λ 1.17 vs wiki 1.05-1.15). Needs a coordinated re-box of TIMING_RETARDED, WORN_PISTON_RINGS (wiki idle HC 100-150) and WORN_ENGINE, after the T-GASA-F14 λ ruling |
