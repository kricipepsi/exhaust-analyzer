# T-GV2-14 — Bank-asymmetry signatures (`number_of_banks`)

> **STATUS: BLOCKED — signal/noise gate fails. Not coder-runnable.**
> This file is authored so the block is on the record with its exact resolution
> path. The coder must **not** implement it; it stays `blocked` in the ledger
> until the owner decision below lands. (Per `START_HERE.md` step 5:
> "you cannot name a consumer for an added value → STOP and surface.")

### Goal (as carried in the ledger) ###

Implement bank-asymmetry signatures that consume `number_of_banks`
(`dna_view.py:30`, `ge=1, le=4`) — i.e. detect a fault present on one cylinder
bank but not the other (e.g. a single-bank exhaust leak, a per-bank O₂-sensor
bias, a per-bank cam-timing deviation) on a V-engine.

### Why this is blocked (verified — the governing constraint) ###

The single design constraint: *every field/enum value added to any schema must
have a named, existing consumer in COMLab analytics or fault-atlas routing;
"future use" is not a consumer.* Bank-asymmetry fails this on three independent
counts:

1. **The wiki itself labels the field "future."** `01_role_boundaries §` (the
   DNA-ingestion field table, L82) and `GAS_WIKI §1.4` (L80) both map
   `number_of_banks → vin_dna.number_of_banks → "future bank-asymmetry
   signatures"`. The canonical source flags it as not-yet-real — that is the
   textbook "future use," which the constraint explicitly rejects.
2. **No consumer exists in GASLab.** `grep number_of_banks GASLab/` returns a
   single hit: the field definition at `dna_view.py:30`. It is read in **zero**
   live code paths — a standing orphan in GASLab's local DNA slice.
3. **No target `ChemicalSignature` exists.** There is no bank-asymmetry value in
   the v2 enum (`GAS_VOCABULARY §7` / the chemistry-pure roster at
   `10_limited_scope_confidence.md §` L35). Implementing this would require
   minting a **new** enum value — whose *own* consumer would again be "future,"
   compounding the breach rather than resolving it.

A deeper physical point reinforces the block: a single tailpipe 5-gas sample is
the **mixed** exhaust of both banks. GASLab cannot see per-bank asymmetry from
one stabilised-idle sample at all — bank isolation needs either two probes or
per-bank O₂/STFT from OBD, neither of which is a GASLab input. So even with an
enum value, GASLab has no signal to route on.

### What would unblock it (owner decision required — do not guess) ###

Authoring a runnable spec needs the owner to supply **all three**:

1. **A named, existing consumer** — a COMLab analytics function or fault-atlas
   route that reads a GASLab bank-asymmetry output. (None exists today; COMLab's
   `number_of_banks` reads in `horizon_context_injector.py` / `projection.py` /
   `ingestion.py` are VIN-DNA plumbing, **not** a consumer of a GASLab chemical
   verdict.)
2. **The input that carries per-bank signal** — per-bank O₂/STFT or a second
   probe must enter the GASLab contract (a new context input, itself needing a
   consumer and citation). A single tailpipe sample cannot support it.
3. **The output surface** — either reuse an existing enum value with a defined
   per-bank meaning, or ratify a new `ChemicalSignature` *with its consumer named
   up front*.

Until 1–3 are answered, this is a **future-use field with no consumer** and does
not ship. Recommended disposition unless the owner supplies the above: keep
`blocked`, or fold `number_of_banks` into the FU-style follow-up that questions
whether the field should remain in GASLab's local `dna_view` slice at all (it is
fully served by COMLab's own VIN reads).

### If unblocked — provisional scope (for reference only, do NOT implement now) ###

- Files would be `GASLab/gaslab/resolution.py` (+ the new per-bank input on
  `process.py::GasLabContext`) and `GASLab/tests/`.
- Every per-bank numeric literal would carry a `# wiki:` citation to the
  (not-yet-written) bank-asymmetry wiki section — which must be authored first.
- Blocked-by would remain **T-GV2-7** (shares the POA/leaf-routing region) **plus**
  the new input task and the consumer task from the owner decision above.

### Signal/noise consumer ###

**NONE — this is the blocking finding.** No existing COMLab analytics or
fault-atlas code path consumes a GASLab bank-asymmetry output, and the wiki marks
`number_of_banks` "future." Per the constraint, the value does not ship.

### Sequencing note (architect) ###

Ledger Blocked-by is **T-GV2-7** (`done`), but the *real* blocker is the owner
decision above, not a task dependency. Kept in the pack per user direction
("lowest priority; wiki-flagged future, kept per user"); recorded here as
`blocked` rather than `pending` so no coder session picks it up by the
first-unblocked-row rule.
