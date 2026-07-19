# AST Graph Evaluation — Registry Package and Test Suite

This document records the health-check verdicts for the Pass-1 AST graphs built for the registry package and its test suite.

---

## 1. Registry Package Code Graph

- **Target Path:** `labs/comlab/registry/graph/v2_code/graph.json`
- **Source Scope:** `labs/comlab/registry/` (excluding `tests/`, `docs/`, and `graph/`)
- **Extraction Pass:** Pass-1 (tree-sitter AST, offline, free)
- **Evaluation Command:**
  ```bash
  python3 _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/comlab/registry/graph/v2_code/graph.json
  ```

### Verdict Output

```
# Graph health — code graph (`labs/comlab/registry/graph/v2_code/graph.json`)

Single-graph condition check (reads the canonical graph only — no LLM pass, no re-extraction).

| metric | value |
|---|---|
| nodes | 206 |
| links | 363 |
| density | 0.0086 |
| dangling | 0 |
| isolated | 0 |
| confidence split | {'EXTRACTED': 269, 'INFERRED': 94} |
| top hubs (degree) | integration_shim:25, integration_shim_observation:24, rule:21, integration_shim_py_any:20, integration_shim_registryv2router:19 |

**Condition: GOOD.**
- 0 dangling, 0 isolated — graph is structurally sound.
```

---

## 2. Registry Test Suite Graph

- **Target Path:** `labs/comlab/registry/graph/v2_tests/graph.json`
- **Source Scope:** `labs/comlab/registry/tests/`
- **Extraction Pass:** Pass-1 (tree-sitter AST, offline, free)
- **Evaluation Command:**
  ```bash
  python3 _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/comlab/registry/graph/v2_tests/graph.json
  ```

### Verdict Output

```
# Graph health — code graph (`labs/comlab/registry/graph/v2_tests/graph.json`)

Single-graph condition check (reads the canonical graph only — no LLM pass, no re-extraction).

| metric | value |
|---|---|
| nodes | 824 |
| links | 1258 |
| density | 0.0019 |
| dangling | 0 |
| isolated | 0 |
| confidence split | {'EXTRACTED': 1254, 'INFERRED': 4} |
| top hubs (degree) | test_overheating_rules:36, test_mechanical_wear_rules:35, test_sensor_fault_rules:35, test_cam_timing_rules:34, test_vacuum_leak_rules:33 |

**Condition: GOOD.**
- 0 dangling, 0 isolated — graph is structurally sound.
```
