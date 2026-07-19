# T-SE-0 — Progress Note

**Task:** Finalize methodology + blinded rubric + success bar · **Date:** 2026-06-09 · **Coder:** architect (acting coder per bootstrap)

## Plan

1. Write `rubric.md` — 6-axis blinded reviewer rubric (readability, structure, naming, cohesion, error-handling, test-meaningfulness), each axis 0–3 with concrete anchor descriptions. Include blinding protocol (opaque IDs, random order, separate session, no task-context leakage, K≥3 passes) and judge-≠-author rule.
2. Write `metrics_schema.md` — per-trial record: trial identity, first-pass gate counts, convergence cost (iterations/tokens/time), hallucinated-API counts, rubric axes (mean±SD per axis), objective proxies (complexity, mutation score, type/docstring coverage, diff churn). Include Python dataclass reference and per-cohort primary-metric mapping.
3. Edit `SKILL_EVAL_CONTRACT.md` §5 — pin the frozen success bar: ≥1 SD effect (Cohen's d ≥ 1.0), edge cases (SD=0, negative effect, multi-metric skills), verdict table, and reporting requirements.
4. Write this progress note with dual gates.

---

## VERIFICATION GATE

```
VERIFICATION GATE — T-SE-0
===========================
rubric.md exists:         PASS (91 lines, 6 axes × 4 anchors each)
metrics_schema.md exists: PASS (6 sections, 30+ fields, dataclass ref + per-cohort mapping)
CONTRACT §5 frozen:       PASS (5.1–5.5, Cohen's d ≥ 1.0 pinned, edge cases codified)

Internal consistency:
  rubric axes ↔ CONTRACT §4 names:            PASS (exact match on all 6)
  metrics_schema.rubric_* ↔ rubric axes:      PASS (field-per-axis + sd + total)
  metrics_schema fields ⊇ CONTRACT §3 list:   PASS (all 6 metric groups covered)
  success bar references rubric + schema:     PASS (5.2 uses rubric total; 5.5 uses schema fields)
  per-cohort primary mapping ↔ ledger table:  PASS (SE-3/4/5/6 cohorts match)

Blinding protocol:        PASS (5 rules: opaque IDs, random order, separate session,
                            no task-context leakage, K≥3)
Judge-≠-author rule:      PASS (separate session minimum; different model preferred)

Dry-scoring check:
  Can a reviewer score two code samples from rubric.md alone, without re-reading CONTRACT?
  → rubric.md is self-contained: axes, anchors, scoring rules, output format, aggregation
    all defined in one file. VERDICT: PASS

No Python code, no inner loop required (methodology task).

Status: DONE
```

---

## CODE REVIEW

Self-review against task spec (T-SE-0_methodology_and_rubric.md):

- **Deliverable 1 (rubric.md):** 6 axes, each 0–3 with concrete anchor descriptions. No "vibes" — every score level names a specific observable property. Blinding mechanism (5 rules) and judge-≠-author rule both explicit. PASS.
- **Deliverable 2 (metrics_schema.md):** Covers first-pass counts, iterations-to-green, tokens, hallucinated-API, rubric axes, objective proxies, arm/task/skill/seed labels — all CONTRACT §3 fields present. Python dataclass reference included. Per-cohort primary-metric mapping reconciles with ledger. PASS.
- **Deliverable 3 (CONTRACT §5 pinned):** Success bar frozen at Cohen's d ≥ 1.0 (`mean(B) − mean(A) > max(SD(A), SD(B))`). Edge cases codified: SD=0 on both arms (→null), SD=0 on one arm, negative effect (→CUT), multi-metric skills. Verdict table + reporting format. PASS.
- **Success criteria:** Rubric axes mutually distinct (each covers a different quality dimension — readability ≠ naming ≠ cohesion, etc.). Reviewer can score from these files alone without re-reading CONTRACT (rubric.md is self-contained; metrics_schema.md defines the capture; CONTRACT §5 defines the decision rule). PASS.
- **Out of scope:** No runner built, no trial run, no skill loaded as subject. PASS.
- **Signal/noise consumer:** The rubric + schema are consumed by every A/B task (T-SE-3..6) and T-SE-FINAL. Per-cohort mapping in metrics_schema.md §6 names which metrics each cohort reads. Confirmed.
- **No scope creep.** Three files, exactly the contracted deliverables.

No edits to any skill file, no imports from ARCHIVE/v2/v6.
