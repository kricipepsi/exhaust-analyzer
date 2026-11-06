# T-AUD-4q — authoring sidecar (Windows Cowork, 2026-11-06)

Rehearsal: `C:/4DApp/recheck/T-AUD-4q/` (`apply_fix.py`, `rehearsal.patch`, `tests/`).

### Verified context ###
1. **F-D2-10 and F-D2-11 hold:** both `audit/scratch/D2/test_d2_probes.py` probes fail on the base. Observed.
2. **No production caller** (P1): `grep -rln "comlab.projection\|comlab.schemas.lab_dna_views" --include=*.py .`
   lists only the two modules, `test_projection.py`, the audit probes and `Vault/`; `horizon_context_injector.py` has its
   own `_horizon_from_euro`. Observed.
3. **The composition reads the COMLab-C paths:** `_build_gas_dna_view` reads `emissions.has_catalyst`,
   `emissions.egr_equipped` and top-level `target_lambda_v112`. Observed.
4. **Rehearsal** (restored): new file base `2 failed`, fix `2 passed`; comlab 525 → 502/4/2; registry 5F/502P;
   gaslab 208, obdlab 391, dtclab 590, vinlab 376, dnalab 27, symptomlab 72; wired 101; ui 52 (all = base); ruff
   clean; `git apply --check rehearsal.patch` on the base passes. Observed.

### Rulings and the tradeoff that lost ###
- **Retire the projector; the docs follow the code.** Lost: making the code follow HLD §6.1 (the assembler calls
  `comlab.projection.project()`), which would mean rewriting the projector to each lab's own shape and replacing three
  tested builders, for no behaviour gain. Rule 4 (ADR-0003) also forbids keeping a schema with no live consumer.
- **Re-point the two proposals-registry consumers** instead of deleting the entries: COMLab-C is graduated and its
  paths are live in the composition; COMLab-E is a proposal whose real consumer is GASLab's own view.
- **Split the wider doc drift** (≈40 lines in other labs' docs and wikis) into T-AUD-4u. Lost: one sweep; this row
  stays at COMLab's own design docs plus the three lab docstrings the code ships.
- Plan NONE, difficulty 2 (`--model claude-sonnet-5-5 --effort medium`): scripted, rehearsed. Code row (deletions,
  registry), so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `2 passed` (base `2 failed`) |
| step 2 | SIMULATED | comlab `502 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | registry `5 failed, 502 passed, 4 deselected`; gaslab 208, obdlab 391, dtclab 590; wired 101; ui 52 |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-4q: COMLab's dead DNA projector is retired; the docs name the composition as each lab view's builder.

### Cold read ###
own pass 2026-11-06: P1-P4 measured · every `apply_fix.py` literal matched once on the base (the script exits on any
other count) · counts: comlab 525 − 25 + 2 = 502 · traceability: criteria 1-4 → steps 1-4 · no finding.
check 26 FINDING (the lab loop past the per-command limit) patched: one command per lab; CLEAN again.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (criterion 3 "every P4 suite"); 0 findings, 0 patched — 21472 tok, 4 calls.

### Correction history ###
(none)
