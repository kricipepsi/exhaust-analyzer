# T-VINA-8 — authoring sidecar (Windows Cowork, 2026-11-03)

### Verified context ###
1. **Findings reproduce** on `fix/T-VINA-1` (`22a6e98`): C6 probes `-k "f11_ or f12_ or f13_"` → `4 failed`.
2. **Code (read):** `models.py::SymptomDNA.from_json` reads `env.get("load_state", LoadState.IDLE)` under a comment
   that ties the default to the T-DNA-7 schema bump, which landed (`SCHEMA_VERSION = "1.2"`). `validator.py::validate`
   tests `(tier_1, tier_2) not in self._allowed` first: a list raises `TypeError` (unhashable).
3. **Catalog (P4):** `allowed_combinations.yaml` has 7 tier_1 keys × 3; `validator.py:95-96` says 21;
   `wiki/04_catalog_changelog.md:101` records the 18 → 21 change.
4. **Rehearsal (P2, `make_rh.py`):** symptomlab `68 passed` (63 - 0 + 5; one PIN test rewritten); dnalab 27, wired 41,
   ui 30, comlab `526 passed, 4 skipped, 2 errors` unchanged with `PYTHONPATH` on the copy; MR1 `1 failed`, MR2
   `4 failed`; ruff clean. A first comlab run showed 5 more errors: the `--basetemp` parent was missing (step 0 now).
5. **Docs (P3):** 54 old-count lines outside the ADR (wider regex than the probe's 40); 6 oil sub-filter entries
   missing from HLD and LLD; ADR header: "immutable once Accepted … supersede an ADR with a new one".

### Rulings and the tradeoff that lost ###
- `load_state` required. Lost: keep the idle default with a deprecation flag: the version gate already refuses
  pre-1.2 payloads, so no valid payload lacks the axis; idle silently picks the vacuum-leak regime.
- Type check before the lookup. Lost: catch `TypeError` around the lookup: an explicit `isinstance` names the cause.
- A superseding ADR-0008. Lost: edit ADR-0003 in place: the file's own rule forbids it.
- Score 2: rehearsed code; the bulk is mechanical doc edits with a grep criterion.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 0 | RAN | `mkdir -p` (without it comlab shows 5 extra errors) |
| step 1 | SIMULATED | copy: `68 passed` |
| step 2 | SIMULATED | copy: `5 passed`; MR1 `1 failed, 67 passed`; MR2 `4 failed, 64 passed` |
| step 3 | SIMULATED | `PYTHONPATH` on the copy: `27`, `41`, `30`, `526 passed, 4 skipped, 2 errors` |
| step 4 | SIMULATED | copy: `3 passed, 48 deselected`; base `3 failed` |
| step 5 | DEFERRED | prose is the implementer's; base `54`, `6`, `0`, `0` |
| step 6 | SIMULATED | ruff on the copy: `All checks passed!` |

### Exclusivity ###
No other implementer runs. T-VINA-1 closed and pushed.

### Progress hook ###
T-VINA-8: SymptomLab refuses missing load_state and non-string tiers; docs say 21 pairs; ADR-0008 supersedes 0003.

### Cold read ###
own pass 2026-11-03: anchors 6 (each `grep -cF` = 1; `make_rh.py` asserts each `rep()` once) · counts: 68 = 63 + 5;
5 = 1 round trip + 4 non-string cases · rule rehearsal: 4 suites through the copy, 2 mutants · traceability:
criteria 1-5 → steps 1-6; every write has a Files line · JUDGEMENT criteria: 0.
cold read 2026-11-03 FOCUSED reader; trigger grep hit (R5 "every"); 0 findings, 0 patched, 0 not-a-conflict — 3 calls
(`recheck/scratch/coldread_T-VINA-8.md`).

### Correction history ###
