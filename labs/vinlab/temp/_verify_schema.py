import os
import sqlite3

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
conn = sqlite3.connect('vinlab/data/vref.db')
cols = {r[1] for r in conn.execute('PRAGMA table_info(engine_ref)')}
assert 'has_maf' in cols and 'has_map' in cols, f"Missing columns: {cols}"
maf = conn.execute("SELECT COUNT(*) FROM engine_ref WHERE has_maf=1").fetchone()[0]
mp  = conn.execute("SELECT COUNT(*) FROM engine_ref WHERE has_map=1").fetchone()[0]
print(f'has_maf=1: {maf}  has_map=1: {mp}')
assert maf > 0 and mp > 0, "MAF or MAP count is zero"
conn.close()
print('Schema + count check: OK')
