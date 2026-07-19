# Unresolved Cylinder Count Report — 2026-05-20

**1,630 rows still missing `cylinder_count`** (28.1% of 5,806)

All 1,630 have `fuel_system_type=PORT_INJECTION` and a non-empty `engine_displacement` value.

---

## By brand

| Brand | Unresolved |
|---|---|
| BMW | 108 |
| PEUGEOT | 102 |
| RENAULT | 102 |
| CITROEN | 77 |
| HYUNDAI | 77 |
| FORD | 65 |
| HONDA | 62 |
| VOLVO | 62 |
| TOYOTA | 58 |
| VOLKSWAGEN | 56 |
| CHEVROLET | 45 |
| FIAT | 45 |
| JEEP | 43 |
| OPEL | 42 |
| CHRYSLER | 39 |
| MERCEDES BENZ | 38 |
| AUDI | 32 |
| NISSAN | 32 |
| ROVER | 32 |
| SUZUKI | 28 |
| SKODA | 27 |
| JAGUAR | 25 |
| MAZDA | 23 |
| MITSUBISHI | 22 |
| KIA | 20 |
| SUBARU | 20 |
| DAEWOO | 19 |
| ZASTAVA | 19 |
| MINI | 18 |
| MERCEDES-BENZ | 17 |
| Other (<15 each) | ~160 |

## Top 30 unresolved engine codes

All appear exactly once (unique per row).

```
HJY683411   FKA44621    0526/AS     00526A88079   AK00515
AR6134      AR6224      E6D         AR016100      AR00539
AR0051      AR1308      TIPAR30751  TIPAR16201    TIPAR36201
670052588   670051007   1172339     JF8           AM04
AM04/       95/79075/A  AM14/       AM08          60/4T
DLGA        CYM         CTY         TIPAPS        TIPAHC
```

## Why these remain unresolved

| Reason | Brands affected |
|---|---|
| Engine code is an internal ID or VDS fragment, not a manufacturer engine code | PEUGEOT (102), CITROEN (77), HYUNDAI (77), many others |
| Code exists in TecDoc but lacks `NumberOfCylinders` or `FuelType=petrol` attribute | Mixed — low single digits per brand |
| Manufacturer not covered by naming rules (`enginevincyl.md` only covers 4 brands) | FORD (65), HONDA (62), VOLVO (62), TOYOTA (58), VW (56), and others |
| Code matches naming pattern but is an exception (e.g., N63 = V8 but rule says 6) | BMW — small number |

## Possible next steps

- **T-CSV-3c** — Extend naming rules to FORD, HONDA, TOYOTA, VW, VOLVO (their engine codes also encode cylinder count structurally)
- **T-CSV-3d** — Displacement-based fallback: for the remaining codes, look up cylinder count by engine displacement (±15% range) from the existing 4,176 filled rows
- Accept 71.9% coverage as sufficient for v1 and move on
