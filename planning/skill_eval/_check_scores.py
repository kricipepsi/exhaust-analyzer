import json
with open("results/cohort_housestyle_scored.jsonl") as f:
    recs = [json.loads(line) for line in f]

# Spot-check: task_01 arm A vs B/python
for r in recs:
    if r["task_id"] == "task_01_string_tools" and r["arm"] == "A" and r["seed"] == 42:
        print(f"A (seed=42): rubric_total={r['rubric_total']} readability={r['rubric_readability']} structure={r['rubric_structure']} naming={r['rubric_naming']}")
    if r["task_id"] == "task_01_string_tools" and r["arm"] == "B" and r["skill_id"] == "python" and r["seed"] == 42:
        print(f"B/python (seed=42): rubric_total={r['rubric_total']} readability={r['rubric_readability']} structure={r['rubric_structure']} naming={r['rubric_naming']}")

# task_03 hallucinated-API
for r in recs:
    if r["task_id"] == "task_03_trap_api" and r["seed"] == 42:
        print(f"task_03 {r['arm']}/{r['skill_id']}: hallu_imports={r['hallucinated_imports']} first_pyright={r['first_pyright_errors']} rubric_total={r['rubric_total']}")
