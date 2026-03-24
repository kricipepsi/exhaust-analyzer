#!/usr/bin/env python3
"""
Convert diagnostic_rules_enhanced.yaml to expanded_knowledge_base.json
"""

import yaml
import json
import sys
from pathlib import Path

# Severity to health_score mapping (based on instructions)
SEVERITY_MAP = {
    'critical': 20,
    'high': 40,
    'medium': 55,
    'low': 65
}

def parse_condition(cond_dict):
    """Convert condition dict to lambda expression string"""
    parts = []
    
    # Handle lambda/range conditions
    if 'lambda' in cond_dict:
        lam = cond_dict['lambda']
        if isinstance(lam, str):
            if lam.startswith('>'):
                val = lam[1:].rstrip('%')
                parts.append(f"calculated_lambda > {val}")
            elif lam.startswith('<'):
                val = lam[1:].rstrip('%')
                parts.append(f"calculated_lambda < {val}")
            elif '-' in lam:
                # Range: "0.85-0.95"
                low, high = lam.split('-')
                parts.append(f"{low} <= calculated_lambda <= {high}")
            else:
                parts.append(f"calculated_lambda == {lam}")
        else:
            # numeric value
            parts.append(f"calculated_lambda == {lam}")
    
    # Handle other conditions like obd_lambda, obd_stft, nox, etc.
    for key, val in cond_dict.items():
        if key == 'lambda':
            continue
        if isinstance(val, str):
            if val.startswith('>'):
                parts.append(f"{key} > {val[1:]}")
            elif val.startswith('<'):
                parts.append(f"{key} < {val[1:]}")
            elif val == 'none':
                parts.append(f"{key} is None")
            elif val.startswith("'") and ".." in val:
                # Example: "0.15-0.99"
                low, high = val.strip("'").split('-')
                parts.append(f"{low} <= {key} <= {high}")
            else:
                parts.append(f"{key} == {val}")
        else:
            parts.append(f"{key} == {val}")
    
    return ' and '.join(parts) if parts else 'True'

def build_logic(rule):
    """Build the logic string from gas_signs and condition"""
    logic_parts = []
    
    # Convert gas_signs
    gas_signs = rule.get('gas_signs', {})
    for gas, cond in gas_signs.items():
        if isinstance(cond, str):
            if cond.startswith('>'):
                # Remove % and convert to float
                val_str = cond[1:].rstrip('%')
                try:
                    val = float(val_str)
                except:
                    val = val_str
                if gas in ['co', 'o2', 'co2']:
                    logic_parts.append(f"low_idle.{gas} > {val}")
                else:  # hc, nox
                    logic_parts.append(f"low_idle.{gas} > {val}")
            elif cond.startswith('<'):
                val_str = cond[1:].rstrip('%')
                try:
                    val = float(val_str)
                except:
                    val = val_str
                logic_parts.append(f"low_idle.{gas} < {val}")
            elif cond.startswith("'") and '-' in cond:
                # Range like "2-4%" inside quotes
                range_str = cond.strip("'")
                if '-' in range_str:
                    low, high = range_str.split('-')
                    # Remove % if present
                    low = low.rstrip('%')
                    high = high.rstrip('%')
                    try:
                        low_f = float(low)
                        high_f = float(high)
                        logic_parts.append(f"{low_f} <= low_idle.{gas} <= {high_f}")
                    except:
                        logic_parts.append(f"low_idle.{gas} in range")
            elif cond == 'high':
                # Qualitative: treat as > typical threshold
                if gas == 'co':
                    logic_parts.append("low_idle.co > 2.0")
                elif gas == 'hc':
                    logic_parts.append("low_idle.hc > 1000")
                elif gas == 'o2':
                    logic_parts.append("low_idle.o2 > 2.0")
                elif gas == 'co2':
                    logic_parts.append("low_idle.co2 > 10.0")
                else:
                    logic_parts.append(f"low_idle.{gas} > 0")
            elif cond == 'low':
                if gas == 'co':
                    logic_parts.append("low_idle.co < 0.5")
                elif gas == 'hc':
                    logic_parts.append("low_idle.hc < 100")
                elif gas == 'o2':
                    logic_parts.append("low_idle.o2 < 0.5")
                elif gas == 'co2':
                    logic_parts.append("low_idle.co2 < 10.0")
                else:
                    logic_parts.append(f"low_idle.{gas} < 100")
        elif isinstance(cond, (int, float)):
            # Simple equality
            logic_parts.append(f"low_idle.{gas} == {cond}")
        elif isinstance(cond, list):
            # Range as list? Not seen in data but handle
            pass
    
    # Add condition part
    condition_dict = rule.get('condition', {})
    if condition_dict:
        cond_expr = parse_condition(condition_dict)
        if cond_expr != 'True':
            logic_parts.append(cond_expr)
    
    # Combine all parts with 'and'
    if logic_parts:
        return ' and '.join(logic_parts)
    else:
        return "True"  # Should not happen for valid rules

def create_case_entry(rule, existing_ids):
    """Convert a rule to a case entry"""
    case_id = rule['id']
    
    # Skip if ID already exists
    if case_id in existing_ids:
        return None
    
    existing_ids.add(case_id)
    
    name = rule['name']
    logic = build_logic(rule)
    
    # Map severity to health_score
    severity = rule.get('severity', 'medium').lower()
    health_score = SEVERITY_MAP.get(severity, 55)
    
    # Build verdict: "<rule name> - <summary of condition>"
    # Use first part of condition or gas_signs as summary
    verdict_parts = [name]
    
    # Add brief condition summary
    condition = rule.get('condition', {})
    if condition:
        cond_str = " and ".join([f"{k}={v}" for k, v in condition.items()])
        verdict_parts.append(f"Condition: {cond_str}")
    elif rule.get('gas_signs'):
        gases = [f"{k}={v}" for k, v in rule['gas_signs'].items()]
        verdict_parts.append("Gas signs: " + ", ".join(gases[:3]))
    
    verdict = " - ".join(verdict_parts)
    
    # Build action
    causes = rule.get('possible_causes', [])
    if causes:
        action = "Follow diagnostic procedure for: " + "; ".join(causes)
    else:
        action = "Perform comprehensive diagnostic based on gas patterns."
    
    return {
        "case_id": case_id,
        "name": name,
        "logic": logic,
        "health_score": health_score,
        "verdict": verdict,
        "action": action
    }

def main():
    workspace = Path(__file__).resolve().parent
    yaml_path = workspace.parent / "ARCHIVE" / "diagnostic_rules_enhanced.yaml"
    master_path = workspace / "data" / "master_knowledge_base.json"
    output_path = workspace / "data" / "expanded_knowledge_base.json"
    
    # Load YAML
    print(f"Loading YAML from: {yaml_path}")
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    
    rules = yaml_data.get('rules', [])
    print(f"Total rules in YAML: {len(rules)}")
    
    # Load existing master knowledge base to get existing case IDs
    print(f"Loading master knowledge base from: {master_path}")
    with open(master_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)
    
    existing_ids = set()
    for case in master_data.get('diagnostic_matrix', []):
        existing_ids.add(case['case_id'])
    print(f"Existing case IDs: {len(existing_ids)}")
    
    # Process rules
    new_cases = []
    skipped = []
    
    for rule in rules:
        try:
            case = create_case_entry(rule, existing_ids)
            if case:
                new_cases.append(case)
            else:
                skipped.append(f"Duplicate ID: {rule['id']}")
        except Exception as e:
            skipped.append(f"Rule {rule.get('id', 'unknown')}: {str(e)}")
    
    print(f"New cases generated: {len(new_cases)}")
    print(f"Rules skipped: {len(skipped)}")
    
    # Build expanded knowledge base
    expanded_data = master_data.copy()
    expanded_data['diagnostic_matrix'].extend(new_cases)
    
    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(expanded_data, f, indent=2)
    
    print(f"Saved expanded knowledge base to: {output_path}")
    print(f"Total cases in expanded matrix: {len(expanded_data['diagnostic_matrix'])}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Total rules in YAML: {len(rules)}")
    print(f"Selected and added: {len(new_cases)}")
    print(f"Skipped: {len(skipped)}")
    
    # List new case IDs (first 10 and last 10)
    new_ids = [c['case_id'] for c in new_cases]
    print("\nNew case IDs (first 10):")
    for cid in new_ids[:10]:
        print(f"  - {cid}")
    if len(new_ids) > 20:
        print("\nNew case IDs (last 10):")
        for cid in new_ids[-10:]:
            print(f"  - {cid}")
    
    if skipped:
        print("\nSkipped rules:")
        for s in skipped[:20]:  # limit output
            print(f"  - {s}")
        if len(skipped) > 20:
            print(f"  ... and {len(skipped)-20} more")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
