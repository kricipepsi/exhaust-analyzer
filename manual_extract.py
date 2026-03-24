#!/usr/bin/env python3
"""Extract more diagnostic rules from YAML and append to expanded KB."""

import json
import re
from pathlib import Path

# Load existing expanded KB
with open('data/expanded_knowledge_base.json', 'r') as f:
    kb = json.load(f)

# Load the enhanced rules YAML
_script_dir = Path(__file__).resolve().parent
with open(_script_dir.parent / 'ARCHIVE' / 'diagnostic_rules_enhanced.yaml', 'r') as f:
    yaml_content = f.read()

# Simple regex extraction of rule blocks
# Each rule starts with "- id: <name>"
rule_blocks = re.split(r'\n(?=- id:)', yaml_content)
print(f"Found {len(rule_blocks)} rule blocks in YAML")

# Parse each block for id, name, gas_signs, condition
def parse_rule(block):
    try:
        # Extract id
        id_match = re.search(r'id:\s*(.+?)\s*$', block, re.MULTILINE)
        if not id_match:
            return None
        rule_id = id_match.group(1).strip().replace(' ', '_').lower()

        # Extract name
        name_match = re.search(r'name:\s*(.+?)\s*$', block, re.MULTILINE)
        name = name_match.group(1).strip() if name_match else rule_id

        # Extract gas_signs
        gas_signs = {}
        gas_section = re.search(r'gas_signs:(.*?)(?=\n\s{2,}[a-z]|$)', block, re.DOTALL)
        if gas_section:
            for line in gas_section.group(1).split('\n'):
                m = re.match(r'\s*([a-z]+):\s*[\'"]?([<>]?\d+%?)(?:-(\d+%?))?[\'"]?', line.strip())
                if m:
                    key = m.group(1)
                    val = m.group(2)
                    gas_signs[key] = val

        # Extract condition.lambda
        lambda_match = re.search(r'lambda:\s*[\'"]?([<>]?\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)[\'"]?', block)
        lambda_cond = lambda_match.group(1) if lambda_match else None

        # Extract possible_causes
        causes = []
        in_causes = False
        for line in block.split('\n'):
            if re.match(r'\s*- ', line):
                in_causes = True
                cause = re.sub(r'^-\s*', '', line).strip()
                if cause:
                    causes.append(cause)
            elif in_causes and line.strip() and not line.startswith(' '):
                break

        return {
            'id': rule_id,
            'name': name,
            'gas_signs': gas_signs,
            'lambda': lambda_cond,
            'causes': causes
        }
    except Exception as e:
        print(f"Error parsing block: {e}")
        return None

parsed_rules = []
for block in rule_blocks:
    rule = parse_rule(block)
    if rule and rule['id'] and rule['name'] and rule['lambda'] and rule['gas_signs']:
        parsed_rules.append(rule)

print(f"Successfully parsed {len(parsed_rules)} rules")

# Build case_id to avoid duplicates
existing_ids = set(c['case_id'] for c in kb['diagnostic_matrix'])
new_cases = []
added = 0

for rule in parsed_rules:
    # Skip if already present
    if rule['id'] in existing_ids:
        continue

    # Build logic string
    logic_parts = []
    for key, val in rule['gas_signs'].items():
        # Convert >7% to > 7.0, <8% to < 8.0
        if val.startswith('>'):
            num = float(val[1:].replace('%',''))
            logic_parts.append(f"low_idle.{key} > {num}")
        elif val.startswith('<'):
            num = float(val[1:].replace('%',''))
            logic_parts.append(f"low_idle.{key} < {num}")
        elif '-' in val:
            # Range, but we'll define as both sides? Typically gas_signs are thresholds, not ranges
            # For simplicity, take lower bound as minimum
            low, high = val.split('-')
            low_num = float(low.replace('%',''))
            logic_parts.append(f"low_idle.{key} > {low_num}")
        else:
            # Exact? Treat as equality (rare)
            num = float(val.replace('%',''))
            logic_parts.append(f"low_idle.{key} == {num}")

    # Add lambda condition
    lam = rule['lambda']
    if lam.startswith('>'):
        num = float(lam[1:])
        logic_parts.append(f"calculated_lambda > {num}")
    elif lam.startswith('<'):
        num = float(lam[1:])
        logic_parts.append(f"calculated_lambda < {num}")
    elif '-' in lam:
        low, high = lam.split('-')
        low_num, high_num = float(low), float(high)
        logic_parts.append(f"{low_num} <= calculated_lambda <= {high_num}")
    else:
        # exact?
        num = float(lam)
        logic_parts.append(f"calculated_lambda == {num}")

    logic_str = ' and '.join(logic_parts)

    # Health score based on severity (from YAML if available, else default 55)
    severity_match = re.search(r'severity:\s*(high|medium|low)', rule.get('block', ''), re.IGNORECASE)
    if severity_match:
        sev = severity_match.group(1).lower()
        health = 40 if sev == 'high' else 55 if sev == 'medium' else 65
    else:
        health = 55

    case = {
        "case_id": rule['id'],
        "name": rule['name'],
        "logic": logic_str,
        "health_score": health,
        "verdict": f"{rule['name']} - Detected via gas signature",
        "action": "Inspect: " + "; ".join(rule['causes'][:3]) if rule['causes'] else "Further diagnostics required"
    }
    new_cases.append(case)
    added += 1
    existing_ids.add(rule['id'])

    if added >= 20:  # We only need ~20 to reach 50+ total
        break

# Append to KB
kb['diagnostic_matrix'].extend(new_cases)

# Save
with open(_script_dir / 'data' / 'expanded_knowledge_base.json', 'w') as f:
    json.dump(kb, f, indent=2)

print(f"\nAdded {added} new cases.")
print(f"New case IDs: {[c['case_id'] for c in new_cases][:10]}")
print(f"Total cases now: {len(kb['diagnostic_matrix'])}")
