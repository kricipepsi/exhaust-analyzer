# T-GV2-6 — TIMING_RETARDED 7-Family Separation (decomposition overview)

**Not an implementable task — a map.** The coder never runs `T-GV2-6`; it runs
one of the `T-GV2-6x` leaves below.

### Why decomposed ###

~25 % of the corpus presents as, or collides around, `TIMING_RETARDED`; this is
the single largest discrimination gap (rebuild-proposal roadmap **RQ2**;
`questions.md` Q1). The discriminator engine is the **idle→2500 RPM
differential**, available only since `reading_high` landed in T-GV2-4
(`TEST_RPM_SEPARATION_MATRIX`, GASWIKI-08 / `GAS_WIKI §4` L207).

The literal "split into 7 families" cannot be one task: (a) it would exceed one
session, and (b) several of the seven families **emit no distinct idle
chemistry** (`questions.md`: mechanical_wear 0/11; ecu/non_starter are
non-chemical). A pure-gas 7-way split is therefore partly *infeasible* — those
families route by the RPM differential or **abstain to OBD/DTC**, never by
inventing a DNA field (signal/noise).

### Seven candidate families → where each is handled (no duplication) ###

| Family | Handled in | Status |
|---|---|---|
| cam_timing | **T-GV2-6a** | authored |
| misfire | **T-GV2-6b** | authored 2026-06-05 (scope = prune low-HC misfire when 6a RPM-confirms timing) |
| lean | **T-GV2-6c** | authored 2026-06-05 (scope = lean co-survival mutual-exclusion only) |
| ecu (non-chemical → abstain) | **T-GV2-6d** | **blocked** — no wiki abstain contract; owner decision needed (ledger ABSTAIN-1) |
| sensor | **T-GV2-10** (calibration) + 6d (routing) | T-GV2-10 authored |
| catalyst | **T-GV2-5** | done |
| mechanical_wear | **T-GV2-7** | pending |

### Rules for the leaves ###

- Each leaf is ≤ 50 % context, one session, names its COMLab `chemical_state` /
  fault-atlas consumer, and is **authored by the architect/owner** before its
  session — the coder does not author (decision 2026-06-04).
- A leaf **references** T-GV2-5/7/10 for families they own; it does not
  re-implement their chemistry.
- All numeric literals carry a `# wiki: docs/GASLab/wikiNEW/…` citation. No leaf
  invents a threshold — if the wiki gives a range not a delta, the coder pins it
  in scope confirmation.
