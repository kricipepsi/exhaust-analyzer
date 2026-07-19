# Architecture Decision Records — VINLab (v2)

**Scope:** VINLab (vehicle-identity channel, Part A of the DNA family).
**Format:** Nygard template (one decision per record, immutable once Accepted).
**Date compiled:** 2026-06-11 — back-filled from the shipped sibling-split rework
(T-RM-2-DNA, T-FX-2, T-FX-5, T-VL-4, T-VL-7).

> These ADRs record decisions already implemented in `vinlab/`. Each captures *why* a
> choice was made, with the task ID that carried it. Future changes supersede an ADR
> with a new one rather than editing it in place.

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0001 | Offline runtime — bake all reference data into `vinlab/data/`, zero MySQL/network | Accepted |
| ADR-0002 | VINLab is a sibling module, not a sub-package of DNALab | Accepted |
| ADR-0003 | No cross-lab Python imports — COMLab mirrors `VinDNA` | Accepted |
| ADR-0004 | Enum-typed `VinDNA` fields replace bare `str` | Accepted |
| ADR-0005 | Single deep air-metering module replaces two parallel switches | Accepted |
| ADR-0006 | Data-driven checksum bypass for non-NHTSA markets | Accepted |
| ADR-0007 | Cylinder-count heuristic is a gated last resort, never an override | Accepted |
| ADR-0008 | Confidence is graded, never fatal — degrade rather than crash | Accepted |
| ADR-0009 | SQL isolation — all SQL lives in `db/tecdoc_query.py` (H8) | Accepted |
| ADR-0010 | `ChassisNumberError` distinguishes wrong-length input from decode failure | Accepted |

---

## ADR-0001: Offline runtime — bake all reference data into `vinlab/data/`

**Status:** Accepted (VINLab hard constraint)

### Context

The decode must run on a technician's device with no guaranteed connectivity. The full
reference corpus lives in MySQL (`mysql_data/`, ~484 MB), but a runtime MySQL/network
dependency is unacceptable on the shop floor.

### Decision

All runtime reference data is baked into `vinlab/data/` at build time: `wmi.csv`,
`years.csv`, `vds_engine_map.csv`, and a small SQLite `vref.db`. The runtime makes
**zero** network and **zero** MySQL calls. `mysql_data/` is retained for build-time
extraction only and is a Track-2 removal candidate.

### Consequences

- **Positive:** decode works fully offline and deterministically.
- **Positive:** tests run without a database server (skip when `vref.db` is absent).
- **Negative:** reference data is a build-time snapshot — staleness is a release
  concern, not a runtime one.
- **Neutral:** the ~484 MB `mysql_data/` copy sits in the tree pending cleanup.

### Alternatives Considered

1. **Runtime MySQL connection.** Rejected: violates the offline constraint.
2. **Bundle the full corpus as SQLite.** Rejected: too large for the device; the
   per-engine-code overlay only needs a slim `vref.db`.

---

## ADR-0002: VINLab is a sibling module, not a sub-package of DNALab

**Status:** Accepted (2026-06-06 — T-RM-2-DNA)

### Context

In v1, VINLab lived inside `DNALab/VINLab/`. The v2 architecture treats the DNA family
as three independently-versioned codebases (`vinlab`, `symptomlab`, `dnalab`) connected
only through typed JSON.

### Decision

VINLab migrated to its own top-level folder with its own `pyproject.toml`. `dnalab`
imports `vinlab` (one-directional, allowed within the family); VINLab imports no other
lab. v1 process history stays in `DNALab/VINLab/` for the Phase-5 archive.

### Consequences

- **Positive:** VINLab builds, tests, and versions on its own.
- **Positive:** the DNA-family import direction is explicit and auditable.
- **Negative:** shared types (e.g. enums) are duplicated as local copies until the
  Phase 0b `comlab.schemas.vocabulary` import swap.

### Alternatives Considered

1. **Keep VINLab nested in DNALab.** Rejected: couples versioning and blurs the
   producer/composer boundary.
2. **One mega-package for the whole DNA family.** Rejected: defeats lab isolation.

---

## ADR-0003: No cross-lab Python imports — COMLab mirrors `VinDNA`

**Status:** Accepted (architecture constraint)

### Context

The 4D architecture keeps each lab a fully isolated codebase connected only through
typed JSON boundaries. COMLab, OBDLab, DTCLab, and GASLab all need data that originates
in `VinDNA`.

### Decision

VINLab **never imports** from another lab, and no other lab imports VINLab — except
`dnalab`, which imports `vinlab` (the one allowed in-family direction). COMLab mirrors
`VinDNA`'s types locally and projects them into per-lab DNA views.

### Consequences

- **Positive:** no import cycles; labs version independently.
- **Negative:** mirrored types can drift from `VinDNA` (e.g. the `UpstreamO2Type`
  member-name divergence reconciled by COMLab-D; the CoC/emissions nesting drift, whose
  VINLab-side shape is now formalized by T-DNA-4 with the projector path fix paired as
  COMLab-C). Sync is a documented manual responsibility.

### Alternatives Considered

1. **Shared `common` enum package.** Rejected: reintroduces the coupling isolation
   exists to remove.
2. **Direct import of COMLab projector types.** Rejected: violates the boundary.

---

## ADR-0004: Enum-typed `VinDNA` fields replace bare `str`

**Status:** Accepted (T-FX-5)

### Context

Early `VinDNA` annotated vocabulary fields as bare `str`. Typos and out-of-vocabulary
values were not caught until far downstream, and the contract §8 vocabulary was not
enforced at the type level.

### Decision

Replace bare `str` annotations with local `StrEnum` types whose members carry the exact
`SEMANTIC_CONTRACT §8` strings (`InductionType`, `FuelDeliveryType`, `AirMeteringStrategy`,
`EuroEmissionCategory`, etc.). `to_json()` coerces members to `.value`, so the wire form
is unchanged; `from_json()` raises on an unknown string.

### Consequences

- **Positive:** invalid vocabulary fails at construction, not downstream.
- **Positive:** the future cut-over to `comlab.schemas.vocabulary` is a one-line import
  swap.
- **Negative:** the enums are presently duplicated in `models.py` rather than imported.

### Alternatives Considered

1. **Keep bare `str` + runtime validators.** Rejected: validation scattered, types
   uninformative.
2. **Import enums from COMLab now.** Rejected: would break the no-cross-lab-import rule
   before Phase 0b.

---

## ADR-0005: Single deep air-metering module replaces two parallel switches

**Status:** Accepted (T-FX-2 — audit candidate #3, "two views of one fact")

### Context

`VinDNA` ships both `primary_load_calculation` (developer label) and
`air_metering_strategy` (OBDLab-canonical). Two separate switch statements computed
these from `(has_maf, has_map)`, so the same physical fact had two code paths that
could disagree.

### Decision

Introduce `overlay/air_metering.classify_air_metering(has_maf, has_map)`, a single deep
module returning a frozen `AirMeteringClassification` with **both** labels from one
classification. The decoder calls it once.

### Consequences

- **Positive:** one source of truth for the air-metering fact; the two labels can never
  disagree.
- **Neutral:** the mapping table is now centralised (both → DUAL/HYBRID, MAF → MAF_ONLY,
  MAP/neither → MAP_ONLY/SPEED_DENSITY).

### Alternatives Considered

1. **Keep two switches, add a consistency test.** Rejected: tests a defect that
   shouldn't be expressible.
2. **Drop one label.** Rejected: both are consumed (developer ergonomics vs OBDLab
   routing).

---

## ADR-0006: Data-driven checksum bypass for non-NHTSA markets

**Status:** Accepted (VINlookup.md §1; exercised by T-FX-5)

### Context

The NHTSA modulo-11 check digit (49 CFR Part 565) is mandatory only for the
US/CA/MX market (ISO 3780). European, Japanese, Korean, and Indian VINs legitimately
omit or dummy the position-9 character, and a batch of Mexican Mazda VINs in the
Slovenian DMV data have corrupt check digits. A strict checksum would reject valid,
in-scope vehicles.

### Decision

`validate_vin_checksum` applies three bypass paths before computing the checksum:
(1) non-NHTSA WMI by `wmi.csv` country, (2) the OPSI corrupt-prefix set
`{3MZ, 3MD, 3MV}`, (3) a non-standard position-9 character (`vin[8] ∉ "123456789X"`).
The bypass is **data-driven** (driven by `wmi.csv`), not hard-coded per VIN.

### Consequences

- **Positive:** valid European/Asian VINs decode; the checksum still guards North
  American VINs.
- **Negative:** a genuinely corrupt non-NHTSA VIN passes structural validation and is
  caught later (or graded down) rather than at the checksum.

### Alternatives Considered

1. **Always enforce the checksum.** Rejected: rejects valid in-scope vehicles.
2. **Always skip the checksum.** Rejected: discards a real integrity signal for North
   American VINs.

---

## ADR-0007: Cylinder-count heuristic is a gated last resort, never an override

**Status:** Accepted (T-VL-7)

### Context

CSV and `vref.db` do not always supply a cylinder count, but downstream routing
(bank-2 contract, UI field gating) needs one. Brand-aware engine-code rules can infer
it — but they must never override authoritative data.

### Decision

`overlay/cylinder_heuristic.infer_cylinder` fires **only** when `cylinder_count == 0`
after CSV + `vref.db`. It returns a `CylinderHint(count=0)` when it cannot resolve, and
the rule table must not be expanded without a follow-up task.

### Consequences

- **Positive:** more vehicles get a usable cylinder count without risking real data.
- **Negative:** heuristic values are lower-confidence; they ride the same `VinDNA` field
  as authoritative values (provenance is in the heuristic's `source`, not on `VinDNA`).

### Alternatives Considered

1. **Always run the heuristic and reconcile.** Rejected: risks overwriting real data.
2. **Leave `cylinder_count = 0` when unknown.** Rejected: breaks bank/UI gating that
   needs a positive count.

---

## ADR-0008: Confidence is graded, never fatal — degrade rather than crash

**Status:** Accepted (T-FX / contract §4.1)

### Context

Reference data is incomplete for parts of the 1990–2020 fleet. A decode that failed
whenever a row was missing would be unusable; but downstream labs must know how much to
trust the profile.

### Decision

Missing/partial data collects **confidence flags** rather than raising. The grade is
`NONE` (engine not in CSV), `PARTIAL` (any downgrade flag), or `HIGH` (clean). Only
genuine scope/structure violations (H1 non-petrol, H2 year, bad charset/checksum, WMI
miss) raise `VINDecodeError`.

### Consequences

- **Positive:** partial profiles still flow downstream, graded honestly.
- **Positive:** OBDLab's three-branch DNA-RPM gate keys off `confidence` directly.
- **Negative:** `PARTIAL` is coarse — a single missing CoC field and a missing engine
  code both read `PARTIAL`; the specific flags are not on `VinDNA`.

### Alternatives Considered

1. **Raise on any missing data.** Rejected: unusable on a real fleet.
2. **Silent best-effort with no grade.** Rejected: downstream cannot calibrate trust.

---

## ADR-0009: SQL isolation — all SQL lives in `db/tecdoc_query.py`

**Status:** Accepted (H8 constraint)

### Context

`vref.db` lookups need SQL, but SQL scattered across modules is hard to audit and to
keep read-only.

### Decision

Every SQL string lives in `db/tecdoc_query.py`. `lookup_engine_ref` opens `vref.db`
read-only via the SQLite `mode=ro` URI and returns rows as plain dicts. No other module
writes SQL (H8).

### Consequences

- **Positive:** one place to audit queries; read-only enforced at the connection.
- **Neutral:** the decoder depends on a thin query layer rather than touching SQLite
  directly.

### Alternatives Considered

1. **Inline SQL in the decoder.** Rejected: violates H8; harder to audit.
2. **An ORM.** Rejected: overkill for a single read query, and adds a dependency.

---

## ADR-0010: `ChassisNumberError` distinguishes wrong-length input from decode failure

**Status:** Accepted (decoder API)

### Context

Pre-standardisation vehicles use chassis/frame numbers that are not 17 characters.
Treating these as ordinary decode failures conflates "this isn't a VIN" with "this VIN
won't decode".

### Decision

A non-17-character input raises `ChassisNumberError`, a subclass of `VINDecodeError`.
Callers can catch the subclass to route legacy identifiers to a separate pipeline;
catching `VINDecodeError` still catches both.

### Consequences

- **Positive:** callers separate "not a VIN" from "bad VIN" without string-matching
  messages.
- **Neutral:** one extra exception type in the public surface.

### Alternatives Considered

1. **One generic `VINDecodeError` for everything.** Rejected: loses the routing
   distinction.
2. **Return a sentinel instead of raising.** Rejected: inconsistent with the rest of
   the validation path, which raises.

---

## References

- `SEMANTIC_CONTRACT.md §4.1, §6.x, §8` — `VinDNA` schema and locked vocabulary.
- `VINlookup.md` / `VINparametres.md` — decode rules and parameter sources.
- `labs/dnalab/tasks/PROGRESS.md` — DNA-family ledger (T-DNA-3/4/5/6 done; dispositions in PRD §8 / HLD §9).
- `docs/decypher.md` — brand cylinder-rule provenance.
- `HLD_VINLab.md` / `DLD_VINLab.md` / `LLD_VINLab.md` — current design surface.
