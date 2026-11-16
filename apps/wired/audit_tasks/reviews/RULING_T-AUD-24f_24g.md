# RULING T-AUD-24f, T-AUD-24g — Windows Cowork, 2026-11-16

Both rows close with no fix and no implementer. Measured on `fix/T-AUD-24e` (`29ec583`).

## T-AUD-24f — catalyst rear-O2 window ERR-CF-004 (CK0714, CK0715, CK1091)

**Verdict stays CONTRADICTED; the row is not fixed, because the claims are not on the default path.**

- `global_fault_registry.json` and `config/kg/*.json` are the v1 path. `lab_pipeline_aggregator.py:125` resolves
  `USE_V2_REGISTRY` to `"1"` when unset; on v2, `fault_atlas_router.py:1977` delegates to the registry shim and
  returns at `:2210`, before the ERR-CF-004 gate (`:1034`) and the KG enrichment (`:2233`).
- v7 corpus (314 cases), measured three ways: tip, the `o2_b1s2_v` gate dropped, the gate widened to `[0.0, 5.0]`.
  Each gives 0 changed verdicts, 221 of 314 correct by family, and no case with an `ERR-CF-004` verdict
  (`recheck/T-AUD-24f/`).
- In v1 the gate is the only discriminator between ERR-CF-001 (`o2_b1s2_v > 0.6`, score 0.8 + 0.2) and ERR-CF-004
  (`[0.4, 0.5]`, 0.9 + 0.1): both need `CATALYST_OVERWHELMED` and P0420/P0430. Without the gate, the two rules tie at
  1.0 every time ERR-CF-001 fires. A single snapshot of `o2_b1s2_v` cannot detect the switching that S017 describes,
  so no correct one-PID gate exists.
- Lost alternative: drop the gate and rewrite the KG text. It corrects text that no default user sees, and it breaks
  the v1 discrimination that the `USE_V2_REGISTRY=0` comparison ruler uses.
- Record: the register suspect notes of CK0714, CK0715, CK1091 carry `NOT LIVE (T-AUD-24f)`.

## T-AUD-24g — OBDLab VE skew cutoff 90 % (RK0062)

**Verdict CONTRADICTED → PARTLY; no fix.**

- S019 (`sources/S019.md:107, 115`): the "90% or above" VE test is read "while at WOT".
- `ve_engine.py:268-273` fires `FAULT_VE_SENSOR_SKEW` only at `STABILIZED_IDLE` on an NA engine. The code's own
  MAP-referenced idle targets are 0.65 and 0.70 (`ve_engine.py:36-40`). A healthy WOT figure does not contradict an
  idle-only cutoff. S019 says nothing about idle VE, so the cutoff is neither confirmed nor contradicted.
- The T-AUD-23b review line ("healthy NA engines reach 85-95 %") compared two operating points; this ruling
  corrects it.
- The code-vs-wiki drift (wiki §6.4/§10.3 > 85 %, code 90 %) belongs to T-AUD-23c.
- Lost alternative: lower or raise the cutoff. No source gives an idle VE band, so either value is a guess.

## Checks

`check_verdicts.py`: `VERDICTS OK` for scopes T-GASA-17 (20), T-AUD-23a (25), T-AUD-23b (29).
`check_code_claims.py`: `CLAIMS OK` for comlab (1608) and rest (451), the same as before the edit.
