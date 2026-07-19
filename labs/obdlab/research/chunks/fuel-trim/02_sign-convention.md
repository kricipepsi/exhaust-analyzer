---
chunk: fuel-trim/02_sign-convention
topic: fuel-trim
sources:
  - master_fuel_trim_guide.md §2
consumer: COMLab truth-vs-perception fusion — trim *direction* is compared against gas-chemistry λ (see 07_trim-vs-gas-chemistry-crosscheck); the sign is the comparison key
consumer_status: active
dedup: canonical sign table; supersedes scattered sign notes in Fuel Trim Diagnostics.txt and Ross-Tech_ VAG-COM_ Fuel Trim Info.md
---

# Fuel-trim sign convention

| Sign | Meaning | What the ECU is doing |
|---|---|---|
| **Positive (+)** | System running **lean** | ECU is **adding** fuel |
| **Negative (−)** | System running **rich** | ECU is **subtracting** fuel |
| **0 %** | Perfect stoichiometric | No correction required |

Positive trim ⇔ engine getting more air than the ECU expected (lean).
Negative trim ⇔ engine getting less air than expected, or extra unmetered fuel
(rich).

**Standardisation.** This sign convention is universal across OBD-II vehicles per
SAE J1979 PID `$06` (STFT B1) / `$07` (LTFT B1).

**Pre-OBD-II caveat.** Some Asian-market pre-OBD-II proprietary ECUs use the
opposite convention. If the vehicle is **≤ 1995**, the engine raises
`trim_sign_uncertain` and the truth-vs-perception comparison
(`07_trim-vs-gas-chemistry-crosscheck`) must not assume the table above.

Citation: SAE J1979 (PID `$06`/`$07` sign definition).


## Core Entities

- STFT, LTFT, POSITIVE_TRIM, NEGATIVE_TRIM, trim_sign_uncertain

## Graph relations (explicit)

**POSITIVE_TRIM** INDICATES **LEAN_MIXTURE**
**NEGATIVE_TRIM** INDICATES **RICH_MIXTURE**
**trim_sign** COMPARED_AGAINST **lambda_chem**
**pre-OBD-II ECU** RAISES **trim_sign_uncertain**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
