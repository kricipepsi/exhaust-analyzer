# Generative Test Harness — Proposal & Task Drafts

**Status:** proposal (not registered — confirm §6 before live ledger rows)
**Date:** 2026-06-04
**Scope:** a reusable, pluggable harness consumed by each per-lab forked suite
(GASLab first) and by the full wired suite.
**Relates to:** `PER_MODULE_TESTSUITE_DESIGN_SPEC.md` (the fork model this plugs into).

---

## 1. The gap this closes

The fork model is already established: the full 65-column
`cases_petrol_master_v6.csv` is the **4DLabWired** input contract; each lab gets
a **specialized suite bound to its own input schema** (`DESIGN_SPEC §5–§9`).
GASLab's fork is built (T-GAS-5..15, T-CUR-1).

But every existing suite is a **hand-authored static CSV + a thin diff runner**.
Adding a boundary case, a noise sweep, or asking "do any two fault boxes overlap?"
means hand-editing rows. There is no programmatic capability layer.

This proposal adds that layer: a harness that, given a **module descriptor**
(schema field ranges + fault-box table + entry point + plausible-range spec),
*generates* and *analyses* tests — boundary, combinatorial, noise, overlap,
metamorphic, fuzz, regression — and emits `.md` reports. Each forked suite plugs
in by supplying its own descriptor; the wired suite plugs in by supplying the
composed contract.

## 2. Why this stays inside the architecture (isolation)

The harness lives under `TestSuite/harness/` as **test-only tooling**, not lab
runtime code, so it does not violate "no cross-lab Python imports" (that rule
governs lab runtime codebases importing each other). It is **lab-agnostic**: it
operates only on a `ModuleDescriptor` and the lab's typed JSON boundary. A
GASLab fork importing GASLab is not a cross-lab import; the harness itself
imports no lab. This is the same isolation logic that lets each fork exist.

**Signal/noise discipline (carried over):** every generator ships only with a
**named, existing consumer** — a forked suite that actually runs it. The pilot
consumer is the built GASLab fork; generators are proven there against real box
data before any descriptor rollout to other labs. No generator ships "for later."

## 3. Design (three pieces)

- **`descriptor.py` — `ModuleDescriptor`** (typed): per-field plausible ranges,
  the fault-box table (`{signature: {dim: (min, max)}}`), the entry-point
  callable, and the oracle hook (box-membership for `spec`, recorded-run for
  `characterization`). Each fork supplies one; GASLab's is built from
  `gaslab/contracts.py` + the `ChemicalSignature` box table.
- **`runner.py`** — generic generate → invoke entry point → diff vs oracle →
  collect. Reuses the existing per-module runner's row/diff conventions
  (`gt_method`/`gt_source` governance) so generated cases are first-class.
- **`report.py`** — `.md` emitter (project rule: reports are `.md`). Analytical
  capabilities (overlap, noise) emit reports, not pass/fail gates.

## 4. Test menu

Your two ideas plus higher-leverage additions. "Catches" = the bug class it
actually surfaces; "Consumer" = who runs it.

| Capability | What it does | Catches | Gate or report |
|---|---|---|---|
| **Boundary / edge** (your #1) | per dim per box: `min−ε, min, min+ε, max−ε, max, max+ε`; oracle = box membership | off-by-ε, `>=` vs `>` inclusivity bugs at thresholds | pass/fail gate |
| **t-wise combinatorial** | hyperrectangle corners / pairwise dim combos (full grid explodes → pairwise) | multi-dimension interaction bugs a per-axis sweep misses | pass/fail gate |
| **Box overlap & coverage-gap** | static geometry on the box table: which pairs intersect in feature space, and which plausible regions fall into **no** box | **the discrimination ceiling** — overlapping/ambiguous faults, and unclassifiable holes | report (`.md`) |
| **Noise / fault injection** (your #2) | seeded Gaussian/uniform perturbation around clean centroids; amplitude sweep → degradation curve | brittleness to real-world non-ideal readings | report (`.md`), **not** an inner-loop gate |
| **Metamorphic / monotonicity** | domain relations (↑CO never lowers a rich-fault score; moving toward a centroid never lowers its rank) | directional logic inversions without needing an exact oracle | pass/fail gate |
| **Contract / schema fuzz** | malformed / missing / NaN / out-of-type / out-of-range at the JSON boundary | the boundary itself: crash instead of a typed error | pass/fail gate |
| **Golden-corpus regression** | seeded synthetic corpus snapshot + enumerate label deltas between versions | silent classification drift (generalizes the T-GV2-3 / T-GAS-10 delta discipline) | gate + delta report |

**The one to weight heavily:** *box overlap & coverage-gap*. Boundary and noise
test the **plumbing** (are comparisons correct, is it robust to jitter) — they'll
pass green while the classifier still can't separate two faults whose boxes
overlap. Overlap analysis is static, needs no code run, and points straight at
the ~45% discrimination ceiling that is this engine's actual historical failure
mode. Build the plumbing tests, but this is where projects like this die.

## 5. Proposed tasks (registration-ready)

One capability per task, ≤50% context each, GASLab fork as the pilot consumer.
Foundation first; the two highest-leverage generators next.

| ID | Task | Consumer | Blocked by |
|---|---|---|---|
| **T-TH-0** | Harness core: `ModuleDescriptor` + generic runner + `.md` report emitter; GASLab descriptor built from `contracts.py` + `ChemicalSignature` box table; **parity gate** = replay the existing GASLab CSV through the descriptor, 0 mismatches | GASLab fork | — |
| **T-TH-1** | Boundary / edge-point generator (your #1) | GASLab fork | T-TH-0 |
| **T-TH-2** | Box-overlap & coverage-gap analyzer → `.md` report | GASLab fork + fault-atlas routing | T-TH-0 |
| **T-TH-3** | t-wise combinatorial corner coverage | GASLab fork | T-TH-1 |
| **T-TH-4** | Noise / fault-injection characterization → `.md` degradation report | GASLab fork | T-TH-0 |
| **T-TH-5** | Metamorphic / monotonicity property suite | GASLab fork | T-TH-1 |
| **T-TH-6** | Contract / schema fuzz at the JSON boundary | each fork's input-validation contract | T-TH-0 |
| **T-TH-7** | Golden-corpus regression harness (generalizes delta discipline) | all forks | T-TH-0 |
| **T-TH-8** | Per-lab descriptor rollout (OBD → DTC → VIN → Symptom → COM), one descriptor per session | each per-lab fork | T-TH-0..7; each lab's fork existing |

Deferred / optional:

| ID | Task | Why deferred |
|---|---|---|
| T-TH-9 | Confidence-calibration harness (reliability curve: does higher confidence track correctness?) | needs modules emitting a confidence/score; build once that surface is stable |

**Sequencing:** T-TH-0 → **T-TH-1 + T-TH-2** (prove the highest-value pair on
GASLab) → T-TH-3..7 → T-TH-8 rollout, gated on each other lab's fork existing
(OBD/DTC/DNA/COM forks are still unscoped per `TESTSUITE_PROGRESS §63`).

## 6. Confirm before I register (one fork)

These become atomic ledger rows once confirmed (task file + row written together,
never split). I need one decision:

**Registration home** — register this as its **own pack**
(`TestSuite/harness/HARNESS_START_HERE.md` + `HARNESS_PROGRESS.md` +
`harness/harness_tasks/`, plus a row in the root `CLAUDE.md` bootstrap table),
matching how each per-lab suite gets its own pack — **or** fold these rows into
the existing `TESTSUITE_PROGRESS.md`. Own pack is recommended (keeps the
generative harness separable from the hand-authored CSV suites; same convention
as every other lab pack). Also confirm the pilot consumer = **GASLab fork** and
the T-TH-0 → {1,2} priority order above.
