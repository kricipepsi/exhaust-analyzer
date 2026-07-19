# T-VIN-FIX-1 progress note

Status: done
Date: 2026-06-21

## Scope completed

- Added case/spacing/hyphen/diacritic folding for brand joins.
- Preserved exact-brand lookup priority because the source CSV contains conflicting
  duplicate Mercedes VDS rows under `MERCEDES BENZ` and `MERCEDES-BENZ`.
- Added `wmi_brand_missing`; a blank WMI brand now yields public
  `confidence=PARTIAL` instead of an unexplained `NONE`.
- Added `CITROEN,SA5FR,,5FR,1.6,4,I4,GDI`.
- Added regression tests for the presentation Citroën VIN, normalized Mercedes
  lookup, diacritic folding, and the blank-brand path.

## WMI source record

ISO 3780 defines the WMI as the VIN section identifying the manufacturer and
requires assigned codes to be maintained by the registration authority:
https://www.iso.org/standard/45844.html

Assignments filled from the WMI tables below:

- `VF7=CITROEN`, `VF8=MATRA`, `VFA=ALPINE`, `VNV=NISSAN`, `VR1=DS`,
  `VR3=PEUGEOT`, `VR7=CITROEN`
- `WDF=Mercedes-Benz`, `WMX=Mercedes-AMG`
- `SJN=NISSAN`, `SAR=ROVER`

Assignment references:

- Consolidated WMI table:
  https://en.wikibooks.org/wiki/Vehicle_Identification_Numbers_%28VIN_codes%29/World_Manufacturer_Identifier_%28WMI%29
- Mercedes WMI table:
  https://en.wikibooks.org/wiki/Vehicle_Identification_Numbers_%28VIN_codes%29/Mercedes-Benz/VIN_Codes
- Nissan WMI table:
  https://en.wikibooks.org/wiki/Vehicle_Identification_Numbers_%28VIN_codes%29/Nissan/VIN_Codes

The remaining country-group blanks were not guessed. `S24`, for example, appears
as a low-volume suffix (`W09/S24`) rather than a standalone French WMI in the
available assignment table. Other unresolved rows include numeric pseudo-WMIs or
country-prefix conflicts. They remain blank so the new fail-loud path exposes them.

## VDS source and sibling audit

- The task audit identifies the presentation VIN's VDS as `SA5FR` and engine code
  `5FR`: `planning/AUDIT_2026-06-21_vin_engine_resolution.md`.
- The existing Citroën siblings `SA5FD`, `SA5FF`, and `SA5FS` were present; no
  additional sibling row was added without a source.
- External engine-list corroboration maps Citroën/Peugeot `5FR` to a 1.6 L,
  four-cylinder direct-injection application:
  https://autotrend.ua/en/usefull-download?file=public%2Fsoft%2F6GEC2M8X3sgi3Uu6SG8qYJblspJOwRGSdp4bAhBF.pdf
- The existing `PEUGEOT,WB5FR` row remains `PORT_INJECTION` and is flagged for
  review only, as required by the task's no-existing-value-change boundary.

## Verification gate

- `python -m ruff check vinlab tests` — passed.
- `python -m pyright vinlab` — 0 errors, 0 warnings.
- `python -m pytest tests -x -q` — 190 passed, 8 skipped.
- `VF7SA5FR8AW511081` — `CITROEN`, 1.6 L, 4 cylinders, GDI, PARTIAL.
- `1MB010010A1234567` — `Mercedes-Benz`, 1.8 L, 4 cylinders, PARTIAL.
- Remaining blank-brand fixture — blank make, zero engine dimensions, PARTIAL
  through `wmi_brand_missing`.

No `labs/vinlab/tasks/PROGRESS.md` ledger exists in this checkout, so there was no
ledger row to flip.
