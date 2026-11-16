# RULING T-AUD-24r — what to fix from the T-AUD-23k v2-router verdicts (Windows Cowork, 2026-11-16)

Input: `REVIEW_T-AUD-23k.md` (6 CONTRADICTED; CK0240 set aside by its M2). Corpus: v7, 314 cases (base output
identical to `recheck/T-AUD-24k/promoted.json`: family 224, code 126). Literal variants on
`labs/comlab/registry/integration_shim.py`: `C:/4DApp/recheck/T-AUD-24r/run.sh`, `lit.py`, `run.txt`.

| claim | line | variant | changed | family | probe (never) |
|---|---|---|---|---|---|
| CK0244 total trim at idle ≥ 15 | `:733` | ≥ 20 (OEM ±20 % combined) | 0 | 224 | 8 changed, 224 → 217 |
| CK0248 port rail drop < 280 kPa | `:739` | < 240 (Ford 35 psig) | 0 | 224 | 0 |
| CK0260 downstream > 0.7 V | `:783` | > 0.85 (Ford filtered top) | 0 | 224 | 0 |
| CK0283 idle trim ≤ −10 % as rich | `:958` | ≤ −20 | 5 | 224 → 219 | 9 changed, 224 → 215 |
| CK0284 catalyst index > 0.20 | `:959` | > 0.75 (Ford pass ≤ 0.75) | 2 | 224 | 2 changed, 224 |

## Rulings
1. **No fix: CK0244.** The gate carries weight (never: −7), and the source boundary changes nothing. No measured
   gain. Lost: moving it to 20 for the source alone.
2. **No fix: CK0283.** At −20 the row loses 5 family verdicts; the gate is load-bearing at −10.
3. **No fix: CK0248, CK0260.** Not reached (never-probes 0 of 314).
4. **No fix: CK0284.** Two cases change with family and code accuracy equal. Ford's ratio counts rear-sensor
   switches against front; `c2_index` is the repo's own catalyst index, and nothing shows the two measure the
   same thing. Lost: 0.75 on a likeness that is not shown.
5. **CK0240 not acted on** (REVIEW_T-AUD-23k M2: the source is a monitor-validity band, and the gate reads better as
   PARTLY).
