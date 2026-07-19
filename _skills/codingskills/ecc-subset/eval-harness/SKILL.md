---
name: eval-harness
description: Formal evaluation framework implementing eval-driven development (EDD) — define pass/fail criteria before implementation, measure agent reliability with pass@k metrics, create regression suites for accuracy benchmarks.
origin: ECC
---

# Eval Harness Skill

A formal evaluation framework for Claude Code sessions, implementing eval-driven development (EDD) principles. Particularly relevant for T12 (semantic evaluator) and T13 (re-baseline) in the 4DApp coder pack.

## When to Activate

- Designing the semantic evaluator (T12) — define what "correct" means before writing code
- Running the T13 re-baseline — structure the accuracy report as a formal eval report
- Setting up pass/fail criteria for accuracy gates across the 234-case corpus
- Measuring whether engine changes improve or regress diagnostic performance

## Philosophy

Eval-Driven Development treats evals as the "unit tests of AI development":
- Define expected behaviour **before** implementation
- Run evals continuously during development
- Track regressions with each change
- Use pass@k metrics for reliability measurement

## Eval Types

### Capability Evals
Test if the engine can do something it couldn't before:
```markdown
[CAPABILITY EVAL: semantic-evaluator]
Task: Correctly classify O2 sensor fault from gas readings alone
Success Criteria:
  - [ ] Lambda calculated correctly from Brettschneider formula
  - [ ] O2 fault node appears in top-3 results
  - [ ] Confidence > 0.7 for known-good test cases
Expected Output: ranked fault list with confidence scores
```

### Regression Evals
Ensure changes don't break existing accuracy:
```markdown
[REGRESSION EVAL: post-T06-refactor]
Baseline: pre-T06 accuracy = 71% on 234-case corpus
Tests:
  - lean_misfire_cases:    PASS/FAIL (X/20)
  - rich_mixture_cases:    PASS/FAIL (X/15)
  - o2_sensor_cases:       PASS/FAIL (X/18)
Result: X/234 passed (baseline: Y/234)
```

## Grader Types

### 1. Code-Based Grader (preferred for 4DApp)
Deterministic checks:
```bash
# Run pytest suite
cd exhaust-analyzer-main && python -m pytest tests/ -x --tb=short

# Run 25-case fast benchmark
python tests/run_accuracy_benchmark.py

# Run full corpus replay
python run_dual_engine_comparison.py
python analyze_engine_a_failures.py
```

### 2. Model-Based Grader
Use for semantic evaluator quality assessment:
```markdown
[MODEL GRADER PROMPT]
Given this engine output and the known ground-truth fault:
1. Is the correct fault node in the top-3 results?
2. Is the confidence ranking appropriate given the gas chemistry?
3. Is the specific fault ranked above any generic fallback?
Score: PASS / PARTIAL / FAIL
Reasoning: [explanation]
```

## Metrics

### pass@k
"At least one success in k attempts"
- pass@1: First attempt success rate
- pass@3: Success within 3 attempts
- Target for capability evals: pass@3 >= 90%

### Accuracy as eval metric (4DApp-specific)
- Layer-2 corpus accuracy is the primary regression eval metric
- Any task that touches model output must show accuracy >= baseline
- Record in PROGRESS.md: `Accuracy: X/234 (baseline: Y/234)`

## Eval Workflow for T12 (Semantic Evaluator)

### 1. Define (before writing a line of code)
```markdown
## EVAL DEFINITION: semantic-evaluator-T12

### Capability Evals
1. Evaluator correctly scores a known-good diagnosis (confidence > 0.7)
2. Evaluator correctly penalises generic-over-specific ranking
3. Evaluator handles missing PIDs gracefully (no crash)
4. Evaluator output is deterministic for same input

### Regression Evals
1. Layer-1 pytest suite still green after evaluator added
2. Layer-2 accuracy >= pre-T12 baseline
3. No new attractor nodes introduced

### Success Metrics
- pass@3 >= 90% for capability evals
- pass^3 = 100% for regression evals (must be stable)
- Layer-2 accuracy: no regression vs. T11 checkpoint
```

### 2. Implement → Evaluate → Report
```markdown
EVAL REPORT: semantic-evaluator-T12
=====================================

Capability Evals:
  correct-score-good-case:    PASS (pass@1)
  penalise-generic-ranking:   PASS (pass@2)
  missing-pids-graceful:      PASS (pass@1)
  deterministic-output:       PASS (pass@1)
  Overall: 4/4

Regression Evals:
  layer-1-pytest:   PASS (X tests green)
  layer-2-accuracy: PASS (X/234, baseline Y/234)
  no-new-attractors: PASS
  Overall: 3/3

Metrics:
  pass@1: 75%
  pass@3: 100%

Status: READY — flip T12 to done in PROGRESS.md
```

## Eval Storage

```
exhaust-analyzer-main/
  .claude/
    evals/
      T12-semantic-evaluator.md    # Eval definition
      T13-rebaseline.md            # Eval definition
      baseline.json                # Accuracy baselines per checkpoint
```

## Best Practices

1. **Define evals BEFORE coding** — forces clear thinking about what "done" means
2. **Run evals frequently** — catch regressions early
3. **Keep evals fast** — Layer-1 pytest must stay under 30 seconds
4. **Version evals with code** — evals are first-class artifacts, commit them
5. **Never skip Layer-2 for model-touching tasks** — T05–T09, T12, T13 all require it
