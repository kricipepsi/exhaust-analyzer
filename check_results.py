#!/usr/bin/env python3
from pathlib import Path
import json, os
p = Path('petrol_test_run_results.json')
if p.exists():
    print("File exists, size:", p.stat().st_size)
    data = json.loads(p.read_text())
    print("Keys:", data.keys())
    print("Overall:", data.get('overall'))
else:
    print("File does not exist in current directory")
    print("Current dir:", Path.cwd())
    print("Contents:", os.listdir('.')[:20])