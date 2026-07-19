# Graph-Trust Audit — make the framed graph trustworthy before wiring
**Pack goal:** before `T-WIRE-1` composes the labs, verify that **every framed
`consumers` / `drift_guards` / `implements` edge** in every framed lab resolves to a
**real code read** — so a coder consulting the Obsidian view (the whole point of the
vault-live pack) can trust it instead of re-deriving from grep every time.

**Why now:** `EVAL-VLIVE-1` (see `../eval/`) showed the framed graph carries drift
the strongest coders only caught by going to code — e.g. `power_loss_analytics`
appears as a DTCLab consumer **8×** across dtclab notes but has **0** DTC references.
Wiring against a map that lies is the failure this pack prevents.

**Lane:** vault-tooling / architect-authoring (map assets). **Mode:** STRICT.
**Method spec:** `T-GTA-METHOD.md` (the per-lab procedure). **Reports:** `reports/<lab>__<agent>.md`.

---
## Classification taxonomy (the ruling that defines "live")
Every framed edge is exactly one of:

- **LIVE** — a real reader of the named field/type/symbol exists in code. **Unit-test-
  only exercise is sufficient pre-wiring**: the live pipeline is `T-WIRE-1`; a reader
  not yet *called* by a pipeline that doesn't exist yet is **expected, not a defect**.
- **MISLABEL** — a reader exists, but consumes **different** fields than the edge
  claims (e.g. `perception_contradiction` reads `rich_dtc_present` (P0172/P0175), not
  the "HistoricalFaultContext / FuelSystemStatus" the edge names). → relabel the edge.
- **ORPHAN** — **no** reader exists at all (e.g. `power_loss_analytics`: 0 DTC refs).
  → repoint to the true reader, or demote the note to `plain` if none exists.
- **PENDING** — reader is an explicitly future task (e.g. `apps/wired/.../composition.py
  (pending T-WIRE-1)`). → keep, with the `(pending …)` marker.

An audit that flags a LIVE-but-unwired consumer as ORPHAN is **wrong** — that
distinction is the crux and the seeded cases below test for it.

## Seeded validation cases (the audit MUST reproduce these)
From `EVAL-VLIVE-1`, verified against code 2026-06-29. Any lab audit that misses
these has a broken method:
- dtclab · `power_loss_analytics.py …` → **ORPHAN** (0 DTC refs; all 8 occurrences).
- dtclab · `perception_contradiction.py HistoricalFaultContext / FuelSystemStatus` →
  **MISLABEL** (real read is `rich_dtc_present`).
- dnalab · `VehicleDNA` readers (`horizon_context_injector.from_vehicle_dna`,
  `projection.project`) → **LIVE** (readers exist + unit-tested; "no live caller" is
  expected pre-wire — must **not** be flagged ORPHAN).

## Cross-check & union (why all three coders run it)
`EVAL-VLIVE-1` showed the models are **complementary** — Agy caught the
`power_loss_analytics` orphan, Claude caught the no-live-caller nuance, Codex found
extra real consumers. So each lab is audited by **all three coders** (Codex, Agy,
Claude), each writing `reports/<lab>__<agent>.md`. Because the audit is **read-only**,
running one task ID on three coders is safe (no edit race) — the redundancy is the
point. `T-GTA-UNION-<lab>` then merges the three reports: an edge flagged ORPHAN/MISLABEL
by **≥1** agent goes to the reconcile list, annotated with **agreement count** (3/3 =
high confidence; 1/3 = verify harder). The union's superset is what the reconcile fixes.

Cost knob: 3× per lab buys depth. If you'd rather buy breadth, partition (one lab per
coder) instead — recommended only for low-risk labs; keep 3× on the wiring-critical maps
(comlab + the gas/obd/dtc emitters + dnalab/vinlab).

## Ledger — single source of truth
The task ledger lives in **`GRAPH_TRUST_PROGRESS.md`** (read by `GRAPH_TRUST_START_HERE.md`).
Do not keep a second ledger here. dtclab is the worked example — combined audit+fix
`T-VLIVE-3c_reconcile_dtclab_drift.md` (**done** 2026-06-29). The remaining labs run
`T-GTA-METHOD.md`, three coders each (`reports/<lab>__<agent>.md`), unioned per lab.

## Success criteria
- Every framed `consumers`/`drift_guards`/`implements` edge in every lab above is
  classified LIVE / MISLABEL / ORPHAN / PENDING in `reports/<lab>__<agent>.md`.
- All ORPHAN edges repointed or demoted; all MISLABEL edges relabeled; PENDING edges
  carry the marker. Zero unclassified.
- The three seeded cases reproduced exactly.
- **Gate:** `T-WIRE-1` should not be marked runnable until dtclab + the emitter labs
  (gas/obd/dtc) + dnalab + vinlab + comlab read GREEN here — those are the maps the
  wiring composes against.
