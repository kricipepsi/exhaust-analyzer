import json
from collections import Counter

with open('diagnostic_suite_failures.json', 'r') as f:
    fails = json.load(f)

print(f"Total failures: {len(fails)}")
cats = Counter()
for entry in fails:
    # entry could be [id, expected, actual] or dict
    if isinstance(entry, dict):
        exp = entry.get('expected') or entry.get('Expected_Result') or 'UNKNOWN'
    else:
        exp = entry[1] if len(entry) > 1 else 'UNKNOWN'
    cats[exp] += 1

print("\nBreakdown by expected category:")
for cat, cnt in cats.most_common():
    print(f"  {cat}: {cnt}")
