---
node_type: "wiki"
lab: "vinlab"
module: "vinlab"
subsystem: "brand-cylinder-rules"
implements:
  - "labs/vinlab/vinlab/overlay/cylinder_heuristic.py"
consumers:
  - "vinlab: labs/vinlab/vinlab/overlay/cylinder_heuristic.py infer_cylinder"
drift_guards:
  - "labs/vinlab/tests/unit/test_cylinder_heuristic.py"
tags: [vinlab, finished, wiki]
source: "labs/vinlab/wiki/12_brand_cylinder_rules.md"
---

# 12. Brand Cylinder Rules

> **What this page owns.** The per-manufacturer engine-code → cylinder-count rules
> that the cylinder fallback (page 11, §11.5) dispatches to. The research draft
> `decypher.md` is the **raw source**: an exploratory, partly-inconsistent decoding
> tree that also wanders into out-of-scope brands and diesel. This page is the
> **clean, shipped distillation** — exactly the rules implemented in
> `cylinder_heuristic.py`, brand by brand. When `decypher.md` and the code disagree,
> the code (and therefore this page) wins; `decypher.md` is kept only for lineage.

**Scope reminder.** Every rule here fires **only** when `cylinder_count == 0` after
CSV and `vref.db` lookups (page 11) — it never overrides authoritative data. A
brand with no rule below (or any unmatched code) falls through to the
displacement-band table on page 11. Induction defaults to `NATURALLY_ASPIRATED`
unless a rule promotes it to `TURBOCHARGED`.

## 12.1 Brand dispatch table {#RULE_DISPATCH}

`infer_cylinder` looks the (upper-cased) brand up in `_BRAND_DISPATCH`; a hit calls
that brand's rule, a miss uses the displacement fallback. The dispatched brands:

| Brand keys | Rule |
|---|---|
| `BMW` | §12.2 |
| `HYUNDAI`, `KIA` | §12.3 |
| `HONDA` | §12.4 |
| `TOYOTA` | §12.5 |
| `VOLVO` | §12.6 |
| `MERCEDES`, `MERCEDES-BENZ`, `MERCEDES BENZ` | §12.7 |
| `VOLKSWAGEN`, `AUDI`, `SKODA`, `SEAT` | §12.8 |
| `NISSAN` | §12.9 |
| `MITSUBISHI` | §12.10 |
| `MAZDA` | §12.11 |
| `SUBARU` | §12.12 |
| `RENAULT`, `DACIA` | §12.13 |
| `PEUGEOT`, `CITROEN` | §12.14 |

`# source: cylinder_heuristic.py — _BRAND_DISPATCH`

## 12.2 BMW {#RULE_BMW}

Engine codes match `[NBMS](\d)(\d)…`; the **first of the two digits** (the "tens"
digit) encodes cylinders:

| Tens digit | Count | Config |
|---|---|---|
| 2 | 4 | `I4` |
| 4 | 4 | `I4` |
| 5 | 6 | `I6` |
| 6, 7 | 8 | `V8` |
| 8 | 12 | `V12` |
| 3 or other | displacement fallback | — |

For numeric-first codes (`code[1]` and `code[2]` are digits), displacement is the
signal: `disp <= 2.0 → I4`; `disp >= 4.0 → V8`; otherwise `I6`.

**BMW turbo families** (induction → `TURBOCHARGED`): `N54`, `N55`, `B58`, `S55`,
`S63`. Any `I3` config is also treated as turbo (modern small-displacement engines
are nearly all turbo).

`# source: cylinder_heuristic.py — _infer_bmw, _is_turbo_bmw`

## 12.3 Hyundai / Kia {#RULE_HYUNDAI_KIA}

Codes match `G(\d)…`; the digit after `G` is the cylinder count when it is one of
`{3, 4, 6, 8}` → `I{count}`. Otherwise displacement fallback. Induction `NA`.

`# source: cylinder_heuristic.py — _infer_hyundai_kia`

## 12.4 Honda {#RULE_HONDA}

J-series checked first: `J\d…` with `disp >= 3.0 → V6`. The generic Honda I4 family
is the prefix set `D, B, F, K, R, J, L` (`[DBFKRJL]\d…`) → `I4`. Induction `NA`.

`# source: cylinder_heuristic.py — _infer_honda`

## 12.5 Toyota {#RULE_TOYOTA}

The family prefix is taken from the code (leading digits stripped) and looked up in
fixed sets:

| Set | Members | Count | Config |
|---|---|---|---|
| `_TOYOTA_I4` | `AZ, NR, NZ, ZZ, QR, AR` | 4 | `I4` |
| `_TOYOTA_V6` | `GR, VZ, JZ, MZ` | 6 | `V6` |
| `_TOYOTA_V8` | `UZ` | 8 | `V8` |

No match → displacement fallback. Induction `NA`.

`# source: cylinder_heuristic.py — _infer_toyota, _TOYOTA_I4/V6/V8`

## 12.6 Volvo {#RULE_VOLVO}

Codes match `B(\d)…`; the digit after `B` is the cylinder count (valid `3–8`).
Config is `I5` for 5, `I6` for 6, else `I{count}`. A **`T` suffix** on the code
sets induction `TURBOCHARGED`; otherwise `NA`.

`# source: cylinder_heuristic.py — _infer_volvo`

## 12.7 Mercedes-Benz {#RULE_MERCEDES}

Codes match `M\d{3}` and are looked up in the engine-family table:

| Family | Count | Config | | Family | Count | Config |
|---|---|---|---|---|---|---|
| `M111` | 4 | `I4` | | `M113` | 8 | `V8` |
| `M271` | 4 | `I4` | | `M273` | 8 | `V8` |
| `M166` | 4 | `I4` | | `M278` | 8 | `V8` |
| `M112` | 6 | `V6` | | `M104` | 6 | `I6` |
| `M272` | 6 | `V6` | | `M275` | 12 | `V12` |
| `M276` | 6 | `V6` | | `M279` | 12 | `V12` |
| | | | | `M137` | 12 | `V12` |

No match → displacement fallback. Induction `NA`.

`# source: cylinder_heuristic.py — _infer_mercedes, _MERCEDES_TABLE`

## 12.8 Volkswagen / Audi / Škoda / Seat {#RULE_VW_AUDI}

Alpha-code prefixes are unreliable for this group, so the rule is **displacement
fallback** (page 11 bands) with brand-aware induction applied on top (`I3` → turbo).
This is a deliberate choice from the T-VL-7 notes, not a gap.

`# source: cylinder_heuristic.py — _infer_vw_audi`

## 12.9 Nissan {#RULE_NISSAN}

Two-letter prefix lookup:

| Set | Members | Count | Config | Induction |
|---|---|---|---|---|
| `_NISSAN_I4` | `GA, CA, CR, QG, SR, HR, MR` | 4 | `I4` | `NA` |
| `_NISSAN_V6` | `VQ, VK` | 6 | `V6` | `NA` |
| `_NISSAN_TURBO_I4` | `TB` | 4 | `I4` | `TURBOCHARGED` |

No match → displacement fallback.

`# source: cylinder_heuristic.py — _infer_nissan`

## 12.10 Mitsubishi {#RULE_MITSUBISHI}

The **leading digit** is the cylinder count (`4G…` → 4, `6G…` → 6): `3, 4 → I{n}`;
`6 → V6`; `8 → V8`. No match → displacement fallback. Induction `NA`.

`# source: cylinder_heuristic.py — _infer_mitsubishi`

## 12.11 Mazda {#RULE_MAZDA}

Prefix `[BFKP]\d…` → `I4`, induction `NA`. Otherwise displacement fallback.

`# source: cylinder_heuristic.py — _infer_mazda`

## 12.12 Subaru {#RULE_SUBARU}

Two-letter prefix → boxer configuration:

| Set | Members | Count | Config |
|---|---|---|---|
| `_SUBARU_BOXER_4` | `EJ, FA, FB, EE` | 4 | `BOXER_4` |
| `_SUBARU_BOXER_6` | `EZ` | 6 | `BOXER_6` |

No match → displacement fallback. Induction `NA`.

`# source: cylinder_heuristic.py — _infer_subaru, _SUBARU_BOXER_4/6`

## 12.13 Renault / Dacia {#RULE_RENAULT}

Family lookup on the `[A-Z]\d[A-Z]` head:

| Set | Members | Count | Config |
|---|---|---|---|
| `_RENAULT_I4` | `K4M, H4M, K9K, F4R, F4P, K4J` | 4 | `I4` |
| `_RENAULT_I3` | `H5F, D4F, H4Bt` | 3 | `I3` |

No match → displacement fallback. Induction `NA`.

`# source: cylinder_heuristic.py — _infer_renault, _RENAULT_I4/I3`

## 12.14 PSA (Peugeot / Citroën) {#RULE_PSA}

Two prefix patterns both resolve to `I4`: legacy `[EX][USW]…` (e.g. `XU`, `ES`,
`EW`) and modern `[EP][FWS]…` (EP/EW families). Otherwise displacement fallback.
Induction `NA`.

`# source: cylinder_heuristic.py — _infer_psa`

## 12.15 Lineage note — decypher.md vs shipped code {#RULE_LINEAGE}

`decypher.md` is an exploratory research draft generated against a 1,630-row engine
corpus. It contains material that is **not** part of the shipped rule set and must
not be read as authoritative:

- Out-of-scope brands (Ford, GM/Chevrolet/Opel, Chrysler/Dodge/Jeep) — absent from
  `_BRAND_DISPATCH`; the EU petrol corpus does not need them, so they fall through
  to the displacement bands.
- Diesel families and `MEDIUM`/`LOW` "confidence" notes — VINLab is petrol-only
  (page 10, §10.4) and the cylinder hint carries a `source` tag, not a confidence.
- A truncated demonstration script — illustrative only; the real logic is the
  `_infer_*` functions transcribed above.

Treat this page as the truth and `decypher.md` as the provenance trail behind it.
Extending any brand rule (new family member, new brand) is a follow-up task, not an
inline edit — the rule tables are intentionally closed.

## Graph relations (explicit)

**VINWIKI-12-BRAND_CYLINDER_RULES** DESCRIBES **_BRAND_DISPATCH**
**vinlab.overlay.cylinder_heuristic.infer_cylinder** CONSUMES **_BRAND_DISPATCH**
**vinlab.overlay.cylinder_heuristic.infer_cylinder** CONSUMES **_displacement_fallback**
**vinlab.overlay.cylinder_heuristic._infer_bmw** CONSUMES **BMW cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_hyundai_kia** CONSUMES **Hyundai/Kia cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_honda** CONSUMES **Honda cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_toyota** CONSUMES **Toyota cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_volvo** CONSUMES **Volvo cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_mercedes** CONSUMES **Mercedes-Benz cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_vw_audi** CONSUMES **Volkswagen/Audi/Skoda/Seat displacement rule**
**vinlab.overlay.cylinder_heuristic._infer_nissan** CONSUMES **Nissan cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_mitsubishi** CONSUMES **Mitsubishi cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_mazda** CONSUMES **Mazda cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_subaru** CONSUMES **Subaru cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_renault** CONSUMES **Renault/Dacia cylinder rule**
**vinlab.overlay.cylinder_heuristic._infer_psa** CONSUMES **PSA cylinder rule**
**labs/vinlab/tests/unit/test_cylinder_heuristic.py** VERIFIES **vinlab.overlay.cylinder_heuristic.infer_cylinder**
**decypher.md** LINEAGE_ONLY_FOR **VINWIKI-12-BRAND_CYLINDER_RULES**

## Core Entities

- **_BRAND_DISPATCH** - Upper-cased brand to rule-handler dispatch map. Consumer: `vinlab.overlay.cylinder_heuristic.infer_cylinder`.
- **_displacement_fallback** - Last-resort displacement-band fallback used only when brand rules do not resolve. Consumer: `vinlab.overlay.cylinder_heuristic.infer_cylinder`.
- **BMW cylinder rule** - BMW engine-code and turbo-family inference. Consumer: `vinlab.overlay.cylinder_heuristic._infer_bmw`.
- **Hyundai/Kia cylinder rule** - `G` digit cylinder inference. Consumer: `vinlab.overlay.cylinder_heuristic._infer_hyundai_kia`.
- **Honda cylinder rule** - J-series V6 and generic Honda I4 inference. Consumer: `vinlab.overlay.cylinder_heuristic._infer_honda`.
- **Toyota cylinder rule** - Toyota family-prefix lookup sets. Consumer: `vinlab.overlay.cylinder_heuristic._infer_toyota`.
- **Volvo cylinder rule** - `B` digit count and `T` suffix turbo inference. Consumer: `vinlab.overlay.cylinder_heuristic._infer_volvo`.
- **Mercedes-Benz cylinder rule** - `M###` family table. Consumer: `vinlab.overlay.cylinder_heuristic._infer_mercedes`.
- **Volkswagen/Audi/Skoda/Seat displacement rule** - Deliberate displacement fallback plus brand-aware induction. Consumer: `vinlab.overlay.cylinder_heuristic._infer_vw_audi`.
- **Nissan cylinder rule** - Two-letter Nissan family sets. Consumer: `vinlab.overlay.cylinder_heuristic._infer_nissan`.
- **Mitsubishi cylinder rule** - Leading-digit cylinder inference. Consumer: `vinlab.overlay.cylinder_heuristic._infer_mitsubishi`.
- **Mazda cylinder rule** - Mazda prefix I4 inference. Consumer: `vinlab.overlay.cylinder_heuristic._infer_mazda`.
- **Subaru cylinder rule** - Boxer 4/6 family sets. Consumer: `vinlab.overlay.cylinder_heuristic._infer_subaru`.
- **Renault/Dacia cylinder rule** - Renault/Dacia family sets. Consumer: `vinlab.overlay.cylinder_heuristic._infer_renault`.
- **PSA cylinder rule** - Peugeot/Citroen prefix patterns. Consumer: `vinlab.overlay.cylinder_heuristic._infer_psa`.
