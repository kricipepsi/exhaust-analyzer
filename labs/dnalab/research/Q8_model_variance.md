# DNA10 Q8 - `model` variance check

Date: 2026-06-11

## Question

Does `D3_commercial_name` / `model` add diagnostic signal beyond
`P15_engine_code` for the CoC targets that drive petrol diagnosis?

This answers DNA10 Q8 and T-DNA-5. The named consumer is DTCLab's local
`DtcLabDnaView.model` requirement. COMLab's canonical `DtcLabDnaView` omits
`model`, and `VinDNA` does not emit it.

## Method

The task-contracted method was to group
`DBS/docs/vehicles_petrol_specimens.csv` by `P15_engine_code` and measure
within-engine-code spread for the diagnosis-driving targets:

| Column | Meaning |
|---|---|
| `V112_lambda` | CoC lambda target |
| `V101_CO_low_idle` | CoC low-idle CO target |
| `V111_CO_high_idle` | CoC high-idle CO target |
| `P14_rated_rpm` | Rated RPM source used by OBDLab |

Numbers were parsed with semicolon CSV delimiters and decimal-comma support.
Only rows with non-empty `P15_engine_code` were considered.

## Findings

`vehicles_petrol_specimens.csv` does not contain repeated non-empty
`P15_engine_code` groups:

| Measure | Result |
|---|---:|
| Specimen rows with non-empty `P15_engine_code` | 7,079 |
| Unique non-empty `P15_engine_code` values | 7,079 |
| Engine-code groups with more than one specimen | 0 |

Therefore the literal within-engine-code variance requested by T-DNA-5 is not
computable from the specimen file. Per target column:

| Field | Filled rows | Engine-code groups with >3 filled specimens | Median within-code stdev |
|---|---:|---:|---:|
| `V112_lambda` | 1,223 | 0 | n/a |
| `V101_CO_low_idle` | 1,043 | 0 | n/a |
| `V111_CO_high_idle` | 1,134 | 0 | n/a |
| `P14_rated_rpm` | 3,420 | 0 | n/a |

The broader registry file, `DBS/docs/vehicles_petrol_M1_1990_2020.csv`, does
show that commercial names vary within an engine code:

| Measure | Result |
|---|---:|
| Registry rows with non-empty `P15_engine_code` | 551,988 |
| Unique non-empty `P15_engine_code` values | 7,063 |
| Engine codes with more than one `D3_commercial_name` | 3,014 |
| Maximum commercial names under one engine code | 157 |

That registry file does not contain the CoC target columns, so it cannot answer
whether those model-name variants change `V112_lambda`, `V101_CO_low_idle`,
`V111_CO_high_idle`, or `P14_rated_rpm`.

## Decision

**KEEP-EMPTY.** `model` does not ship on `VinDNA`.

This is a signal/noise decision, not a claim that the specimen data proved zero
variance. DBS does not provide within-engine-code CoC replicate groups in the
contracted specimen file, and therefore provides no empirical basis for adding a
new `VinDNA.model` field. Adding it would create a schema field with no measured
diagnostic consumer.

The paired proposal is COMLab-D: relax or drop DTCLab's local mirror requirement
for `DtcLabDnaView.model` so DTCLab matches the COMLab-owned canonical view.

## Consumer Disposition

| Consumer | Disposition |
|---|---|
| `dtclab/dtclab/schemas/dna_view.py:DtcLabDnaView.model` | Relax to optional or remove in COMLab-D / DTCLab mirror reconciliation |
| `labs/comlab/comlab/schemas/lab_dna_views.py:DtcLabDnaView` | Keep canonical shape without `model` |
| `VinDNA` | No schema change |

## Verification Snippet Result

The task-provided lambda check returned:

```text
engine_codes w/ >3 specimens: 0
median within-code lambda stdev: n/a
```
