# T-SE-0 — Finalize methodology + blinded rubric + success bar

**Status:** authored · impl pending · **Blocked by:** — · **Pack:** `planning/skill_eval/`
**Mode:** STRICT
**Load skills (session start):** read `SKILL_EVAL_START_HERE.md`; sandbox Python 3.14;
mandatory pair (`codingskills/pythonskill/python` + `ecc-subset/verification-loop`).

## Goal

Turn `SKILL_EVAL_CONTRACT.md` (architect draft) into the frozen measurement spec the
A/B tasks bind to: the blinded judge rubric, the exact success bar, and the metric
capture schema. Nothing downstream is sound until these are pinned.

## Deliverables

1. `rubric.md` — the 6-axis blinded review rubric (readability, structure, naming,
   cohesion, error-handling, test-meaningfulness), each axis 0–3 with concrete
   anchor descriptions per score. Judge instructions: blinded, K≥3 passes, mean±SD.
2. `metrics_schema.md` (or a typed dataclass in the runner) — the per-trial record:
   first-pass ruff/pyright/pytest counts, iterations-to-green, tokens, hallucinated-API
   count, rubric axes, objective proxies (complexity, mutation score, type/docstring
   coverage, diff churn), arm label, task id, skill id, seed.
3. Pin the **success bar** numerically in `SKILL_EVAL_CONTRACT.md` §5 (default:
   `mean(B) − mean(A) > max(SD(A), SD(B))`, i.e. ≥ 1 SD; confirm or change with Q-SE-2).

## Success criteria

- Rubric axes are mutually distinct and each has 0/1/2/3 anchors (no "vibes").
- The judge protocol names the blinding mechanism and the judge-≠-author rule.
- A reviewer can, from these files alone, score two code samples and decide KEEP/
  TRIM/CUT without re-reading the CONTRACT.

## Out of scope

Building the runner (T-SE-2) or running any trial. No skill is loaded *as a subject* here.

## Signal/noise consumer

The rubric + schema are consumed by every A/B task (T-SE-3..6) and T-SE-FINAL. No
metric ships without a consumer here: if an axis or field is read by no scoring step,
drop it.

## Verification

`rubric.md` + `metrics_schema.md` exist and are internally consistent with CONTRACT
§3–§5; a dry scoring of one sample produces a defensible number.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-SE-0.md`, opening with `## Plan`.)
