"""Run inner-loop checks on modified files."""
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

files = ['tools/build_vref_db.py', 'vinlab/decoder.py']
ok = True

for f in files:
    # 1. py_compile
    r = subprocess.run([sys.executable, '-m', 'py_compile', f], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL py_compile {f}: {r.stderr}")
        ok = False
    else:
        print(f"PASS py_compile {f}")

    # 2. ruff check
    r = subprocess.run(['ruff', 'check', f, '--fix'], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL ruff {f}: {r.stdout[-200:]}")
        ok = False
    else:
        print(f"PASS ruff {f}")

    # 3. pyright
    r = subprocess.run(['pyright', f], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"NOTE pyright {f}: {r.stdout[-200:]}")
    else:
        print(f"PASS pyright {f}")

if ok:
    print("\nInner loop: ALL PASS")
else:
    print("\nInner loop: FAILURES")
    sys.exit(1)
