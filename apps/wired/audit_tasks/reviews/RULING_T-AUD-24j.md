# RULING T-AUD-24j — the 14 T-AUD-23d CONTRADICTED gates (Windows Cowork, 2026-11-16)

Measured on `fix/T-AUD-23d` (`1c64e43`), v7 corpus (314 cases), `recheck/T-AUD-24j/`. Base: family 221, code 117
(`expected_fault_code`). Each group was moved to its source band in isolation.

| group | claims | variant | changed | family | code | ruling |
|---|---|---|---|---|---|---|
| lean trims | CK0442, CK0444, CK0448 | STFT/LTFT gates → ±10 % | 5 | 217 | 115 | **no fix** |
| misfire trims | CK0516, CK0517, CK0520 | → ±10 % | 1 | 221 | 117 | **no fix** |
| rich trims | CK0613, CK0615, CK0619 | → ±10 % | 4 | 221 | 117 | **no fix** |
| NORMAL HC | CK0352, CK0524 | CF-002 `hc < 50`, MF-004 `hc < 50` | 0 | 221 | 117 | **fix** (T-AUD-24j) |
| LC-002 MAP | CK0445 | `map_kpa gt 50` (direction flipped) | 10 | 221 | 126 | **fix** (T-AUD-24j) |
| LC-003 MAF | CK0447 | gate never passes | 0 | 221 | 117 | **no fix** |
| CF-004 CO2 | CK0358 | `co2 ≥ 14.5` | 0 | 221 | 117 | **no fix** |

- **Trims, no fix.** The gates are SUGGESTIVE weights behind GATING or DEFINITIVE chemistry, so a healthy trim adds
  0.05 only to a rule whose chemistry already fired. Moving the lean gates loses 4 family and 2 code verdicts. The
  rich and misfire moves trade verdicts one for one (rich: era3_005 lost, EXP-N006 gained). The healthy-band
  evidence is mostly TRADE (S030); the one OEM source (S029) gives ±20 % combined as a P0171 functional criterion, not
  a fault boundary. Lost alternative: the source band everywhere (−4 family, −2 code).
- **NORMAL HC, fix.** "Pristine" chemistry is 0-35 ppm (S023) or < 50 ppm (S034); 100 and 200 ppm accept a
  not-lit catalyst band (75-125 ppm). 0 verdicts change.
- **LC-002 MAP, fix.** The gate pointed at healthy vacuum (30-50 kPa, S036), so LC-002 took vacuum-leak cases from
  LC-001. Flipped to `gt 50`, LC-001 wins the 10 cases the corpus expects as LC-001 (CSV-110, EXP-N001, case_019,
  EXT-218, …). VL-001 already gates `map_kpa gt 40`; T-COMA-28 called `< 40` "normal idle vacuum". Lost: `gt 40`
  (the same corpus result, but inside the healthy band).
- **LC-003 MAF, no fix.** The healthy idle MAF scales with displacement (about 1 g/s per litre, S019), and the rule
  has no displacement input; the gate never decides a corpus verdict. Registered as too small.
- **CF-004 CO2, no fix.** A not-lit catalyst gives 13.5-14.5 % (S023), so `≥ 13` is the floor of that band; it
  also admits healthy 14.5-16 %, but the rule is GATING on CATALYST_NOT_LIGHTING_OFF chemistry. 0 change.
