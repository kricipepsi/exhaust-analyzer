# Oil-Burn Diagnostic — 5FR Simulation Results (presentation)

**Vehicle:** `VF7SA5FR8AW511081` · Citroën · **5FR / EP6CDT** · 1.6 L · **turbo + GDI** · EURO 5.
**ECU model:** Bosch MED17.4 with **secondary (post-cat) fuel-trim control** on the downstream sensor.
**Sensor config:** *Modern Standard* — **wideband upstream (S1) + narrowband downstream (S2)** (per `5fr.md`, `O2NBvsWB.md`).
**What this is:** a **standalone simulation** (`oil_burn_5fr_sim.py`) that mocks the post-cat-trim-enabled pipeline. It is **not** wired into the real labs — it demonstrates the intended end-state that tasks **PCT-1…PCT-10** implement for real.

---

## Result: 5 / 5 cases route correctly

| Case | GAS chemical state | Post-cat B1S2 signature | Verdict | Conf |
|---|---|---|---|---|
| Worn piston rings | WORN_PISTON_RINGS | FIXED_NEGATIVE (LTFT-B1S2 steady neg, all RPM) | **MW-001** | 0.88 |
| Worn valve stem seals | WORN_VALVE_SEALS | TRANSIENT_NEGATIVE (sharp neg STFT-B1S2 at idle) | **MW-002** | 0.90 |
| Blown head gasket | COOLANT_LEAK_INTERNAL | NEUTRAL (gas + ECT>95 drive it) | **MW-003** | 0.93 |
| PCV stuck open | POA_SIGNATURE | **DIVERGENT** (upstream +, downstream −) | **MW-008** | 0.90 |
| Turbo turbine-seal leak | POA_SIGNATURE | **DFCO_NEGATIVE** (B1S2 pinned rich on fuel-cut) | **MW-009** | 0.91 |

### Demand ranking (which case stresses the pipeline most)

The simulation scores each case by how many evidence channels it needs and how ambiguous its gas family is — to help pick the single presentation case:

| Rank | Demand | Case | Why |
|---|---|---|---|
| 1= | **4.0** | PCV stuck open (MW-008) | ambiguous POA family + requires the **simultaneous** upstream(+)/downstream(−) divergent split |
| 1= | **4.0** | Turbo turbine-seal (MW-009) | ambiguous POA family + requires **DFCO** fuel-cut capture, decoupled from combustion |
| 3 | 3.5 | Worn piston rings (MW-001) | needs post-cat B1S2 + historic cross-lab conflict (low-idle HC vs rule) |
| 4 | 2.0 | Worn valve stem seals (MW-002) | needs post-cat B1S2 |
| 5 | 1.0 | Head gasket (MW-003) | routes on gas + ECT alone |

The most demanding cases (PCV, turbo) are the strongest showcases — they **cannot** be diagnosed by gas chemistry alone; post-cat trim is what makes them resolvable.

The post-cat B1S2 trim is what lets the two previously-unroutable cases land cleanly:
**PCV** is the classic *divergent split trim* (upstream swings positive while downstream goes negative), and **turbo seal** is the *decoupled DFCO negative trim* (downstream stays rich even when fuel is cut). Gas chemistry alone could not separate these two from the rings family — post-cat trim is the discriminator.

---

## Why post-cat trim is the key

```
 engine ─> [WIDEBAND upstream S1] ─> catalytic converter ─> [NARROWBAND downstream S2]
              primary fuel loop                                 SECONDARY fuel-trim loop
                                                                (B1S2 STFT / LTFT)
   oil in exhaust → low O2 at S2 → false-rich → ECU pulls fuel → NEGATIVE B1S2 trim
```

Per the Bosch MED17.4 strategy, burning oil starves O₂ at the post-cat sensor, which reads false-rich, so the ECU commands a **negative** post-cat trim. *Where* and *how* the oil enters changes the pattern (steady vs transient vs divergent vs fuel-cut) — that pattern is the per-failure fingerprint.

---

## Sensor-config coverage (the "both O₂ types" requirement)

The data model must represent the sensor at **each position** plus the trim role. Three real configs exist (`O2NBvsWB.md`):

| Config | Upstream | Downstream | Example |
|---|---|---|---|
| Traditional | narrowband | narrowband | older cars |
| **Modern Standard ← 5FR** | **wideband** | **narrowband** | most modern GDI |
| Premium | wideband | wideband | BMW / Mercedes / Subaru |

> Data fix implied: `vref.db` currently stores a single `o2_type='NB'`, which is wrong for the 5FR upstream. The real model needs `upstream_o2_type=WIDEBAND`, `downstream_o2_type=NARROWBAND`, `downstream_trim_role=SECONDARY_FUEL_TRIM` (handled in PCT-4).

---

## How to run (for the demo)

```bash
python3 planning/sim/oil_burn_5fr_sim.py
```

Prints the engine identity, the 5-case routing table (5/5 PASS), and the per-case gas + B1S2 reasoning. Pure Python, no dependencies, no labs import — safe to run live.
