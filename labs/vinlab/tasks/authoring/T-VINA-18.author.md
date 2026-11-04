# T-VINA-18 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. `symptomlab/validator.py` enforces 21 pairs (`len(self._allowed) != 21`); ADR-0008 decides 21. Observed.
2. Five stale lines in four files (P1); R3 named three of them, Cowork found PRD `:185`. Observed (`grep -rn "18"
   labs/symptomlab/docs labs/dnalab/docs | grep -i "pair\|len"`).
3. `black_smoke` is a live pair (`allowed_combinations.yaml:30`). Observed.

### Rulings and the tradeoff that lost ###
- Live statements only; ADR history stays. Lost: rewriting ADR-0003/0007 (history must keep its own numbers).
- Difficulty 1, no second review (docs row, CLAUDE.md step 6).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | on the base the grouped grep counts 5 matching lines (`grep -cE` variant, Cowork 2026-11-04) |
| step 2 | DEFERRED | needs the implementer's commit |
| step 3 | DEFERRED | the same |
| step 4 | DEFERRED | the same |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-18: the symptom catalog's live size statements say 21 (ADR-0006, DNALab DLD/HLD/PRD).

### Cold read ###
own pass 2026-11-04: P1-P2 measured · literals: 5 lines found · traceability: criteria 1-3 → steps 1-4 · JUDGEMENT: 0.
cold read 2026-11-04: not triggered (no 1c hit in a ruling or criterion beyond "only", which names its set).

### Correction history ###
(none)
