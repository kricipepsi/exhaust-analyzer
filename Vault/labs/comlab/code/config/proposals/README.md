# Semantic Proposals Registry

This directory contains the proposals registry for the 4DLab diagnostic engine. This registry provides an open extension mechanism, allowing new faults to be developed and integrated systematically across different lab boundaries.

By keeping the core standard closed while allowing active additions to pass through this registry, we ensure signal-to-noise control without halting forward progress.

---

## 1. Entry Schema

Every proposal added to this registry must be defined in `comlab/config/proposals/entries.yaml` (or as a separate YAML file in this directory) matching the following schema fields:

| Field | Type | Description | Example |
|---|---|---|---|
| `id` | `str` | Unique proposal identifier from the research ledger. | `"EP-OBD-17"` |
| `family` | `str` | Standard family from the `EP-DTC-02` taxonomy backbone. | `"P01XX"` |
| `consumer` | `str` | The file path and symbol (class, function, or method) in code that consumes this fault. | `"comlab/comlab/core/perception_contradiction.py:detect"` |
| `iso_sae_citation` | `str` | The dual-anchor standards citation mapping the fault to standard specifications. | `"ISO 15031-6 §5.6.1 / SAE J2012 — P0130-P0135"` |
| `status` | `str` | The current lifecycle state: `proposed`, `pinned`, or `graduated`. | `"proposed"` |
| `owning_ledger` | `str` | The ledger of the lab that owns and implements the discrimination logic. | `"OBDLab ledger"` |

---

## 2. Graduation Rules

A proposal moves through a three-stage lifecycle before becoming part of the active diagnostic engine:

```
[ proposed ] ────────────────> [ pinned ] ───────────────> [ graduated ]
(Consumer named in proposal)  (Live reader in codebase)    (Shipped, gated & merged)
```

1. **proposed:** The proposal is extracted, has a named target consumer, and is registered in the proposals registry. No logic exists in the codebase yet.
2. **pinned:** A code path has been implemented to parse, reference, or read the proposal's telemetry, meaning the consumer is now a live reader.
3. **graduated:** The proposal passes the `T-SEM-4` conformance gate (validating citations and named consumers), is merged into the live `global_fault_registry.json`, and its status is marked `graduated` (or it is retired from the proposals registry).

---

## 3. Dual ISO/SAE Citation Convention

To maintain standards-traceability, all registry entries must carry a dual-anchor citation in the following style:

* **For DTC-relevant entries (powertrain faults):**
  `ISO 15031-6 §<clause> / SAE J2012 — <P-code range>`
* **For PID-relevant entries (live data/telemetry):**
  `ISO 15031-5 §<clause> / SAE J1979 — <PID>`

---

## 4. Worked Example: Adding a New Fault

To add a new fault (e.g., `EP-OBD-17` Wideband O2 Calibration Offset):

### Step 1: Register the Proposal
Add the entry to `comlab/config/proposals/entries.yaml`:

```yaml
- id: "EP-OBD-17"
  family: "P01XX"
  consumer: "comlab/comlab/core/perception_contradiction.py:detect"
  iso_sae_citation: "ISO 15031-6 §5.6.1 / SAE J2012 — P0130-P0135"
  status: "proposed"
  owning_ledger: "OBDLab ledger"
```

### Step 2: Implement the Consumer (Transition to `pinned`)
In `comlab/comlab/core/perception_contradiction.py`, implement a check that references the proposal's ID:

```python
def detect(payload):
    # Reference to the registered proposal EP-OBD-17
    if payload.obd_live_data.o2_failure_mode == O2FailureMode.WRONG_CENTERLINE:
        # Perform O2 calibration offset verification
        ...
```

The `T-SEM-4` conformance gate will check that the file `comlab/comlab/core/perception_contradiction.py` exists, contains the string `detect` (or `EP-OBD-17`), and matches the registered citation format.

---

## 5. High-Risk Index

The following index maps the high-risk/structural-conflict items identified in the diagnostic engine proposal (§9) to their corresponding proposals registered in this registry:

| High-Risk Item | Description | Mapping Proposals |
|---|---|---|
| **HR-1** | `sensor_fault` component-vs-system conflict | `EP-COM-05` (semantic-coherence), `EP-COM-04` (ECU-hardware checker), `EP-OBD-14` (consistency gates), `EP-OBD-17` (wideband offset) |
| **HR-2** | `lean_condition` / `rich_mixture` cross-layer drift | `EP-COM-05` (semantic-coherence), `EP-COM-03` (lambda delta engine - cross-linked), `EP-COM-15` (truth-perception corpus) |
| **HR-3** | VVT / `cam_timing` calculation strategy separation | `EP-COM-06` (signature matrix), `EP-DTC-02` (standard taxonomy backbone) |
