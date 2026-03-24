import json
with open('diagnostic_suite_failures.json','r') as f:
    fails = json.load(f)
print(f"Total failures: {len(fails)}")
print("\nFirst 20 failures:")
count = 0
for entry in fails:
    if count >= 20:
        break
    if isinstance(entry, (list, tuple)) and len(entry) >= 3:
        tid, exp, act = entry[0], entry[1], entry[2]
    elif isinstance(entry, dict):
        tid = entry.get('ID', 'N/A')
        exp = entry.get('expected', entry.get('Expected_Result','N/A'))
        act = entry.get('actual', entry.get('Actual','N/A'))
    else:
        tid = exp = act = '???'
    print(f"{tid}: expected '{exp}', got '{act}'")
    count += 1