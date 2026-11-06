# T-AUD-13 — authoring sidecar (Windows Cowork, 2026-11-06)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_dnalab.md`, `reviews/REVIEW_T-AUD-11b.md`. Rehearsal:
`C:/4DApp/recheck/T-AUD-13/` (`apply_fix.py`, `rehearsal.patch`, `census.sh`).

### Verified context ###
1. **Each upheld finding re-read at its doc line** on `fix/T-AUD-12`: README:8, PRD:86, PRD:126-128, HLD:52, HLD:106,
   LLD:74, DLD:70, DLD:107, DLD:109; code `assembly.py:32,41-47` (five keys), `models.py:74-75` (`to_json_payload`).
   Observed.
2. **ADR_DNALab check (11b's population gap):** ADR:129 (`to_json()` delegation) and ADR:160 (four keys) repeat
   findings; `docs/adr/` is named 7 times in ADR (5), BDD (1), DLD (1), while the files are `labs/dnalab/adr/0001-0004`
   (`ls labs/dnalab/adr`; `ls labs/dnalab/docs/adr` fails). Observed.
3. **Rehearsal** (restored): census base `stale 19`, after `stale 0`; `adr paths 1 missing 0` both; dnalab 27 passed;
   seven docs, 21 insertions / 20 deletions. Observed.

### Rulings and the tradeoff that lost ###
- **README boundary states ADR-0002** (DNALab imports vinlab and symptomlab, no COMLab). Lost: nothing; "no cross-lab
  imports" contradicted the accepted ADR.
- **`resolve()` is described with five named keys.** Lost: the shorter `**triage` notation, which hid that
  `free_text_notes` is dropped (HLD:83/158 already said so).
- Docs row: no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `stale 0`; `adr paths 1 missing 0` |
| step 2 | SIMULATED | `27 passed` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-13: DNALab docs match the code (10 drift findings of 11b + the ADR check).

### Cold read ###
own pass 2026-11-06: P1-P2 measured · `apply_fix.py` exits on any literal count other than 1 (5 for the ADR paths) ·
traceability: criteria 1-3 → steps 1-3 · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (criterion 3 "only"); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
