---
node_type: "wiki"
lab: "dtclab"
module: "dtclab"
subsystem: "turbo-gdi-routing"
implements:
  - "labs/dtclab/dtclab/config/routing_tag_map.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py DTCRoutingTag routing"
drift_guards:
  - "labs/dtclab/tests/unit/test_routing_tag_mapper.py"
tags: [dtclab, finished, wiki]
source: "labs/dtclab/wiki/08_forced_induction_gdi.md"
---
# 08 — Forced-induction & GDI DTCs (v2, new)

Domain reference, new in v2. Sources: `DtcDoc.md`, `DtcDoc2.md`. Turbo and GDI
petrol are **in scope** (petrol, 1990–2010 — both technologies predate 2010).
Post-2010 / Euro 6+ content (GPF differential-pressure P2452, Low-Speed
Pre-Ignition P0324/LSPI) is **out of scope** and removed — see
`11_proposals_register.md §11.4`. Diesel and hybrid-drive logic remain out of
scope. See `00_INDEX.md`.

---

## 8.1 Era framing

`DtcDoc2.md` classifies the corpus by architecture; within the **1990–2010**
scope there are **two in-scope eras**, which set what hardware (and therefore
which DTC families) a vehicle can carry:

| Era | Years | Fuel/air & after-treatment | New DTC families |
|---|---|---|---|
| A | 1990–2000 | Port FI, narrowband Zr O₂, simple TWC, K-Line/J1850 | early P0xxx, immobiliser PATS/Passlock |
| B | 2000–2010 | Port FI **and early GDI/TGDI + forced induction**, VVT, upstream wideband O₂, dual-bed TWC, CAN | P0011/P0016 (VVT), P0455 (EVAP decay), P0128; P0087/P0090/P0191 (GDI rail), P0234/P0299 (boost) |

> The original `DtcDoc2.md` era-C bucket (2010–2020: GPF, dual-injection,
> Euro 6+) is **out of the 1990–2010 scope**. GDI and forced induction are *not*
> era-C-only — both reached production well before 2010, so they stay (in era B);
> only the genuinely post-2010 tech (GPF P2452, LSPI P0324) is dropped.

This era tag is a **context prior**, not a verdict; it bounds which monitors and
codes are physically possible. (Cross-lab: the era prior is shared with the
OBDLab taxonomy chunk.)

---

## 8.2 Forced induction — boost faults

| DTC | Name | Reading |
|---|---|---|
| P0234 | Turbocharger/supercharger overboost | Actual boost exceeds target ceiling; charge-pipe split downstream of compressor can run the engine physically rich under boost |
| P0299 | Turbocharger/supercharger underboost | Actual boost below target; wastegate stuck open, BOV/diverter diaphragm rupture, or charge leak |

**Idle-centric note.** At stress idle (≈ 4000 RPM, no road load) boost should be
minimal, so a boost fault may not express at idle. Under a snap-throttle event
MAP should rise toward the boost ceiling and MAF should exceed ≈ 40× displacement
(g/s); failure to rise indicates an induction leak or turbo failure. Boost
verdicts are load-dependent and largely outside the idle window — DTCLab passes
the code and the Mode `$06` MID `$71` (boost control) deviation through; COMLab
decides.

---

## 8.3 GDI / TGDI high-pressure fuel system

Camshaft-driven High-Pressure Fuel Pumps (HPFP) raise rail pressure to the
hundreds-of-bar range GDI injectors need. Failure modes:

| DTC | Name | Reading |
|---|---|---|
| P0087 | Fuel rail/system pressure too low | HPFP cannot reach target high pressure; rail stuck near low-feed pressure |
| P0090 | Fuel pressure regulator 1 control circuit | HPFP spill-valve solenoid open circuit; pump cannot trap fuel |
| P0191 | Fuel rail pressure sensor performance | Rail-pressure sensor reference drift (can falsely report high pressure ⇒ pump commanded near-off ⇒ no-start) |

A leaking HPFP seal can also dilute engine oil with fuel, drawn back through the
PCV — producing strongly negative trims with a P0172/P0087 pair (`DtcDoc2.md`
EXP-N013).

---

## 8.4 Combustion-anomaly / oil-source DTCs

| DTC | Name | Reading |
|---|---|---|
| P250C | Engine oil level too low | Oil-burning / mechanical-source HC (POA signature) — see chunk `09` |

> **Out of scope (post-2010 / Euro 6+):** GPF differential-pressure **P2452**
> (Gasoline Particulate Filter, Euro 6c+, 2017/2018+) and **Low-Speed
> Pre-Ignition (P0324/LSPI)** are post-2010 phenomena outside the 1990–2010
> scope and are not covered here — see `11_proposals_register.md §11.4`. (The
> generic knock-control code P0324 is still readable as a code token; only its
> LSPI interpretation is dropped — see chunk `06`.)

## Graph relations (explicit)

**P0234** ROUTES_TO **DTCRoutingTag.BOOST_HISTORY**
**P0299** ROUTES_TO **DTCRoutingTag.BOOST_HISTORY**
**P0235** through **P0245** ROUTES_TO **DTCRoutingTag.BOOST_HISTORY**
**P0087** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0090** ROUTES_TO **DTCRoutingTag.INJECTOR_HISTORY**
**P0191** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P250C** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**DTCRoutingTag.BOOST_HISTORY** MAPS_TO **None** family
**Era A** BOUNDS **port injection**, **narrowband O₂**, **PATS**
**Era B** BOUNDS **GDI**, **turbo/forced induction**, **wideband O₂**, **CAN**

## Core Entities

- **P0299** — Confirmed DTC indicating Turbocharger/Supercharger Underboost. Consumer: `dtclab/config/routing_tag_map.yaml`.
- **P0087** — Confirmed DTC indicating Fuel Rail/System Pressure Too Low. Consumer: `dtclab/config/routing_tag_map.yaml`.
- **P0191** — Confirmed DTC indicating Fuel Rail Pressure Sensor Circuit Range/Performance. Consumer: `dtclab/config/routing_tag_map.yaml`.
- **Era A** — Contextual fleet era covering 1990–2000. Consumer: COMLab/OBDLab taxonomy.
- **Era B** — Contextual fleet era covering 2000–2010. Consumer: COMLab/OBDLab taxonomy.

