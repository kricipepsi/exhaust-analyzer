# T-GV2-3 — Reconcile the GASLab in/out dataset contract to the v2 wiki

### Goal ###

Bring the **inbound** `GasLabDnaView` and the per-vehicle NORMAL calibration up to
the v2 wiki (`wikiNEW §1.4` + `GAS_VOCABULARY §3/§4.7`), and confirm the
**outbound** `GasLabPayload` already matches the canonical 9-field surface
(`wikiNEW §1.3`). Two concrete corrections:

1. Replace the fabricated λ **band** (`target_lambda_low` / `target_lambda_high`)
   with the single canonical `target_lambda_v112`; the NORMAL λ window is
   `[v112 − 0.005, v112 + 0.005]` (wiki: *"center the ±0.005 window on this
   value"*, `GAS_VOCABULARY` L429).
2. Add `co_high_idle` to the view; it is the per-vehicle mild-rich CO ceiling at
   2500 RPM (`GAS_VOCABULARY` L431). (Field lands here; its 2500-RPM consumer is
   wired in T-GV2-4.)

> **SAI is out of scope for GASLab (decision 2026-06-04).** Do **not** add
> `secondary_air_equipped` or any SAI field/flag. SAI is owned by DTCLab (P0410 /
> `SAI_HISTORY`). This task runs **after** T-GV2-S1 has stripped SAI from the
> wiki, so the wiki §1.4 it reconciles to no longer lists `secondary_air_equipped`.
> GASLab code is already SAI-free; keep it that way.

Done when `gaslab.dna_view.GasLabDnaView` matches the post-purge wiki §1.4 field
set (names + types), `_coc_adjust_normal_bounds` centres the NORMAL λ window on
`target_lambda_v112 ± 0.005`, no `target_lambda_low`/`target_lambda_high`
remains in `gaslab/`, the wired mapper builds the new view, and the full GASLab
suite is green.

### Success criteria ###

Tests-first. Write these failing, then make them pass:

- `tests/test_dna_view.py::test_view_matches_wiki_s1_4` — asserts the field set
  of `GasLabDnaView` equals the post-purge wiki §1.4 set; `target_lambda_v112`
  present; `target_lambda_low`/`target_lambda_high` absent; `co_high_idle`
  present; `secondary_air_equipped` **absent** (SAI is DTCLab-owned).
- `tests/test_rule_engine.py::test_normal_lambda_window_centres_on_v112` — with
  `target_lambda_v112 = 1.000`, NORMAL matches λ in `[0.995, 1.005]` and rejects
  `0.989` / `1.011`; with `v112 = None`, the generic window is unchanged.
- `tests/test_rule_engine.py::test_co_low_idle_ceiling_unchanged` — existing
  per-vehicle CO behaviour preserved (regression guard).
- A corpus regression check: classifications that changed solely because of the
  band→window switch are **enumerated and reviewed**, not silently accepted
  (paste the delta in the progress note).
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Context ###

`ASSESSMENT_InOutProp.md` + `docs/GASLab/v2_prep/PROPOSAL_GASLabV2_InOut_and_Rebuild.md`
established that the runtime λ band is **drift**: the wiki, OPSI (`V112` column),
and COMLab's projector all use a **single** `target_lambda_v112`; GASLab alone
invented `target_lambda_low/high`, and `4DLabWired/composition.py` fabricates the
band from `gas_inputs`. This task removes the drift and aligns GASLab to the
canonical inbound contract before any chemistry-discrimination work builds on it.

`co_high_idle` is a wiki §1.4 field GASLab currently omits. It is added now (the
contract is reconciled once), with its 2500-RPM consumer scheduled (T-GV2-4). Per
the user's field policy (2026-06-04), wiki fields are kept with scheduled
consumers, not pruned. `secondary_air_equipped` is **not** added — SAI is purged
(owner decision 2026-06-04, `T-FX-PURGE-SAI`); GASLab code + wiki are already
SAI-free and stay that way.

**Named signal/noise consumer (required to ship these values):**
- `target_lambda_v112` → **live** consumer `rule_engine._coc_adjust_normal_bounds`
  (NORMAL λ window). This *replaces* an existing consumed field — not a net-new
  orphan.
- `co_high_idle` → consumer is the 2500-RPM mild-rich ceiling, wired in
  **T-GV2-4** (this task adds the field + the idle-side plumbing; T-GV2-4 reads
  it at 2500 RPM). Until then it is parsed and carried, matching COMLab's
  projector which already emits it.

If the reviewer judges that adding `co_high_idle` *ahead* of its consumer
violates signal/noise for this repo, the fallback is to land **only** the λ fix
in T-GV2-3 and add `co_high_idle` in its consumer task (T-GV2-4). **Surface this,
do not guess** — default is to add both the λ fix and `co_high_idle` now (one
contract reconcile), per the proposal.

**Wiki window rule (transcribe verbatim, do not invent):** NORMAL λ centre =
`target_lambda_v112`, half-width `0.005` (`GAS_VOCABULARY` L429). `co_low_idle`
→ `normal_with_cat.max` CO (L430). `co_high_idle` → `mild_rich.max` at 2500 RPM
(L431). Per-vehicle override applies only when `confidence = HIGH` and CoC targets
are populated (`GAS_VOCABULARY` L425).

**Load skills:** `gaslab-python`, `gaslab-verification-loop`,
`gaslab-code-review` (mandatory), `gaslab-wiki-provenance` (field + numeric-literal
edits). Do **not** load the rest of the bundle.

### Deliverables ###

1. `GASLab/gaslab/dna_view.py` — `GasLabDnaView`: remove `target_lambda_low` /
   `target_lambda_high`; add `target_lambda_v112: Optional[float]`; add
   `co_high_idle: Optional[float]`; align
   `confidence` if the type drift is in scope (keep `str` if a `VinConfidence`
   import would create a cross-lab dependency — note the deferral). Update the
   docstring field count + `# wiki: GAS_WIKI §2.4 / §1.4` citations.
2. `GASLab/gaslab/rule_engine.py` — `_coc_adjust_normal_bounds`: replace the
   `[low, high]` band logic with `lo = v112 - 0.005`, `hi = v112 + 0.005` when
   `target_lambda_v112 is not None`; keep the `co_low_idle` CO-ceiling branch;
   cite `# vocab: GAS_VOCABULARY §3` (L429) + `# wiki: GAS_WIKI §4.7`.
3. `4DLabWired/wired/composition.py::_build_gas_dna_view` — build the new view:
   pass `target_lambda_v112` (from `gas_inputs["coc_target_lambda_v112"]`, or the
   existing single CoC source), `co_high_idle`, `secondary_air_equipped`; drop the
   `coc_target_lambda_low/high` fabrication. (Wired touch per FU-4 — keeps the
   harness green; commit from `4DLabWired\`.)
4. `GASLab/tests/test_dna_view.py` — add `test_view_matches_wiki_s1_4`
   (create the file if absent).
5. `GASLab/tests/test_rule_engine.py` — add the two λ-window tests; update any
   fixture that set `target_lambda_low/high` to set `target_lambda_v112`.
6. `GASLab/tests/` — update every fixture/builder that constructs a
   `GasLabDnaView` with the old band fields (grep `target_lambda_low`).

### Files to touch ###

- `GASLab/gaslab/dna_view.py` (MODIFY)
- `GASLab/gaslab/rule_engine.py` (MODIFY)
- `4DLabWired/wired/composition.py` (MODIFY — wired mapper only)
- `GASLab/tests/test_dna_view.py` (CREATE/MODIFY)
- `GASLab/tests/test_rule_engine.py` (MODIFY)
- `GASLab/tests/` fixtures referencing `target_lambda_low/high` (MODIFY)

### Out of scope ###

Does **not** touch COMLab `lab_dna_views.py` / `projection.py` / `vocabulary.py`
or COMLab tests — that is the Stage-4 mirror reconcile (T-GV2-2 / FU-4 COMLab
side); GASLab and COMLab stay intentionally divergent until then. Does **not**
build the 2500-RPM consumer for `co_high_idle` (T-GV2-4) — only adds the field +
idle-side plumbing. Does **not**
add the second `GasReading` to `process()` (T-GV2-4). Does **not** implement euro
scaling / induction / O2-bias consumers (T-GV2-8..10). Does **not** edit any wiki
under `docs/GASLab/`. No outbound-payload change. No new enum value. Surgical-change
rule: every changed line traces to a Deliverable; adjacent issues → `PROGRESS.md`
"Unplanned follow-ups".

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab/GASLab   # or C:\Users\muto\claude\4DApp\4DLab\GASLab on Windows
# (restore sandbox Python 3.14 first — see 4DLab/CLAUDE.md § Sandbox Python)

# Inner loop on each edited file
ruff check gaslab/dna_view.py gaslab/rule_engine.py
pyright gaslab/dna_view.py gaslab/rule_engine.py

# Structural checks
python3.14 -c "from gaslab.dna_view import GasLabDnaView as V; f=set(V.model_fields); assert 'target_lambda_v112' in f; assert not {'target_lambda_low','target_lambda_high'} & f; assert {'co_high_idle','secondary_air_equipped'} <= f; print('view OK', sorted(f))"
grep -rn "target_lambda_low\|target_lambda_high" gaslab/   # expect: no live references

# λ-window behaviour
python3.14 -c "import gaslab.rule_engine as r; print('window rule present:', 'v112' in open('gaslab/rule_engine.py').read() or '0.005' in open('gaslab/rule_engine.py').read())"

# Functional / test checks
pytest tests/ -x -q --tb=short

# Wired harness still green after the mapper change
cd ../4DLabWired && pytest -x -q --tb=short 2>/dev/null || echo "run wired suite per 4DLABWIRED_START_HERE"
```

All steps must pass. Enumerate any NORMAL-classification deltas caused by the
band→window switch in the progress note