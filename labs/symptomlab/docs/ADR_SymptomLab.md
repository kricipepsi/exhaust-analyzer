# Architecture Decision Records — SymptomLab (v2)

**Scope:** SymptomLab (operator-symptom channel, Part B of the DNA family).
**Format:** Nygard template (one decision per record, immutable once Accepted).
**Date compiled:** 2026-06-11; refreshed 2026-06-12 — back-filled from the sibling-split
rework (T-RM-2-DNA) and the revised-catalog tasks (T-DNA-1 / reconciled T-DNA-8), with the
`load_state` axis (T-DNA-2) and `will_not_start` rename (T-DNA-10) landed.

> These ADRs record decisions already implemented in `symptomlab/`. Each captures *why*,
> with the task ID that carried it. Future changes supersede an ADR with a new one.

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0001 | SymptomLab produces a prior input, never a routing verdict | Accepted |
| ADR-0002 | Tier vocabulary is open (YAML-validated), not a hard-coded enum | Accepted |
| ADR-0003 | Enforce exactly 18 catalog pairs at construction | Accepted |
| ADR-0004 | Environmental axes are typed enums; tiers are not | Accepted |
| ADR-0005 | SymptomLab is a sibling module with no cross-lab imports | Accepted |
| ADR-0006 | `from_json` validates structure only; `resolve()` owns the catalog invariant | Accepted |
| ADR-0007 | Rework the catalog to remove overlap with the environmental axes | Accepted |

---

## ADR-0001: SymptomLab produces a prior input, never a routing verdict

**Status:** Accepted (architecture constraint; `DNALab_TO_COMLab_FLOW.md §4`)

### Context

The operator's symptom is a cheap, independent signal — but a self-reported symptom is
fallible (research bounds the misleading-report rate near 35%). If SymptomLab emitted
routing (suppress modes, target equation, a fault verdict), the symptom signal would
become an override of the physical evidence.

### Decision

`SymptomDNA` carries **only** the four contract §4.2 fields and **no** routing. All
routing — the symptom→family prior, mode suppression, the context modifiers — lives in
COMLab, where the signal is applied as a **prior** under a trust ceiling (COMLab-B, 65%).

### Consequences

- **Positive:** the symptom channel cannot override physical evidence; the
  truth-vs-perception discipline holds.
- **Positive:** SymptomLab stays a small, pure validator/packager.
- **Negative:** SymptomLab alone produces no diagnosis — its value is realised only when
  COMLab consumes it.

### Alternatives Considered

1. **Emit routing/suppression hints with the symptom.** Rejected: couples the lab to
   COMLab's job and risks the symptom becoming an override.
2. **Emit a tentative fault verdict.** Rejected: that is COMLab's verdict surface.

---

## ADR-0002: Tier vocabulary is open (YAML-validated), not a hard-coded enum

**Status:** Accepted (sibling split, T-RM-2-DNA)

### Context

The symptom vocabulary will grow as the catalog is researched and refined. Encoding tier
strings as a `StrEnum` would make every catalog change a code change with a release.

### Decision

`tier_1_primary_symptom` and `tier_2_subfield_filter` are typed `str`, validated at
runtime against `data/allowed_combinations.yaml`. Adding or renaming a symptom is a data
edit; the code is unchanged. The two **environmental** axes, being a small closed set,
remain typed enums (ADR-0004).

### Consequences

- **Positive:** the catalog evolves without code churn; research can iterate on the
  vocabulary directly.
- **Negative:** tier typos are caught at runtime (validation), not at import — mitigated
  by the actionable error message listing valid options.

### Alternatives Considered

1. **`StrEnum` tiers.** Rejected: turns every vocabulary change into a code change.
2. **No validation (free strings).** Rejected: COMLab's routing map needs a fixed,
   known key set.

---

## ADR-0003: Enforce exactly 18 catalog pairs at construction

**Status:** Accepted (contract §4.2)

### Context

COMLab's symptom→family routing map is keyed by `(tier_1, tier_2)`. If the catalog could
be any size, the routing surface would be unbounded and untestable, and an accidental
drop/duplicate would silently change the diagnosis.

### Decision

`SymptomValidator.__init__` raises `ValueError` unless the catalog defines **exactly 18**
pairs (6 × 3). The check runs at construction, before any triage is validated.

### Consequences

- **Positive:** the routing surface is a fixed, fully-tested 18-key set; accidental
  drift fails fast and loudly.
- **Negative:** a partial catalog edit breaks construction entirely. This was seen
  mid-pack when the live file briefly sat at 17 pairs; T-DNA-8 reconciled it to 18 and the
  invariant now passes. This is the invariant working as designed — surfacing an
  incomplete edit rather than shipping it silently.

### Alternatives Considered

1. **Accept any catalog size.** Rejected: unbounded, untestable routing surface.
2. **Warn instead of raise.** Rejected: a wrong-size catalog would reach production.

---

## ADR-0004: Environmental axes are typed enums; tiers are not

**Status:** Accepted (contract §4.2 / §8)

### Context

`occurs_during`, `engine_state`, and `load_state` are a small, closed, contract-fixed
vocabulary the diagnostic engine branches on directly. The tier vocabulary, by contrast,
is open and growing (ADR-0002).

### Decision

Model the environmental axes as `StrEnum`s (`OccursDuring`, `EngineState`, `LoadState`)
so an out-of-vocabulary value fails at the boundary; keep the tiers as YAML-validated
`str`.

### Consequences

- **Positive:** invalid environmental context is rejected immediately and precisely.
- **Neutral:** two different validation mechanisms in one lab (enum coercion for
  environment, set membership for tiers) — each matched to its vocabulary's nature.

### Alternatives Considered

1. **All strings, all YAML-validated.** Rejected: loses compile-time/type clarity for a
   genuinely fixed set.
2. **All enums.** Rejected: re-couples the open tier vocabulary to code.

---

## ADR-0005: SymptomLab is a sibling module with no cross-lab imports

**Status:** Accepted (2026-06-06 — T-RM-2-DNA)

### Context

In v1, SymptomLab lived inside `DNALab/SymptomLab/`. The v2 DNA family is three
independently-versioned codebases connected only through typed JSON.

### Decision

SymptomLab migrated to its own folder + `pyproject.toml`. `dnalab` imports `symptomlab`
(the one allowed in-family direction); SymptomLab imports no other lab. COMLab mirrors
`SymptomDNA` locally.

### Consequences

- **Positive:** independent build/test/version; explicit, auditable boundary.
- **Negative:** the `SymptomDNA` type is duplicated in COMLab's mirror — sync is a
  documented responsibility.

### Alternatives Considered

1. **Keep it nested in DNALab.** Rejected: couples versioning, blurs the boundary.
2. **Import COMLab's mirror type.** Rejected: violates isolation.

---

## ADR-0006: `from_json` validates structure only; `resolve()` owns the catalog invariant

**Status:** Accepted (models API)

### Context

`SymptomDNA` is both *constructed from user input* (must be catalog-checked) and
*deserialised at the JSON boundary* (already validated upstream). Running the full
catalog check on every deserialise would couple the model to the catalog file.

### Decision

`SymptomDNA.from_json()` checks **field presence + environmental enum membership** only.
The 18-pair catalog invariant is enforced by `SymptomValidator.validate()` / `resolve()`.
DNALab must build symptom records through `resolve()`; `from_json()` is for an
already-validated payload.

### Consequences

- **Positive:** deserialisation is cheap and decoupled from the catalog file.
- **Negative:** a caller that bypasses `resolve()` and hand-builds via `from_json()` can
  construct an off-catalog pair — documented in the `from_json` docstring as a
  contract callers must honour.

### Alternatives Considered

1. **Run the catalog check in `from_json` too.** Rejected: couples the model to the YAML
   and re-validates already-trusted payloads.
2. **Drop `from_json` validation entirely.** Rejected: structural/enum errors must still
   fail at the boundary.

---

## ADR-0007: Rework the catalog to remove overlap with the environmental axes

**Status:** Accepted (T-DNA-1 — research-revised catalog)

### Context

The legacy 18-pair catalog had tier_2 values that duplicated other axes:
`cold_engine_only` / `only_when_hot` duplicated `occurs_during`; `only_high_rpm_highway`
/ `right_after_fillup` duplicated the load axis (now shipped as `load_state`, T-DNA-2).
Duplicated dimensions inflate the routing surface and confuse the prior.

### Decision

Replace the overlapping tier_2 values with discriminating ones and fill gaps (surging
idle, prolonged crank, tip-in hesitation, knock, backfire), keeping the catalog at
exactly 18 pairs. Two tier_1 categories were renamed
(`vehicle_wont_start → vehicle_starting_issues`,
`poor_economy_fuel_odor → poor_economy_fuel_odor_sound`). The revised strings have no
live consumer yet, so the routing map ships as **proposal COMLab-A**.

### Consequences

- **Positive:** each tier_2 carries independent signal; the environmental axes own the
  thermal/load dimensions.
- **Negative:** the rename is a breaking vocabulary change COMLab-A must absorb. The
  catalog edit was completed by T-DNA-8 (now 18/18); the invariant passes.

### Alternatives Considered

1. **Keep the legacy catalog.** Rejected: dimensional overlap corrupts the prior.
2. **Expand beyond 18 pairs.** Rejected: breaks the fixed-surface invariant (ADR-0003).

---

## References

- `SEMANTIC_CONTRACT.md §4.2, §8` — `SymptomDNA` schema and environmental vocabulary.
- `VehicleDNA.md` — the triage diagram (the catalog's source).
- `DNALab_TO_COMLab_FLOW.md §4` — routing is COMLab-owned.
- `labs/dnalab/tasks/PROGRESS.md` / `docs/research/DNAresearch.md` — revised catalog +
  `load_state` (T-DNA-1, T-DNA-2) and the 65% trust ceiling.
- `HLD_SymptomLab.md` / `DLD_SymptomLab.md` / `LLD_SymptomLab.md` — current design surface.
