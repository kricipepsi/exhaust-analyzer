---
name: wired-signal-pack
description: >
  On-demand domain skill for v3 Phase-4 signal packs. Load for any
  `T-V3-P4-C*-{PRE,SYNTH,A,B}` task — the per-cluster lifecycle that adds a new
  discriminating input signal to the wired engine. Covers the frozen reveal
  contract, the provisional-synthetic seeding policy, dry-run simulation
  mechanics (zero-overlay self-check, FT-8 neighbour audit), commit + yardstick
  mint mechanics, and the baseline-pinning rule. Ignoring it produces the two
  known failure modes: laundered synthetic passes presented as real accuracy,
  and dry-runs sized against a stale baseline (the C4A drift).
status: BUILT
---
# wired-signal-pack — the C-pack lifecycle invariants
A signal pack lands one cluster's discriminating signal in four stages. Each
stage is one task; never fold two stages into one task file.
| Stage | Does | Mutates live state? |
|---|---|---|
| `C*-PRE` | instances the frozen reveal contract for the cluster (thresholds cited, consumers named, FT-8 union derived, per-case split) | NO — reports under `v3/` only |
| `C*-SYNTH` | seeds the cluster's cases with provisional synthetic values (side file) | NO — `v3/data/` side file only |
| `C*A` (dry-run) | simulates producer+consumer in memory over the seed; sizes the commit | NO — reports only |
| `C*B` (commit) | writes corpus columns, wires producer/consumer, re-scores, mints yardstick | YES — gated on owner sign-off + FT-8 clean |
## 1. The reveal contract (frozen — instance it, don't re-derive it)
Template: `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md` (T-V3-P4-C2-PRE).
Every pack report carries the five sections: `BUILDABLE_NOW` / `SCORING_GATED` /
`CODE_LANDED != SCORE_MOVED` / `REGRESSION/FT-8` / `ABSTAIN_FALLBACK`.
A pack that reports "threshold implemented" as "cases banked" is dishonest by
definition — the contract exists to force that separation.
## 2. Provisional-synthetic seeding (policy: `4DLab_CLAUDE.md` §Provisional synthetic signals)
- **Grounded, not gamed:** every value derives from the case's ORACLE fault via
  the cluster answer's signature band. The generator's inputs are the oracle
  label + band table, nothing else.
- **NO BACK-SOLVE:** the generator must not read consumer-rule thresholds or the
  case's current rank. State this in the bands report.
- **Tolerance-wide:** sample from a band with realistic spread; the value must
  sit in the correct band robustly across the whole spread, never on a knife-edge.
  State the band + spread per column.
- **Web-corroborated:** widen/shift each band to field-reported reality; cite
  sources. Prefer the wider spread.
- **Grounding-strength tagged, not laundered:** if a band is empirical-anecdotal
  (e.g. C3's Δλ ≥ 0.05, C4's ΔSTFT) say so in the manifest; standardized values
  (DMM voltage drops) are tagged standardized. Weak grounding is disclosed, never
  dressed as textbook.
- **Labelled + correctable:** `synthetic=true` manifest keyed by
  case_id + column + band_id + citation; scoring keeps a synthetic-vs-real split;
  every value findable for replacement when real data lands.
- **Separability is disclosed, not assumed:** cases whose oracle fault the
  cluster's signal cannot separate (confounders — e.g. exhaust-leak / severe-misfire
  mimics for C3) are flagged STAY-ABSTAINED in the seed, not seeded into a pass.
## 3. Dry-run simulation (C*A)
- In-memory overlay on the ACTIVE baseline run JSON — no engine/lab/registry/
  corpus/yardstick mutation.
- **Zero-overlay self-check first:** the sim with no overlay must reproduce the
  baseline exactly (drift = 0) before any scenario is trusted.
- **Outcome buckets (exact vocabulary):** `WOULD_BANK` / `ALREADY_PASS` /
  `STILL_SHORT` / `ABSTAIN_NO_DATA`; per-case table reconciles to the cluster count.
- **FT-8 neighbour audit:** derive the neighbour union LIVE from the touched
  rules' `passes_cases` (both competition groups); report regressions over the
  full 294 — must be empty. Never reuse a previous pack's neighbour list.
- Report scenario ladder (minimal signal → full signal) so the commit's
  column-add decision is sized from evidence.
## 4. Baseline pinning (the C4A lesson)
A dry-run is sized against the CURRENT active yardstick's named run. If any
commit lands between a C*A and its C*B, the C*B must re-baseline (re-run or
re-simulate the deltas) before sizing — a stale-baseline sizing is a blocking
finding. Pin in every task file: yardstick file, csv/oracle hashes, run dir.
## 5. Commit mechanics (C*B)
- Corpus columns land for the pack's cases only; all other rows stay blank.
- Producer state computed in the registry shim / composition path; consumers
  gate on the emitted state; every new field names its consumer
  (`# consumer:` — signal/noise rule).
- **Mint a NEW `V3_YARDSTICK_<date>`** (corpus hash changed); never overwrite a
  prior yardstick; frozen BEFORE stays immutable. `run_suite.py` stays untouched
  (hash-locked).
- Acceptance: `score` + `diff` vs the pinned pre-commit run — `REGRESSIONS: (empty)`
  and no family regressed; run/trace JSON stays git-untracked.
## 6. Standing hard rules (recap — full text in canon)
No `Vault/` edits. No `graphify`/frozen-graph rebuild. No secrets. Abstain dial
stays `MARGIN=0.02` unless the task file says otherwise. Owner runs the final
git commit by explicit path. Unsupplied/ungroundable signal stays abstained.
