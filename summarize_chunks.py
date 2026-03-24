#!/usr/bin/env python3
import json

with open('test_100cvs_results.json','r') as f:
    data = json.load(f)

results = data.get('results', [])
# Group by chunk of 20 based on numeric ID
chunks = {i: [] for i in range(1,6)}
for r in results:
    cid = r['id']  # like TC001
    num = int(cid[2:])
    chunk_idx = (num-1)//20 + 1
    if 1 <= chunk_idx <= 5:
        chunks[chunk_idx].append(r)

print("Per-chunk results (from previous run):")
for i in range(1,6):
    cases = chunks[i]
    passed = sum(1 for c in cases if c['match'])
    total = len(cases)
    pct = passed/total*100 if total else 0
    print(f"Chunk {i}: {passed}/{total} ({pct:.1f}%)")

overall_passed = sum(1 for r in results if r['match'])
overall_total = len(results)
print(f"\nOVERALL: {overall_passed}/{overall_total} ({overall_passed/overall_total*100:.1f}%)")
