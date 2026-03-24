import json
kb = json.load(open('data/expanded_knowledge_base.json'))
names = [c['name'] for c in kb['diagnostic_matrix']]
print("Number of cases:", len(names))
print("Case names:")
for n in names:
    print(f"  {n}")
