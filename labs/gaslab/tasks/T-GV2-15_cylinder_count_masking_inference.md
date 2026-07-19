# T-GV2-15 — Wire `cylinder_count` into the misfire masking rule (05A inference)

*(Closes follow-up **FU-CYL**. Misfire family — distinct from T-GV2-7's POA/oil
family, which is why it is its own task.)*

### Goal ###

Give the orphan field `cylinder_count` (`dna_view.py:29`, `ge=1, le=16`) a named
live consumer inside GASLab by wiring it into the **misfire masking rule** as the
wiki specifies. `05_fault_atlas_part_a.md §FAULT_IGNITION_MISFIRE` (L35–37)
defines the masking discriminator as a cylinder inference:

> `inferred_misfiring_cylinder_count ≈ round(O₂ / (21 / cylinder_count))`

The current masking rule (`rule_engine.py:274–279`) fires `IGNITION_MISFIRE`
purely on `hc / o2 / nox` thresholds and **never reads `cylinder_count`** — so the
field is read in 0 live GASLab paths (orphan). This task adds the cylinder
inference as a **confirmation conjunct** on the existing masking gate.

### Premise (verified — read before authoring/altering) ###

- Masking rule: `rule_engine.py:274–279` — fires `IGNITION_MISFIRE` when
  `hc > 1000 ∧ o2 > 3.0 ∧ nox < 50` (`GAS_WIKI §8.4`). This is the single live
  code path for the misfire masking signature.
- `cylinder_count` is on the local DNA slice (`dna_view.py:29`) but read in **0**
  GASLab paths. (It *is* consumed downstream in COMLab analytics —
  `power_loss_analytics.py:71/82` dilution normaliser — and `fault_atlas_router.
  py:1142`; that is COMLab's read, not GASLab's. See the signal/noise decision.)
- `05A §FAULT_IGNITION_MISFIRE` marks `dna_gate: none (cylinder math needs
  cylinder_count)` and `match_class: DEFINITIVE (via → RULE_MASKING)`. The
  cylinder math is the **confirmation mechanism**, not a new emitted field.

### Signal/noise consumer ###

`cylinder_count` → read in `rule_engine.py` masking rule to compute
`inferred_misfiring_cylinder_count = round(o2 / (21 / cylinder_count))`, used to
**confirm** the existing `IGNITION_MISFIRE` `ChemicalSignature` → COMLab
`chemical_state` / fault-atlas routing (GASWIKI-05A). **No new field, no new
enum** — the inferred count is a local intermediate used by the gate, not an
output on the payload. Anti-orphan: after this task `grep cylinder_count
GASLab/gaslab/rule_engine.py` must show a live read in the masking branch.

### ⚠ Open decision — architect flag (ratify before coding) ###

There are two defensible homes for `cylinder_count`; the owner picks one:

- **(a) Wire it into the masking rule (this task's default).** The 05A inference
  becomes a confirmation conjunct on the `IGNITION_MISFIRE` gate. Gives GASLab a
  live consumer, keeps the field on the slice. Low regression risk (see literal
  below). **Recommended** — it is the wiki's stated mechanism.
- **(b) Rule the field COMLab-owned and drop it from GASLab's slice.**
  `cylinder_count` is already consumed by COMLab analytics + fault-atlas router;
  if GASLab is not meant to reason on cylinder count, the honest fix is to remove
  it from `dna_view.py` rather than invent a GASLab use. This is a *contract
  narrowing* task, not a masking-rule task, and would touch `dna_view.py` +
  `composition.py::_build_gas_dna_view` (FU-4) instead.

This file specs **(a)**. If the owner prefers **(b)**, this task is re-authored as
a slice-narrowing task. Do not implement both.

### Pinned literal (coder uses exactly this — no invention) ###

Add as a conjunct to the existing masking gate:

```python
# wiki: docs/GASLab/wikiNEW/05_fault_atlas_part_a.md §FAULT_IGNITION_MISFIRE
inferred_cyl = round(reading.o2 / (21 / dna.cylinder_count))
# masking confirmed only if the O2 spike is consistent with >=1 dropped cylinder
... and inferred_cyl >= 1
```

`21` is ambient O₂ % (`# wiki: GAS_WIKI §3` five-gas reference — already cited
elsewhere as the air-O₂ constant). The `>= 1` floor is the wiki's "whole-cylinder
dropout" confirmation: with the gate already requiring `o2 > 3.0`, `round(o2 *
cylinder_count / 21) >= 1` holds for every `cylinder_count >= 1` (e.g. o2=3,
cyl=4 → round(0.57)=1), so on the existing masking population the conjunct is a
**soft confirmation** — it never *removes* a today-firing misfire (no regression),
it only refuses a degenerate `cylinder_count` that cannot support a dropout.

### Steps ###

1. `rule_engine.py` — in the masking branch (L274–279), after the hc/o2/nox gate,
   compute `inferred_cyl` per the pinned literal and add `inferred_cyl >= 1` to
   the condition. Carry both citations inline (`§FAULT_IGNITION_MISFIRE`, `§3`).
   `dna` is already in scope at this point (confirm: it is the classify arg).
2. Tests in `GASLab/tests/test_rule_engine.py`.

### Success criteria ###

- `test_misfire_masking_confirmed_with_cylinder_count` — masking gases (hc>1000,
  o2>3, nox<50) + `cylinder_count = 4` → `IGNITION_MISFIRE` (unchanged outcome,
  now via the cylinder-confirmed path).
- `test_misfire_masking_unchanged_across_cylinder_counts` — same gases at
  `cylinder_count ∈ {1, 4, 8, 12}` all → `IGNITION_MISFIRE` (no-regression: the
  conjunct never suppresses a real masking match).
- `test_cylinder_count_read_in_masking_path` — assert (via the behaviour above)
  that `cylinder_count` participates; orphan closed.
- All existing GASLab tests pass (200 GAS-green baseline from T-GV2-12); inner
  loop clean (`ruff` → `pyright` → `pytest -x -q`).

### Files to touch ###

- `GASLab/gaslab/rule_engine.py` (MODIFY — masking-rule cylinder conjunct)
- `GASLab/tests/test_rule_engine.py` (MODIFY — 3 tests above)

### Out of scope ###

- **Emitting `inferred_misfiring_cylinder_count` on the payload.** It is a local
  gate intermediate; emitting it would mint a new output field needing its own
  consumer (signal/noise). The `[v2: q6]` ECU-divergence / Δλ note in 05A is a
  perception-fusion concern (COMLab), not a GASLab emission — out.
- `LEAN_MISFIRE` / `RICH_MISFIRE` discriminators (05A §FAULT_LEAN_MISFIRE /
  §FAULT_RICH_MISFIRE) — different rules, no `cylinder_count` dependency.
- Option (b) slice-narrowing — only if the owner overrides the decision above.

### Harness compatibility ###

No schema-surface change (no field added/removed under option (a)) ⇒ descriptor /
box table untouched, no fixture invalidation.

### Sequencing note (architect) ###

Blocked-by **—** (none). The masking rule and `cylinder_count` field both exist
today; this task is independent of the timing/POA/leak chain. Runnable as soon as
the owner ratifies option (a).
