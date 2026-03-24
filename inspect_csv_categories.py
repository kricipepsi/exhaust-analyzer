import csv
path = r"C:\Users\asus\Documents\1nov\diagnostic_test_suite.csv"
with open(path, 'r', encoding='utf-16') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Group by Expected_Result and show sample DTCs and O2 ranges
from collections import defaultdict
groups = defaultdict(list)
for r in rows:
    groups[r['Expected_Result']].append(r)

print("Category counts:")
for cat, items in sorted(groups.items()):
    print(f"{cat}: {len(items)}")
    # Show DTC variety
    dtcs = set(item['OBD_DTC'] for item in items)
    print(f"  DTCs: {sorted(dtcs)}")
    # Show O2 range
    o2_vals = [float(item['O2_Pct']) for item in items]
    print(f"  O2 range: {min(o2_vals):.2f} - {max(o2_vals):.2f}")
    # Show lambda range
    lam_vals = [float(item['Lambda_Gas']) for item in items]
    print(f"  Lambda range: {min(lam_vals):.3f} - {max(lam_vals):.3f}")
    print()