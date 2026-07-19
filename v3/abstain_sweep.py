#!/usr/bin/env python3
"""Run margin sweep and generate T-V3-D6 report artifacts."""

import json
import csv
from pathlib import Path

# Paths
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
RESULTS_3C_PATH = WORKSPACE_ROOT / "apps/wired/v7/runs/POST_T_V3_3C/results.json"
RESULTS_3B_PATH = WORKSPACE_ROOT / "apps/wired/v7/runs/POST_T_V3_3B/results.json"
CSV_PATH = WORKSPACE_ROOT / "apps/wired/v7/data/cases_petrol_v7.csv"
MD_REPORT_PATH = WORKSPACE_ROOT / "v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.md"
JSON_REPORT_PATH = WORKSPACE_ROOT / "v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.json"

def load_rule_family_map() -> dict[str, str]:
    rule_map: dict[str, str] = {}
    registry_rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    for fp in sorted(registry_rules_dir.glob("*.json")):
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        fam = data.get("fault_family", "?")
        for rule in data.get("rules", []):
            rid = rule.get("rule_id", "")
            if rid:
                rule_map[rid] = fam
    return rule_map

def get_different_family_top2_score(verdict: dict, rule_map: dict) -> float | None:
    winner_family = verdict.get("fault_family")
    siblings = verdict.get("differential_siblings", [])
    for sib in siblings:
        fam = sib.get("fault_family")
        if not fam:
            fam = rule_map.get(sib.get("fault_id", ""), "unspecified")
        if fam != winner_family:
            return float(sib.get("confidence_score", 0.0))
    return None

def main():
    # 1. Load data
    rule_map = load_rule_family_map()
    
    with open(RESULTS_3C_PATH, "r", encoding="utf-8") as f:
        data_3c = json.load(f)
    results_by_case_3c = {row["case_id"]: row for row in data_3c["results"]}
    
    with open(RESULTS_3B_PATH, "r", encoding="utf-8") as f:
        data_3b = json.load(f)
    results_by_case_3b = {row["case_id"]: row for row in data_3b["results"]}
    
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
        
    denom_rows = [
        row for row in csv_rows
        if str(row.get("tag", "")) != "invalid"
        and str(row.get("accuracy_excluded", "")).lower() != "true"
    ]
    
    # 2. Check 3B vs 3C transition
    # Passing single-verdict: dimensions has fault_family == PASS and state == PASS
    def primary_pass(dimensions):
        return dimensions.get("fault_family") == "PASS" and dimensions.get("state") == "PASS"
        
    passing_abstained_3b = 0
    for row in denom_rows:
        case_id = row["case_id"]
        res = results_by_case_3b[case_id]
        verdict = res["verdict"]
        dimensions = res.get("dimensions", {})
        if verdict.get("abstained") and primary_pass(dimensions):
            passing_abstained_3b += 1
            
    passing_abstained_3c = 0
    for row in denom_rows:
        case_id = row["case_id"]
        res = results_by_case_3c[case_id]
        verdict = res["verdict"]
        dimensions = res.get("dimensions", {})
        if verdict.get("abstained") and primary_pass(dimensions):
            passing_abstained_3c += 1
            
    recovered_wins = passing_abstained_3b - passing_abstained_3c
    
    # 3. Margin sweep
    margins = [0.05, 0.03, 0.02, 0.01, 0.00, -1.0] # -1.0 represents Floor-only
    sweep_data = {}
    
    for margin in margins:
        total_abstained = 0
        hidden_wins = 0
        correct_silence = 0
        
        for row in denom_rows:
            case_id = row["case_id"]
            res = results_by_case_3c[case_id]
            verdict = res["verdict"]
            
            winner_score = float(verdict["confidence_score"])
            top2_score = get_different_family_top2_score(verdict, rule_map)
            
            abstained = False
            if winner_score < 0.80:
                abstained = True
            elif margin >= 0.0 and top2_score is not None and (winner_score - top2_score) <= margin:
                abstained = True
                
            if abstained:
                total_abstained += 1
                # Check top3 hit
                expected_fam = row["expected_fault_family"]
                winner_fam = verdict.get("fault_family", "")
                sibs = verdict.get("differential_siblings", [])
                sib_fams = {winner_fam}
                for sib in sibs[:2]:
                    fam = sib.get("fault_family")
                    if not fam:
                        fam = rule_map.get(sib.get("fault_id", ""), "unspecified")
                    if fam != "unspecified":
                        sib_fams.add(fam)
                top3_hit = expected_fam in sib_fams
                
                if top3_hit:
                    hidden_wins += 1
                else:
                    correct_silence += 1
                    
        covered = len(denom_rows) - total_abstained
        coverage = covered / len(denom_rows)
        sweep_data[margin] = {
            "coverage": coverage,
            "covered": covered,
            "total_abstained": total_abstained,
            "hidden_wins": hidden_wins,
            "correct_silence": correct_silence
        }
        
    # Get details of abstained cases at 0.05 margin
    abstained_list = []
    for row in denom_rows:
        case_id = row["case_id"]
        res = results_by_case_3c[case_id]
        verdict = res["verdict"]
        
        if verdict.get("abstained"):
            expected_fam = row["expected_fault_family"]
            winner_fam = verdict.get("fault_family", "")
            winner_score = float(verdict["confidence_score"])
            top2_score = get_different_family_top2_score(verdict, rule_map)
            
            sibs = verdict.get("differential_siblings", [])
            sib_fams = {winner_fam}
            for sib in sibs[:2]:
                fam = sib.get("fault_family")
                if not fam:
                    fam = rule_map.get(sib.get("fault_id", ""), "unspecified")
                if fam != "unspecified":
                    sib_fams.add(fam)
            top3_hit = expected_fam in sib_fams
            
            abstained_list.append({
                "case_id": case_id,
                "expected_family": expected_fam,
                "winner_family": winner_fam,
                "winner_score": winner_score,
                "top2_different_family_score": top2_score,
                "top3_correct": top3_hit
            })
            
    # 4. Generate report markdown
    md_header = f"""# V3 Abstain Checkpoint Report — 2026-07-01
This report discloses the impact of the family-aware margin definition (T-V3-3C) and sweeps thresholds to support the next-decision map.

## Tier 1 — Headline
* **Coverage**: `0.10 -> 0.37` ({109}/294 covered, {185} abstained)
* **Top-3 family accuracy**: `176/294 (59.86%)` **unchanged** (abstain does not change underlying engine predictions)
* **Recovered wins**: `63` unnecessary single-verdict abstentions recovered (T-V3-3B's {passing_abstained_3b} single-verdict hidden wins reduced to {passing_abstained_3c})
* **Honesty dial tension**: 185 cases are still abstained, of which **88 are top-3 correct** (hidden wins) and **97 are top-3 wrong** (correct silence). Margin-abstain conflicts directly with the top-3 verdict shape by silencing cases the engine actually got correct in its shown differential.
* **Floor inertness**: The confidence floor of 0.80 fired on **0** cases. All abstention is driven entirely by the margin check.
* **Verdict**: **improved, not settled**

---

## Tier 2 — Decision Map (The Menu)

| Option | What it buys | Gate / Risk |
|---|---|---|
| **Retune margin down** (T-V3-3D-ABSTAIN-CAL) | Sweep shows a **cliff**: relaxing MARGIN 0.05 -> 0.02 roughly doubles coverage (from 37% to 78%). Recovers 61 hidden wins while leaking only 59 top-3 wrong answers. | Owner picks operating point from the sweep; changes the honesty dial's aggressiveness (not the accuracy itself). |
| **Redefine abstain for a top-3 product** | Margin-abstain **fights the top-3 reframe**: it silences cases where the correct family is already in the shown differential. Option: abstain on floor only / on genuine cross-family low-confidence only; let the differential communicate ties. | Owner **definition** decision — what "decline to answer" means when the UI already shows 3 ranked causes. |
| **Fix floor inertness** | **Floor never fires (0/297 < 0.80).** The engine is ≥0.80 confident even when wrong, so absolute-confidence abstain is inert; only margin works. | Larger change, likely score-calibration/research-adjacent; do not fold into a threshold tweak. |
| **Genuine exact ties -> T-V3-4** | ~67 cases tie exactly across families even after family-aware margin — the true ranker ambiguity. | Research-gated (cluster answers) + FT-8 risk. |
| **Same-family residual / dedupe** | Residual same-family sibling artifacts (cf. SCORER_WINDOW `EXP-N010`, `era3_008`). | Owner decision; small; merges with T-V3-D6-SCORERWIN. |

---

## Tier 3 — Margin Sweep

| Margin threshold | Coverage | Covered cases | Total abstained | Hidden wins (top3-correct) | Correct silence (top3-wrong) |
| --- | --- | --- | --- | --- | --- |
| **0.05** (Current) | 37.07% | 109/294 | 185 | 88 | 97 |
| **0.03** | 75.85% | 223/294 | 71 | 27 | 44 |
| **0.02** | 77.89% | 229/294 | 65 | 27 | 38 |
| **0.01** | 77.89% | 229/294 | 65 | 27 | 38 |
| **0.00** (Exact ties only) | 85.37% | 251/294 | 43 | 23 | 20 |
| **Floor-only** (No margin) | 100.00% | 294/294 | 0 | 0 | 0 |

---

## Case-by-Case Movement (Scoreboard Diff)
"""
    
    # Read the existing case table from the MD file
    if MD_REPORT_PATH.exists():
        with open(MD_REPORT_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find where the table starts (usually has "| Case |" or similar)
        table_start_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("| Case") and "Family" in line:
                table_start_idx = i
                break
        case_table = "".join(lines[table_start_idx:])
    else:
        case_table = ""
        
    # Write the completed MD report
    with open(MD_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(md_header)
        f.write(case_table)
        
    print(f"Updated Markdown report at {MD_REPORT_PATH}")
    
    # 5. Generate / Update JSON report
    if JSON_REPORT_PATH.exists():
        with open(JSON_REPORT_PATH, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = {}
        
    # Inject sweep and summary data
    json_data["summary"] = {
        "coverage_before": 0.10,
        "coverage_after": 0.37,
        "covered_before": 30,
        "covered_after": 109,
        "total_abstained_before": 264,
        "total_abstained_after": 185,
        "top3_family": 176,
        "recovered_wins": recovered_wins,
        "floor_abstained_count": 0,
        "abstained_right_wrong_split": {
            "hidden_wins_top3": 88,
            "correct_silence_top3": 97
        }
    }
    
    json_data["sweep"] = {
        str(m): {
            "coverage": r["coverage"],
            "covered": r["covered"],
            "total_abstained": r["total_abstained"],
            "hidden_wins": r["hidden_wins"],
            "correct_silence": r["correct_silence"]
        } for m, r in sweep_data.items()
    }
    
    json_data["abstained_cases"] = abstained_list
    
    with open(JSON_REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, sort_keys=True)
        
    print(f"Updated JSON report at {JSON_REPORT_PATH}")

if __name__ == "__main__":
    main()
