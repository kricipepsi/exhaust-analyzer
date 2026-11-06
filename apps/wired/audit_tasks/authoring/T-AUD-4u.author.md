# T-AUD-4u — authoring sidecar (Windows Cowork, 2026-11-06)

Rehearsal: `C:/4DApp/recheck/T-AUD-4u/` (`apply_fix.py`, `rehearsal.patch`). Drawn from Lane 1 (loop_guard refused a
self-made pause below 50 %).

### Verified context ###
1. **Census on the base** (P1): 16 files outside the COMLab design docs name the retired projector (VINLab docs and wiki,
   DTCLab docs, GASLab wiki, DNALab wiki, `labs/semantic` copies, COMLab wiki and skill). Observed.
2. **Rehearsal** (restored): `16 files changed, 36 insertions(+), 37 deletions(-)`; census prints nothing; every lab
   suite equals P3; `git apply --check` passes on the base. Observed.
3. The composition's `_build_obd_dna_view` reads `vin_dna.get("rated_rpm")` (`composition.py`), so the VINLab triples'
   new consumer is true. Observed.

### Rulings and the tradeoff that lost ###
- **Rewrite the live docs; leave history.** Audits, research notes and task packs record what was true then. Lost: a
  repo-wide zero count.
- Plan NONE, difficulty 1 (`--model claude-sonnet-5-5 --effort medium`). Docs row: no second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | census: no line |
| step 2 | SIMULATED | comlab 503/4/2; gaslab 208, obdlab 391, dtclab 590, vinlab 376, dnalab 27, symptomlab 72 |
| step 3 | SIMULATED | 16 files changed; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-4u: no live doc names COMLab's retired DNA projector.

### Cold read ###
own pass 2026-11-06: P1-P3 measured · `apply_fix.py` exits on any count mismatch · traceability: criteria 1-3 → steps
1-3 · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (criteria 2-3); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
