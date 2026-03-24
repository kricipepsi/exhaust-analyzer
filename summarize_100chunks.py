#!/usr/bin/env python3
import json
from pathlib import Path

res_path = Path('test_100cvs_results.json')
if not res_path.exists():
    print("Results not found")
    exit(1)

data = json.loads(res_path.read_text())
results = data.get('results', [])
print(f"Total results entries: {len(results)}")

# Group by chunk of 20 based on ID like TC001
chunks = {i: [] for i in range(1,6)}
for r in results:
    cid = r['id']
    if cid.startswith('TC'):
        num = int(cid[2:])
        chunk_idx = (num-1)//20 + 1
        if 1 <= chunk_idx <= 5:
            chunks[chunk_idx].append(r)

for i in range(1,6):
    group = chunks[i]
    passed = sum(1 for c in group if c['match'])
    total = len(group)
    pct = passed/total*100 if total else 0
    print(f"Chunk {i}: {passed}/{total} ({pct:.1f}%)")

overall_passed = sum(1 for r in results if r['match'])
overall_total = len(results)
print(f"\nOVERALL: {overall_passed}/{overall_total} ({overall_passed/overall_total*100:.1f}%)")
