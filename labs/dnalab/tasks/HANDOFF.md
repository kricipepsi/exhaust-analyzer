# DNA family — HANDOFF (next session pickup)

_Written 2026-06-11 (architect). Read alongside `DNA_TASKS_START_HERE.md` + `PROGRESS.md`._

## Wiki authored — 2026-06-12 (architect)

`dnalab/wiki/` is now a full **dual-disposition** wiki (matching the symptomlab/vinlab
build), not just a landing index:

- **OWNED half** (`10`–`13`, `role: reference-only`, no measured numbers): VehicleDNA
  envelope, schema versioning + version guard, assembly contract, session identity —
  mirrors live `models.py`/`assembly.py`. Leak-checked: zero empirical numbers.
- **RESEARCH half** (`90`–`94`, `role: research-evidence`): the operator-symptom + VIN
  channel evidence from `../answersDNA.md`. Every number carries `# source:` **and**
  `routes-to: COMLab-…` — the numbers' real home is the COMLab proposals registry, not
  `dnalab/`. `00_index.md` states the boundary rule that keeps the two halves apart.
- **Deferred, marked-down only:** output dataset → two-tier `full`|`basic` (retire
  `PARTIAL`). See `../research/DEFERRED_full_basic_dataset_decision.md`; the VIN-decode
  evidence in wiki `93` is its empirical basis. Needs its own research + a named COMLab
  consumer before any task.

## Where the pack stands

Done: T-DNA-1, T-DNA-2 (`load_state` landed), T-DNA-3 (`rated_rpm` emitted).
Pending (run in ledger order, one per session): **T-DNA-4 → T-DNA-5 → T-DNA-6 → T-DNA-7**.
Deferred to a **final cleanup session** (owner decision — not mid-pack): **T-DNA-8**,
**T-DNA-9**, and the **doc-set refresh**.

## Do this in the FINAL cleanup session (after T-DNA-4..7 are all done)

1. **T-DNA-8 — reconcile the symptom catalog to 18 pairs.**
   The live `symptomlab/data/allowed_combinations.yaml` is **17 pairs** (mtime
   2026-05-22): `visible_exhaust_smoke = {black_smoke, blue_oily}`. It is missing
   `white_sweet_smell` and still uses legacy `blue_oily`. T-DNA-1 was flipped `done` with
   its note claiming "18 pairs", but the file was never edited — a stale-ledger +
   unmet-deliverable condition. Because `SymptomValidator` hard-requires exactly 18,
   this currently raises at construction and breaks the whole symptom path (and DNALab
   tests that build a validator transitively). Full spec:
   `T-DNA-8_reconcile_symptom_catalog.md`. Target block:
   ```yaml
     visible_exhaust_smoke:
       - black_smoke
       - blue_oily_smell      # was blue_oily
       - white_sweet_smell    # ADD
   ```
   Confirm COMLab-A's 18 keys match (anti-orphan set-equality), and update the
   `VehicleDNA.md` triage diagram strings.

   > ⚠️ Sequencing tension to keep in mind: T-DNA-7's round-trip gate (and any DNALab
   > pytest) constructs the validator, so while the catalog sits at 17 pairs those gates
   > cannot pass cleanly. The owner has chosen to fix it last; if a pending task's gate
   > blocks on it sooner, run T-DNA-8 first instead.

2. **T-DNA-9 — add `oil_consumption` (owner-requested future symptom).**
   Common symptom mapping to 5–6 faults (worn piston rings, valve-stem seals, turbo
   oil-seal, PCV fault, guide wear). **Open design decision before coding:** the catalog
   is hard-capped at 6 tier_1 × 3 tier_2 = 18, so adding it needs a disposition —
   - a new 7th tier_1 `oil_consumption` (→ raise the validator invariant to 21), or
   - a new tier_2 under an existing tier_1 (note `blue_oily_smell` under
     `visible_exhaust_smoke` already partly covers oil-burning; "consumption without
     smoke" — worn rings — may warrant its own entry).
   Name the COMLab-A consumer mapping for each oil-consumption pair → fault family.
   Blocked-by T-DNA-8 (don't touch the catalog twice).

3. **Doc-set refresh (single pass).**
   The per-lab `docs/` sets authored 2026-06-11 captured the then-live code. The pack has
   since closed gaps the docs flagged as open:
   - SymptomLab: `load_state` is now **shipped** (T-DNA-2), not "proposed" — update
     `EnvironmentalConditions` (3 axes), `SymptomDNA`, the `resolve()` signature, and the
     vocabulary file. Also drop the 17/18 "known gap" once T-DNA-8 lands.
   - VINLab: `rated_rpm` is now **emitted** (T-DNA-3) — flip it from "gap" to live in
     HLD §7/§9, PRD, and `VIN_VOCABULARY.md`. Re-check CoC/`emissions` (T-DNA-4),
     `model` (T-DNA-5), `fuel_type` (T-DNA-6) once those land.
   - DNALab: bump the doc `schema_version` references to `1.1` after T-DNA-7.

## One rule to keep in your head

Signal/noise: every new catalog string / field needs a **named** COMLab consumer (live
or a registered proposal). `oil_consumption` ships as a COMLab-A proposal extension, not
silently into the live schema.
