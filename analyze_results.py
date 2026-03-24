import json
from collections import Counter

with open('diagnostic_suite_results.json','r') as f:
    data = json.load(f)

total = data['total']
passed = data['passed']
failed = data['failed']
print(f"TOTAL: {total}, PASSED: {passed}, FAILED: {failed}, ACCURACY: {passed/total*100:.1f}%")

# The results list may be in the data; if not, we'll derive from failures file
if 'results' in data:
    results = data['results']
else:
    # Load failures file
    with open('diagnostic_suite_failures.json','r') as f:
        fails = json.load(f)
    # Build a simple breakdown by expected result
    # We need mapping from test ID to expected; we'll parse CSV again
    import csv
    tests = {}
    with open(r"C:\Users\asus\Documents\1nov\diagnostic_test_suite.csv", 'r', encoding='utf-16') as f:
        for row in csv.DictReader(f):
            tests[row['ID']] = row['Expected_Result']
    # Count failures by expected
    cat_fails = Counter()
    for fid, exp, act in fails:
        cat_fails[exp] += 1
    print("\nFailure breakdown by expected category:")
    for cat, cnt in cat_fails.most_common():
        print(f"  {cat}: {cnt}")
else:
    # If we have results list with match flags
    results = data.get('results', [])
    # Group by expected result
    by_expected = {}
    for r in results:
        exp = r.get('expected', 'UNKNOWN')
        match = r.get('match', False)
        if exp not in by_expected:
            by_expected[exp] = {'passed':0, 'failed':0}
        if match:
            by_expected[exp]['passed'] += 1
        else:
            by_expected[exp]['failed'] += 1
    print("\nBreakdown by expected category:")
    for exp, counts in sorted(by_expected.items()):
        total_cat = counts['passed']+counts['failed']
        pct = counts['passed']/total_cat*100 if total_cat else 0
        print(f"  {exp}: {counts['passed']}/{total_cat} passed ({pct:.1f}%)")