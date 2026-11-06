# T-COMA-3a — authoring sidecar (Windows Cowork, 2026-11-06)

Design input: `T-COMA-3.design.md` (same folder). Rehearsal: `C:/4DApp/recheck/T-COMA-3a/` (`apply_fix.py`,
`rehearsal.patch`, `tests/`, `cw/corpus2.json`).

### Verified context ###
1. **No rule names P0335/P0336** (P1); case_040 abstains `NS-NO-RULE` on the base. Observed.
2. **The curated corpus cannot be rebuilt:** `build_corpus.py` reads `apps/wired/harness/data/cases_petrol_master_v6.csv`
   and a `_jaeger` blueprint, both absent; `test_build_corpus.py` fails 5 on the base; case_040 is `drop`
   ("duplicate baseline") in `corpus_meta.json`. Observed.
3. **Rehearsal** (restored): new file base `2 failed, 1 passed`, fix `3 passed`; wired 101 → 104; registry 5F/503P
   (base 5F/502P); non_starter tests 30 passed; comlab 503/4/2; corpus exactly case_040 moves (P2); ruff clean;
   `git apply --check` passes on the base. Observed.

### Rulings and the tradeoff that lost ###
- **NS-005, a new rule** (not P0335 added to NS-004, the fuel-delivery rule). Lost: one fewer rule.
- **P0340 out:** many engines start on crank sync alone. Lost: coverage of the engines that need CMP to start.
- **`passes_cases` resolves against curated ∪ v7.** Lost: a single curated test set; hand-editing the generated
  `corpus_curated.csv` would make it disagree with its own build.
- Plan NONE, difficulty 2 (`--model claude-sonnet-5-5 --effort medium`): one rule, rehearsed, one verdict move. Code
  row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `3 passed`; wired `104 passed` |
| step 2 | SIMULATED | registry `5 failed, 503 passed, 4 deselected`; `30 passed`; comlab `503 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | `corpus 314`; `differ 1`; `case_040 … -> ['non_starter', 'NS-005', True, False, None, 0.85]` |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-3a: a non-starter with a crankshaft position sensor DTC names NS-005.

### Cold read ###
own pass 2026-11-06: P1-P4 measured · `apply_fix.py` exits on any literal count other than 1 · counts: wired 101 + 3 =
104, registry 502 + 1 = 503 · traceability: criteria 1-4 → steps 1-4 · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (R1, criterion 4); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
