# REVIEW T-AUD-11e — ACCEPT, score 95 (Windows Cowork, 2026-11-05 22:18 CET)

Facts first: commit `499714a` on `fix/T-AUD-11e` (after spec `49ab697`) changes only
`audit/drift/2026-11-05_DRIFT_REPORT_gaslab.md`. Cowork re-run of `check_report.py`: `sections 8/8, findings 47,
refs ok 80/80`, `REPORT OK` (exit 0). Porcelain: note and RESULT only. Headless run 21:04:03-21:12:17 UTC, exit 0.
Docs row: no second-model review.

## Findings re-derived (47; 16 checked directly, the rest by their quoted line or ABSENT command; none rejected)
Checked by Cowork:
- `grep -c "signature_type: catch_all"` = 4 (docs say 3: PRD, HLD, ADR-0006). `len(GasLabPayload.model_fields)` = 15 (docs say 9).
- `requires_dtc` read by no lab `.py` (0). `confidence` absent from `contracts.py` (HLD:149, ADR-0011 say forwarded).
- `load_ontology` (`ontology_loader.py:26`) has no cache and reads the file; `process.py:38` calls it on every call
  (HLD:201, ADR:98 say loaded once / no hot-path I/O).
- `brettschneider.py:42-47`: all-zero sample returns 1.0; formula has no `Hcv` term (VOCAB:230, 254).
- YAML scope "Petrol 1990-2020" vs VOCAB:27 1990-2010; NOx entry `min: 1000` vs VOCAB:396 1500; worn-rings `hc > 300`
  (`resolution.py:466`) vs VOCAB:440 250.
- README:8 "COMLab and `4dlabwired_v2` mirror the types locally" vs `composition.py:57` importing `gaslab` directly.
- ADR:130 "ranking keeps gated candidates" vs `ranking.py:234` → `_resolve_candidates`, which drops on `dna_gate`
  (`resolution.py:300-304`).

## Drift groups (for the fix row)
1. Counts: catch-alls 3→4, payload 9→15 fields, DNA view consumers (`number_of_banks` unread).
2. `confidence`: not forwarded in the payload; read by `ranking.py`; invariant 7 candidate restriction not applied.
3. **Behaviour:** YAML reloaded on every `process()` call (cache it, or correct HLD/ADR-0004).
4. **Behaviour:** literals the docs say come from the ontology (`fuel_trim > 8.0`, cam vector, rich-timing band).
5. **Promised, absent:** `LambdaBand` discretiser, `COLD_OPEN_LOOP_INVALID` handling, `GasBehavior`, `CatalystStatus`,
   `chemical_efficiency`, `afr_chem`, per-vehicle logging, misfire-count warning, type-approval DNA fields,
   `requires_dtc`. Each needs a ruling: implement, or mark as planned in the docs.
6. Numbers: NOx 1500/1000, HC 250/300, scope 2010/2020, `Hcv`, λ sentinel, collision bound fixed 0.45.
7. Gate table misses two edges (`HIGH_COMBUSTION_TEMP` EGR, FPR NON_GDI); dilution-gate order; BDD low-triangle
   air leak; DNA view built by the composition, not COMLab; README boundary.

## Score
100 − 3 (one-phase `## Time`) − 2 (drift 2 reported in four documents with overlapping wording) = 95.

## Follow-up
T-AUD-16 (GASLab docs drift fixes), with rulings first on groups 3, 4 and 5.

Measured: GASLab (127 KB docs, 2,032 code lines) → 47 findings in 8 min on Sonnet medium.
