# T-COMV2-DELTA-2 — Activate `delta_signature` on the v2-registry production path (re-rank consumer)

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4 (COMLab rework). **Type:** COMLab feature (extends an existing field's consumer to a second, production-default code path).
**Origin:** follow-up split out of `T-COMV2-DELTA-1`. DELTA-1 wires `delta_signature` into the **v1** `execute_triage_loop` Phase 5 path; production defaults to the **v2 registry** (`USE_V2_REGISTRY=1`), which **bypasses Phase 5**. So DELTA-1's consumer is live on a real-but-not-default path. This task threads the field into the v2 path so the delta fires on the production default.
**Drill:** read `START_HERE.md` → `ROADMAP.md` → `AGENTS.md` (five rules) → **this file**, then post the scope-confirm before any code.

> **One-line scope:** when a case carries a second operating-point frame, the `delta_signature` already produced by `delta_engine` (DELTA-1) is read by the **v2 registry integration shim's `scored_rules` re-rank** as a primary discriminator, so the delta is honoured on the `USE_V2_REGISTRY=1` default path. Default-off and additive: with the flag off, or with no second frame, the v2 path is byte-for-byte unchanged.

---

## ⚠ Environment — set up before anything (read first)

Use a **3.14 interpreter adapted to your runtime** per `tasks/COMLAB_PYTHON_ENV_SETUP.md`. The mandated `.sandbox-py` is a **Linux ELF** and will not run under native Windows PowerShell — under PowerShell, build the native `.venv-comlab` (section B of that doc); under WSL/bash/sandbox, use `.sandbox-py`. Do **not** fall back to the DTCLab venv. **Green baseline = `0 failed`** (the 2 former `registry`-import failures were fixed by `T-REG-REVIVE-1` — the registry is now live at `labs/comlab/registry/`). If you still see those 2 reds, your interpreter isn't finding the in-lab registry — fix the environment, don't proceed. DELTA-1 is verified green (`progress_notes/DELTA_ENV_VERIFICATION_2026-06-20.md`).

## ⚠ Gate before build — read first

- **Prerequisites both `done`:** `T-COMV2-DELTA-1D` (delta engine live on v1) and `T-REG-REVIVE-1` (registry cleaned). This task is now **runnable** — it consumes the `delta_signature` the DELTA-1 chain produces and wires it onto the v2 path.
- **Registry status:** the v2 registry is live and clean at `labs/comlab/registry/` (importable as `registry`; the former 2 `test_fault_atlas_router_v2` reds pass; `T-REG-REVIVE-1` removed the stale bytecode + empty `ignition_fault` stub). The `ARCHIVE/registry/` copy is a **stale snapshot** — do not import from or edit it.
- **Gate-1 still applies to *live value*.** As with DELTA-1, the delta can only *move accuracy* once two-point cases exist in the corpus (Gate-1, a product decision, still **OPEN**). This task is buildable/testable now against the same synthetic two-point fixtures; it does not rebuild the corpus.

The point of this task is **path coverage**, not new analytics: DELTA-1 made the field live on the v1 path; this makes it live on the v2 default path so it isn't dormant in production.

---

## Goal

1. Read `delta_signature` (typed, from DELTA-1) inside the **v2 registry integration shim** — the layer that, under `USE_V2_REGISTRY=1`, replaces the v1 Phase 5 ranking by re-scoring/re-ordering `scored_rules`.
2. Apply it as the **same primary discriminator** DELTA-1 applies in Phase 5 (single-point static signature stays the fallback), so v1 and v2 paths agree on the delta's effect — no second, divergent delta policy.
3. Keep the **per-signal band policy** identical to DELTA-1: ΔTrim against `STRESS_IDLE` (3500–4500), Δgas/ΔO₂ against `REGULATORY_HIGH_IDLE` (~2500); **ABSTAIN on band mismatch** (frame's `rpm_state_bucket` governs each per-signal check). Do not introduce a different band rule on the v2 path.
4. Gate on **air-metering architecture** before applying profiles, exactly as DELTA-1 (speed-density nulls ΔTrim; forced-induction inverts sign) — the gate lives with the delta logic, shared by both paths, not re-implemented per path.

## Named signal/noise consumer (rule compliance)

The consumer is the **v2 registry integration shim `scored_rules` re-rank** (the production-default ranker), added in this change. Per `AGENTS.md`/CLAUDE.md, this is compliant: it is **proposal-bounded** and the consumer read is live in the same commit. This flips DELTA-1's status from "live on v1 path only" to "live on both paths," closing the dormant-in-production risk recorded against **DEP-14**.

**Own proposal flag — `COMLab-DELTA-V2` (not a reuse of `COMLab-DELTA`).** The v2 re-rank is the production-default ranker, so it carries a larger blast radius than DELTA-1's v1 path. A shared flag would couple the two: flipping `COMLab-DELTA` would activate the reachable v1 path **and** the production default at the same instant, defeating the staged default-off rollout. A separate `COMLab-DELTA-V2` entry lets you enable delta on v1/staging, validate, then enable the production path independently (and roll it back alone). Add `COMLab-DELTA-V2` to `proposals/entries.yaml` **as part of this change** (same commit as the v2 consumer read) — do not pre-create it; an empty-consumer flag in config is the "future use" anti-pattern. Shape it as a sibling of `COMLab-DELTA` (same `family`, `consumer` = the v2 shim re-rank path, `# Reader: T-COMV2-DELTA-2`).

## Dependencies & gates

| Dep | On | Status |
|---|---|---|
| `T-COMV2-DELTA-1D` | delta_engine wired + typed `delta_signature` live on v1 Phase 5 (whole 1A–1D epic done) | **must be `done`** before this is runnable |
| Gate 1 | two-point capture exists in the workflow/corpus | **OPEN** (product) — blocks *live* value on both paths, not the build |
| Emitter two-point emission | labs emit per-state frames at each operating point | **not yet** — needed for live, not for fixture tests |
| Shared delta policy | band policy + architecture gate are shared, not forked per path | enforce in scope-confirm (grep both call-sites read the same helper) |

## Success criteria (done = all of these)

- `delta_signature` is **grep-confirmed read** in the **v2 registry shim's `scored_rules` re-rank** on a live code path reachable with `USE_V2_REGISTRY=1` (the production default). *Green pytest alone is not done — the v2-path read is the gate.* Evidence: one grep showing the read, one showing the re-rank is reached under the v2 default.
- With the proposal flag **off**, every current v2-path verdict is **identical** to pre-change (regression-locked: existing v2 suite unchanged and green).
- With a second frame + flag on, the v2 path reproduces the **same** Δ sign+magnitude decision as the v1 Phase 5 path for each fixture (cross-path parity test: v1 and v2 agree on the same two-point case).
- Band-mismatch **ABSTAIN** and the **architecture null/inversion** cases behave identically on the v2 path (shared helper, not a re-implementation).
- Proposal-bounded under its **own** entry `COMLab-DELTA-V2` (independent of DELTA-1's `COMLab-DELTA`) and **default-off**; flipping the v2 flag is the only behavioural change on the v2 path, and it is separately toggleable from the v1 path.
- Inner loop clean: `ruff check .` → `pyright comlab/` → `pytest -x -q`. Both `VERIFICATION GATE` + `CODE REVIEW` blocks filled in `progress_notes/T-COMV2-DELTA-2.md`.

## Files to touch (additive where possible)

- `labs/comlab/comlab/core/` — the **v2 registry integration shim** (the `scored_rules` re-rank under `USE_V2_REGISTRY=1`): **MODIFY** to read `delta_signature` via the shared delta helper. *Confirm the exact module/function in the scope-confirm before editing — name it in the post.*
- `labs/comlab/comlab/analytics/delta_engine.py` — **REUSE** (no logic change expected); if the band/architecture gate isn't already a callable shared helper, **MINOR REFACTOR** (restructure with no behaviour change) to expose one so both paths call the same code.
- `labs/comlab/comlab/config/proposals/entries.yaml` — **ADD** a new sibling entry `COMLab-DELTA-V2` (consumer = the v2 shim re-rank path; `# Reader: T-COMV2-DELTA-2`). Do **not** edit `COMLab-DELTA` — the two flags stay independent.
- `labs/comlab/tests/unit/test_delta_engine.py` / a v2-path test module — **ADD** cross-path parity + v2 ABSTAIN/architecture cases.
- `labs/comlab/tests/e2e/` — **ADD** a `USE_V2_REGISTRY=1` two-point activation case + a flag-off regression-lock.
- `labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md` — **UPDATE** the DEP-14 Status: v2-path consumer live (drop the "v2-shim activation deferred" note).
- `labs/comlab/tasks/PROGRESS.md` — flip `T-COMV2-DELTA-2` row to `in_progress`/`done`.

## Out of scope (do NOT do here)

- **Building or changing the delta math, schema, or band policy.** Those are DELTA-1; this task only *consumes* the field on a second path. If the v1 and v2 results disagree for a non-architectural reason, that's a DELTA-1 bug — stop and flag, don't patch the policy here.
- **Rebuilding the corpus** to two-point or changing the single-point default (Gate-1 follow-up).
- **Emitter changes** / cross-lab Python imports (mirror types locally per the boundary rule).
- **Changing the registry default** (`USE_V2_REGISTRY`) or other registry behaviour beyond the re-rank read — keep the blast radius at the one re-rank seam.
- Any **graphify / KG rebuild** (frozen — query, don't rebuild).

## Risks / must-design-for

- **Blast radius at the registry boundary.** The re-rank is the production default ranker; an accidental change to its ordering when the flag is off would regress every case. Keep the read strictly additive and gate it on both the proposal flag **and** second-frame presence; the flag-off regression-lock is the proof.
- **Policy fork.** The real failure mode is two slightly different delta policies (v1 Phase 5 vs v2 re-rank) drifting apart. Mitigate by sharing one helper for the band check + architecture gate; the cross-path parity test is the guard.
- **Numeric literals carry a wiki citation** (`# wiki: §…`); any band/tolerance reused here traces to the same `delta-relations` chunk DELTA-1 cited — do not re-derive.

## Verification

```bash
cd labs/comlab
ruff check . && pyright comlab/ && pytest -x -q
# v2-path consumer read is the real gate (name the actual shim module in scope-confirm):
grep -rnI "delta_signature" comlab/core/        # must show a live read in the v2 scored_rules re-rank
# regression lock (v2 default unchanged when flag off):
pytest tests/e2e -q -k "v2_registry and (regression or flag_off)"
# cross-path parity (v1 Phase 5 vs v2 re-rank agree on the same two-point case):
pytest tests -q -k "delta_parity"
```

## On completion

Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-DELTA-2.md`; confirm `delta_signature` is grep-read in the v2 re-rank on a `USE_V2_REGISTRY=1`-reachable path and the flag-off v2 regression is byte-identical; update **DEP-14** Status to "live on both paths"; flip the ledger row → `done`. Then **STOP**. Live activation (two-point corpus + emitter emission) remains the separate Gate-1 follow-up, not this task.
