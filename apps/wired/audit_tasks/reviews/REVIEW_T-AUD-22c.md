# REVIEW T-AUD-22c — ACCEPT, score 97 (Windows Cowork, 2026-11-14)

Docs row (no second-model review). `fix/T-AUD-22c` on `fix/T-AUD-22-RESYNC` `0fba628`: spec commits `dbbc70d`,
`119c362`, `94682c2`; implementer commit `d8a63ab` (`claims_comlab.csv` +391 rows `CK0302`-`CK0692`, 0 removed).

Facts (Cowork re-run): step 1 `classes ANALYSER_SPEC=26 DIAGNOSTIC_THRESHOLD=266 INTERNAL_PARAMETER=240 NON_DOMAIN=136
PHYSICAL_CONSTANT=6 TYPICAL_RANGE=18`, `suspect 35 same_as_wiki 20`, `CLAIMS OK group=comlab
scope=labs/comlab/registry/rules/* candidates 358 covered claims 692`; step 2 `knobs 130 internal 130`; step 3
`CLAIMS OK group=comlab scope=*.py candidates 293 covered claims 692`; step 4: 1 file, 0 removed lines.

Hand-back B11 (SOFT, UNSATISFIABLE): criterion 3 pinned `covered claims 301`, but the checker counts all rows of the
file. Upheld as a spec defect (Cowork's P4). The implementer's reading (candidates 293 still covered, CK0001-CK0301
unchanged) is the intended one and is confirmed by the append-only diff.

Suspects read (16 new). Re-derived against the rule JSON:
- CK0469/CK0470 MW-004 (and the next MW rule): description "low intake vacuum ... weak cylinders", gate
  `map_kpa lt 30.0` = strong vacuum. Inverted. -> T-COMA-32.
- CK0403 EL-002: description "downstream O2 sees excess oxygen (lean)", gate `o2_downstream ge 0.45` V = rich side.
  Inverted. -> T-COMA-32.
- CK0535/CK0537/CK0547 no_fault accepts CO <= 0.5, O2 <= 0.6, NOx <= 300: above the working-cat values (CO 0.3 legal
  limit W0185). For the verification slice (same root as T-GASA-F45).
- CK0440/CK0611 lean > 1.03 / rich < 0.97 vs wiki 1.05 / 0.95; CK0592 overheating 110 vs vocab 108; CK0635/CK0638
  stuck-rich 0.80 vs vocab 0.85; CK0320/CK0329 three VVT DTC ranges; CK0482 misfire P0300-P0304 only; CK0397 triangle
  [14,16] vs vocab 14/18; CK0432 CO2 ~16 vs 15.5. For the verification slice.
Time: the note records 7 min (first action to finish, two `date -u` readings); expected 30.

## Score
97: complete and careful; two inverted rules found from knowledge; the only defect is the spec's.
