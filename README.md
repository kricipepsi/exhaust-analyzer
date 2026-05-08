# 4D Petrol Diagnostic Engine V2

**Status:** In development — Phase P0 (Foundations)
**Repo:** https://github.com/kricipepsi/v2-diagnostic-app
**Workflow:** `V2_START_HERE.md` (in parent folder `C:\Users\muto\claude\4DApp\v2\`)

## Architecture

Seven-module pipeline: VL → M0 → M1/M2 → M3 → M4 → M5

See `C:\Users\muto\claude\4DApp\v2\01_planning\HLD_v2.md` for full design.

## Quick start

```bash
pip install -r requirements.txt
pytest tests/v2/ -x
```

## Folder layout

| Folder | Contents |
|---|---|
| `engine/v2/` | Source modules (VL, M0–M5) |
| `schema/v2/` | YAML knowledge graph (symptoms, faults, root_causes, edges, thresholds) |
| `schema/v1_reference/` | Frozen V1 schema (read-only) |
| `cases/csv/` | Test corpus (`cases_petrol_master_v6.csv`) |
| `tests/v2/` | Unit, integration, corpus, perturbation, KR3 suites |
| `tools/` | `build_vref_db.py`, dual-run harness |
| `docs/master_guides/` | Domain master guides |
| `results/` | Benchmark and corpus replay outputs |
