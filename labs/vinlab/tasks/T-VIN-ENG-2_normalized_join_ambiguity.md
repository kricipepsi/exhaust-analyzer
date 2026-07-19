# T-VIN-ENG-2 — Normalized vref join + engine-ambiguity confidence flag

**Authored:** 2026-07-06 (architect, Cowork).
**Source:** `planning/AUDIT_2026-07-06_vin_engine_number.md` §2.3–2.4.
**Type:** small decoder change (`decoder.py`, `vinlab/db/tecdoc_query.py`).
**Blocked by:** T-VIN-ENG-1 — **do not start until its Disclosure numbers are in**;
the ambiguity threshold below must be set from the reported majority-share
distribution, not guessed.

### Goal ###
1. Stop losing `vref.db` equipment rows to spelling noise: today the join is raw
   `engine_code = ?`, so `K4M G8` vs `K4MG8` (space/dot/case) misses. Join on a
   normalized form (uppercase, alphanumerics only) — normalize both the lookup
   argument and, once, the `engine_ref` side (either a normalized column or an
   in-memory normalized index in `open_vref_readonly` users). No fuzzy matching.
2. Make VDS ambiguity **visible**: when the winning code's majority share in the
   build (carried in a new map column or sidecar produced by ENG-1's builder) is
   below the threshold chosen from ENG-1's disclosure, append a
   `vds_engine_ambiguous` flag to `conf_flags` so `_compute_confidence` can demote —
   consumed downstream via `VinDNA.confidence` (DNALab/COMLab read it). Flag only;
   no new `VinDNA` field (contract change would need the RFC path).

### Success criteria ###
- A VIN whose map code differs from its `engine_ref` spelling only by
  space/dot/case/junk-prefix now receives the vref tech-mask (add a unit test with
  one real pair from ENG-1's disclosure).
- Ambiguous-VDS VINs carry `vds_engine_ambiguous`; unambiguous ones don't.
- No change to exact-match rate from ENG-1's report (this task adds equipment
  coverage and honesty, not code accuracy); pytest green.

### Disclosure ###
Report before/after counts: map codes joining `engine_ref`, decodes flagged
ambiguous at the chosen threshold, and the threshold + its justification (one line,
citing ENG-1's distribution).
