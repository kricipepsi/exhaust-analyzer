import json
with open('diagnostic_suite_results.json','r') as f:
    data = json.load(f)
print("Keys:", list(data.keys()))
if 'failures' in data:
    fails = data['failures']
    print(f"Number of failures: {len(fails)}")
    if fails:
        print("Sample failures:")
        for f in fails[:5]:
            print(f)
else:
    print("No 'failures' key found")
