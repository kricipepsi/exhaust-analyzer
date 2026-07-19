# AUDIT — VIN → Engine Resolution Data Quality

**Authored:** 2026-06-21 (architect, Cowork).
**Trigger:** test-run prep for `apps/wiredV2` oil-burn presentation. The presentation
vehicle **`VF7SA5FR8AW511081`** (Citroën, engine `5FR` = 1.6 THP **turbo**) failed to
resolve an engine, returning `confidence = NONE`, `cylinder_count = 0`,
`displacement = 0.0`, `induction = NATURALLY_ASPIRATED`.
**Scope of audit:** the three data sources behind VINLab engine resolution —
`vinlab/data/wmi.csv`, `vinlab/data/vds_engine_map.csv`, `vinlab/data/vref.db`.
**Verdict:** the failure is **not the VIN and not the sandbox.** It is four
data-quality defects in the lookup tables, and **they are dataset-wide — every brand
is affected by at least one of them.**

---

## 1. Executive summary

The presentation vehicle is a Citroën whose engine code **`5FR` (EP6CDT, 1.6 L THP,
4-cylinder, turbocharged, direct-injection)** is a real, well-known PSA engine. The
decoder returns *nothing* for it, for two stacked reasons, and could not classify its
induction even if it did. Four independent defects sit on the VIN → engine path:

| # | Defect | What it breaks | Reach |
|---|--------|----------------|-------|
| **D1** | **Blank brand cells** in `wmi.csv` (324 rows, 2.5%) | Engine lookup is silently skipped — the manufacturer's whole catalogue is unreachable | 8 French WMIs incl. **VF7 = Citroën**, 17 German, 17 Italian, 27 Slovenian, others |
| **D2** | **Brand string / encoding mismatch** between `wmi.csv` and `vds_engine_map.csv` | The lookup key never matches, so engine data that exists can't be joined | **Mercedes-Benz (entire brand, 207 engines)**, Rolls-Royce, Škoda, Dacia, ~58 more |
| **D3** | **`vref.db` engine-equipment coverage of 0.6 %** | Engines resolve dimensionally but their *equipment* (induction, Euro class, O₂, CoC) **defaults** — a turbo is silently reported as naturally-aspirated | **3,324 of 3,343 engine codes (99.4 %)** — every brand |
| **D4** | **Incomplete VDS→engine coverage** in `vds_engine_map.csv` | A specific model/engine variant has no map row, so the VIN resolves no engine even with a correct brand | **The presentation VIN's `CITROEN_SA5FR` row is missing** though its siblings `SA5FD/SA5FF/SA5FS` and the code `5FR` itself all exist |

> The original question — *"is it only this VIN, or do other brands produce such
> results?"* — is answered emphatically: **other brands, including Mercedes-Benz in
> its entirety, fail the same way (D1/D2); the equipment-defaulting (D3) is nearly
> universal; and the corrected VIN exposes a coverage hole (D4) on top.**

---

## 2. How VIN → engine resolution is supposed to work

```
 VIN  "VF7 SA5FR 8 A W511081"
        │     │   │ │
        │     │   │ └─ pos 11-17  serial (ignored for engine)
        │     │   └─── pos 10 = "A"  → year 2010              (years.csv)
        │     └─────── pos 4-8 = "SA5FR"  VDS = engine key
        └───────────── pos 1-3 = "VF7"  WMI = brand key       (wmi.csv)

 STEP 1  WMI lookup     VF7 ─► brand = "CITROEN"              [wmi.csv]        ← D1 fails here (blank)
 STEP 2  VDS lookup     key = "CITROEN_SA5FR"                 [vds_engine_map] ← D4 fails here (no row)
                        ─► engine_code 5FR, 1.6 L, 4-cyl
 STEP 3  vref lookup    5FR ─► induction / Euro / O₂ / CoC    [vref.db]        ← D3 fails here (0.6% coverage)
 STEP 4  assemble       VehicleDNA  (+ confidence score)
```

The join (matching a row in one file to a row in another by a shared key) at STEP 2
is `"{BRAND}_{VDS}"`. **STEP 1 supplies the `{BRAND}` half.** If STEP 1 returns an
empty brand (D1) or a brand spelled differently than STEP 2 expects (D2), the join
silently misses. If STEP 2 has no row for that exact brand+VDS (D4), same outcome.
STEP 3 (`vref.db`) being 99.4 % empty (D3) means even a successful STEP 2 produces
defaulted equipment — including a wrong induction flag.

---

## 3. Defect D1 — blank brand cells in `wmi.csv`

**The row for the presentation VIN's manufacturer:**

```
wmi.csv:   VF7,,FRANCE,modern
                ^ brand column is EMPTY
```

**Why it is fatal, silently.** The resolver builds the engine key only when a brand
is present:

```python
# vinlab/decoder.py  _resolve_engine()
brand_upper = brand.upper()
if brand_upper:                       # ← blank brand → this is False
    full_key = f"{brand_upper}_{vds_slice}"
    if full_key in self.vds_full_index:
        return ...                     #  (never reached for VF7)
return None                            #  → conf flag "engine_not_in_csv" → confidence NONE
```

A blank brand isn't an error and isn't logged — it just produces a `None` engine and
a `NONE`-confidence result. There is no signal that real data was bypassed.

**Scale.** 324 of 13,180 WMI rows (2.5 %) carry a blank brand. By country:

| Country | Blank-brand WMIs |
|---|---|
| (no country) | 224 |
| Slovenia | 27 |
| Italy | 17 |
| Germany | 17 |
| United Kingdom | 8 |
| France | 8 |
| Austria | 5 |
| Poland | 4 |
| Spain | 3 |
| Czech Rep. / Netherlands / Belgium | 2 / 2 / 1 |

**The French blanks are high-volume mainstream makers**, not obscure ones:
`S24, VF7, VF8, VFA, VNV, VR1, VR3, VR7`. `VF7` is Citroën's primary WMI. (Curiously,
six *secondary* Citroën codes — `FV7, VFZ, CF7, NF7, VZ7, 1N9423` — *are* labelled,
but the canonical one that real VINs use is not.)

**Proof that D1 is real (in-sandbox, non-destructive patch), using a sibling VDS
that *does* have a map row — `SA5FS`:**

```
VF7 brand = ''         → make=''        disp=0.0  cyl=0  confidence=NONE
VF7 brand = 'CITROEN'  → make='CITROEN' disp=1.6  cyl=4  confidence=PARTIAL
                          (engine F501 / vds SA5FS resolves once brand is present)
```

---

## 4. Defect D2 — brand string / encoding mismatch

Even when a brand *is* labelled, the two files must spell it **identically** (the
join uppercases both sides but does nothing else). They don't always agree.

| `wmi.csv` spells it | `vds_engine_map.csv` spells it | Engine rows stranded |
|---|---|---|
| `Mercedes-Benz` | `MERCEDES BENZ` (hyphen → space) | **207** |
| `Rolls-Royce` | `ROLLS ROYCE` | 4 |
| (Škoda / Dacia / SsangYong / Proton + ~55 long-tail) | unlabelled / encoding-folded | 183 |

**Mercedes-Benz is the headline:** the entire brand's engine catalogue (207 engines)
is unreachable because `"MERCEDES-BENZ" ≠ "MERCEDES BENZ"`. Every Mercedes VIN
decodes to `NONE` confidence with no engine.

**Proof (constructed Mercedes VIN `1MB010010A1234567`):**

```
brand = 'Mercedes-Benz' (as shipped)  → disp=0.0  cyl=0  confidence=NONE
brand = 'MERCEDES BENZ' (key-matched)  → disp=1.8  cyl=4  confidence=PARTIAL
```

**Join health across the whole engine map (5,806 rows / 154 brands):**

| Join status | Brands | Engine rows |
|---|---|---|
| Exact match — joinable today | 94 | 5,412 |
| Blocked by string/encoding mismatch | 2 | 211 |
| No matching brand label at all | 58 | 183 |

D1, D2 and D4 are the *same outcome* (engine unreachable) from three causes: a
missing brand value, a non-matching brand value, and a missing VDS row.

---

## 5. Defect D3 — `vref.db` equipment coverage is 0.6 %

This is the one that turns a **turbo into a "naturally-aspirated"** reading.

STEP 2 (`vds_engine_map.csv`) supplies only *dimensions* — displacement, cylinders,
configuration, fuel system. The **equipment** — induction type (NA / turbo /
supercharged), Euro emission class, O₂ sensor type, and the CoC chemistry targets —
lives only in `vref.db`. When the engine code isn't in `vref.db`, the decoder falls
back to hard-coded defaults:

```python
# vinlab/decoder.py  _apply_vref_techmask()  (no db_row branch)
# "No vref.db row — use CSV-only values with defaults"
#   induction_type   → NATURALLY_ASPIRATED   ← this is why a turbo looks NA
#   euro             → EURO_1                 (→ HORIZON_LEGACY)
#   o2 / CoC targets → generic defaults
```

**Coverage:**

| Metric | Count |
|---|---|
| Distinct engine codes referenced by `vds_engine_map.csv` | 3,343 |
| Of those, present in `vref.db` (full equipment) | **19 (0.6 %)** |
| Missing from `vref.db` (equipment defaulted) | **3,324 (99.4 %)** |
| Is the presentation engine `5FR` present? | **No** → would default to NA, EURO_1 |

**Consequence for confidence.** The decoder's confidence ladder is:

```
engine row not found in CSV ............ NONE      (D1 / D2 / D4)
engine in CSV but NOT in vref.db ....... PARTIAL   (D3 — the 99.4% case)
engine fully resolved .................. HIGH
```

So fixing reachability alone lifts a VIN from `NONE` to `PARTIAL` — the engine size
is now right, but **its induction type and emissions class are still guesses.** A
genuine `HIGH`-confidence decode (and a trustworthy turbo/NA flag) needs D3 fixed too.

**This is why a turbo reads NA:** the NA flag was never looked up — it is the fallback
default for an engine `vref.db` has never heard of. The same is true for 3,324 other
engine codes across every brand.

---

## 6. Defect D4 — incomplete VDS→engine coverage (the corrected VIN)

The corrected presentation VIN exposes a gap that D1/D2 hide: even with the brand
correct, the **specific VDS row is missing.**

```
presentation VDS = "SA5FR"  (engine 5FR = 1.6 THP turbo)

CITROEN rows present in vds_engine_map.csv:
   CITROEN,SA5FD,,5FD,1.6,4,I4,PORT_INJECTION
   CITROEN,SA5FF,,5FF,1.6,4,I4,PORT_INJECTION
   CITROEN,SA5FS,,F501,1.6,4,I4,PORT_INJECTION
   CITROEN,SA5FR  →  *** ABSENT ***

Engine code 5FR exists — but only under another brand:
   PEUGEOT,WB5FR,,5FR,1.6,4,I4,PORT_INJECTION
```

So the row that should read roughly `CITROEN,SA5FR,,5FR,1.6,4,I4,…` simply isn't
there. The siblings are; the engine code is; the brand (once D1 is fixed) is — only
the join row is missing.

**Proof (corrected VIN, brand patched):**

```
VF7=CITROEN, VIN VF7SA5FR8AW511081 → engine_row = None → disp=0.0 cyl=0 confidence=NONE
```

**Two further accuracy notes on `5FR`:** the one existing `5FR` row is tagged
`PORT_INJECTION`, but the EP6CDT THP is **direct-injection + turbo** — so even when a
`5FR` row is added, its `fuel_system_type` should be GDI and its `vref.db` induction
must be turbo (not the NA default). D4 (reachability) and D3 (equipment) both have to
be right for this engine to decode correctly.

---

## 7. What this means for the presentation vehicle

`VF7SA5FR8AW511081` — current vs. achievable:

| Field | As shipped today | After D1+D4 (reachability) | After D1+D4+D3 (full) |
|---|---|---|---|
| make | `''` | `CITROEN` | `CITROEN` |
| engine code | — | `5FR` | `5FR` (EP6CDT) |
| displacement | `0.0` | `1.6 L` | `1.6 L` |
| cylinders | `0` | `4` (I4) | `4` |
| induction | `NATURALLY_ASPIRATED` (default) | `NATURALLY_ASPIRATED` (still default) | **TURBOCHARGED** (authoritative) |
| fuel system | — | (map: PORT — suspect) | **DIRECT_INJECTION (GDI)** |
| Euro class | `EURO_1` (default) | `EURO_1` (still default) | **≈ EURO_5 (MY2010)** |
| confidence | `NONE` | `PARTIAL` | `HIGH` |

The turbo-vs-NA discrepancy the owner flagged is now fully explained: it is **D3 (no
`vref.db` row → NA default)**, and the vehicle can't even reach STEP 3 yet because of
**D1 (blank brand) + D4 (missing VDS row)**.

---

## 8. Recommended fixes (handed off as coder tasks)

1. **`T-VIN-FIX-1` — Brand-join integrity + VDS coverage (fixes D1 + D2 + D4).**
   Fill blank brand cells in `wmi.csv` (VF7→Citroën first); normalize the brand join
   (case + hyphen/space + diacritics) so `MERCEDES-BENZ` matches `MERCEDES BENZ`; add
   the missing `CITROEN_SA5FR → 5FR` map row (and audit sibling VDS coverage); and
   make the empty-brand path **fail loud** (confidence flag) instead of silent.
   Highest impact, smallest change — unblocks the presentation VIN, all Mercedes,
   Rolls-Royce, and the blank-brand European makers.

2. **`T-VIN-FIX-2` — `vref.db` engine-equipment coverage (fixes D3).** Populate
   `vref.db` for the engine codes real VINs hit, with **authoritative induction /
   Euro / O₂ / CoC** per code. Seed with **`5FR` (EP6CDT 1.6 THP, turbo, GDI,
   ≈EURO_5)** so the presentation vehicle reaches `HIGH` confidence with the correct
   turbo flag. Data-sourcing effort — scope by VIN-traffic priority, not all 3,324.

Both specs live in `labs/vinlab/tasks/`.

---

## Appendix — reproduction

All figures produced offline against the in-repo data (no network, no MySQL), using
the project's sandbox interpreter:

```
data:  labs/vinlab/vinlab/data/{wmi.csv, vds_engine_map.csv, vref.db}
decode: vinlab.decoder.RobustVINDecoder(data_dir).decode_vin_payload(VIN)
```

Key counts: wmi.csv 13,180 rows / 324 blank-brand; vds_engine_map.csv 5,806 rows /
154 brands / 3,343 distinct engine codes; vref.db 19 of those codes present
(0.6 %). Presentation VIN `VF7SA5FR8AW511081`: blocked by D1 (VF7 blank) **and** D4
(`CITROEN_SA5FR` row absent), and would hit D3 (`5FR` not in vref.db) once reachable.
Proof patches were applied **in memory only** — no data file was modified by this
audit.
