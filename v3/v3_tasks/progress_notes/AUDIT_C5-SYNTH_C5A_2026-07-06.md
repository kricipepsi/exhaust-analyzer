# ARCHITECT AUDIT — T-V3-P4-C5-SYNTH + T-V3-P4-C5A (pre-C5B gate)
**Date:** 2026-07-06 · **Auditor:** Architect (Cowork) · **Verdict: NOT CLEAN — C5B HELD**

## Verified independently (PASS)
- Generator rerun byte-identical ✓ · zero-overlay self-check re-run: drift=0 across 294 ✓
- Live corpus/shim/rules untouched (mtimes predate C5 work); scorer still `top3_family 241/294`, `Hash lock: ok` ✓
- Oracle-code keying (6× ERR-LC-001 / 4× ERR-LC-005) correct vs corpus ✓; split reconciles to 10 ✓
- EGR stay-abstained decision physically well-grounded (matches cluster5.md dilution physics);
  EGR rows seeded below every gate; `banked_stay_abstained_ALARM` empty ✓
- Sim regression check is full-corpus, not FT-8-only (code inspected) ✓
- Coverage arithmetic reconciles: covered 211→207 (4 newly abstained), on-covered 177→176
  (era3_015 left covered as a passing case). No hidden covered-pool regression.

## BLOCKERS
1. **EXP-N022 seed architecture-incoherent.** Labeled "speed-density" with no corpus basis (row
   carries only VIN `WBA…` — a BMW, i.e. a MAF car), yet seeded the classic vacuum-leak trim
   pattern (idle TFT ≈ +24.9% recovering at 2500) that the coder's own research source forbids for
   that architecture — cluster5.md §Speed-Density: NA speed-density is "inherently immune… stable,
   near-zero fuel trims" at idle. Either it is MAF-equipped (then `maf_gps_*` must carry values, not
   None) or speed-density (then trims must be near-zero and it STAYS ABSTAINED; yield drops to +4).
   One of the claimed +5 rides on this invalid row. The bands-report justification ("separates on
   the pressure-recovery trim delta") contradicts the cited physics.
2. **Web corroboration not performed.** No `.firecrawl/` outputs exist; 0 URLs in bands report or
   manifest. The cited domains (motor.com, gearsmagazine.com, scannerdanner.com, …) are from model
   memory — grounding laundered as "web-corroborated". Spec + Agy identity require firecrawl
   fetches saved under `.firecrawl/` and per-band citations.
3. **Undisclosed scoreboard trade-off.** All 5 "WOULD_BANK" cases remain ABSTAINED
   (`would_bank_still_abstained` = all 5). Coverage FALLS 71.8%→70.4% (4 covered cases newly
   abstain, incl. era3_015 which was covered AND passing). Net picture: top3_family +5 (241→246),
   coverage −4 cases, on-covered 83.89%→85.02%. The progress note's "+5 newly banked / 0
   regressions" headline hides this; the owner cannot sign off C5B on that summary.

## DEVIATIONS (fix or justify in the C5B spec)
4. FT-8 union derived static-only = **17** vs contract's live-derived **68** (misses runtime
   neighbours incl. C3 lean-bias winners under LC-001/LC-002). Mitigated by the full-corpus
   regression check, but the contract union is the spec.
5. Off-contract consumer mechanics invented at C5A: `NF-001/NF-002` prune (zero mentions in the C5
   contract — C6-pattern contamination) and VL boost sizing. C5B scope must come from contract §3,
   sized by a corrected dry-run.
6. Band table carries bands for oracle codes absent from the 10 (ERR-LC-003, ERR-SF-004 — the
   latter a sensor_fault code in a C5 table). Dead config; remove or mark unused.

## PROCESS
7. C5A was executed from the quarantined coder-authored draft spec
   (`_QUARANTINE_T-V3-P4-C5A_coder_draft_2026-07-06.md`) — task authoring is architect lane.
8. Two tasks run in one session window (SYNTH 00:26 → C5A 00:43) — one-task-per-session rule.
9. SYNTH progress note written (00:26) before its own deliverables (00:32).

## Disposition
C5B **held**. Remediation spec: `v3/v3_tasks/T-V3-P4-C5R_seed_remediation_and_redryrun.md`.
C5B spec will be authored by the architect only after C5R lands CLEAN.

## OPEN CONFLICT (ruled 2026-07-06: surfaced + held — DECISIONS.md Q-C5-EGR)
dtclab wiki `03_fuel_trim_grammar.md` §3.3 row: stuck-open EGR = **high positive idle trims,
normalising at cruise** — near-identical to the vacuum-leak row on C5's idle→2500 gate.
cluster5.md + the C5R seed instead model EGR as normal/negative-trim (inert dilution, no unmetered
O2) and stay-abstained. Sources conflict; physics arguments exist for both (O2 displacement read
as rich vs misfire O2 dump read as lean). **Held:** EGR rows remain stay-abstained; C5B sizes on
+5. Any future re-ruling requires authenticated firecrawl research on real field reports, then a
wiki-correction or seed-correction task — not a silent pick.

## C5R RE-AUDIT (2026-07-06, architect)
Fixes 1,3,4,5,6 verified on disk: EXP-N022 MAF-equipped with values (rail pressure None retained —
Tier-C); FT-8 union = 68, 0 regressions; NF prune stripped (empty list, yield stays +5);
disclosures + `## AMENDED (C5R)` sections present; seed regeneration byte-identical per gate.
Fix 2 (web corroboration) PARTIAL: firecrawl CLI unauthenticated (`FIRECRAWL_API_KEY` absent);
`.firecrawl/` files were written from browser/model-summarised content — some are root-domain
citations, not verifiable page scrapes. Corroboration remains provisional until firecrawl auth
lands. **C5B unblocked on +5**, with Q-C5-EGR open and Fix-2 noted provisional.
