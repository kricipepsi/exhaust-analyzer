import io
import json
import os

import mysql.connector

conn = mysql.connector.connect(
    host=os.environ.get('TECDOC_HOST','127.0.0.1'),
    port=int(os.environ.get('TECDOC_PORT','3306')),
    user=os.environ.get('TECDOC_USER','root'),
    password=os.environ.get('TECDOC_PASS',''),
    database=os.environ.get('TECDOC_DB','tecdoc'),
    connection_timeout=10)
cur = conn.cursor()
result = {}

# Hypothesis: passanger_car_prd.id references models.id (not passanger_cars.id)
# Check if prd.id values match models.id values

# 1. Get a few prd.id values with mixture prep
cur.execute("""
    SELECT DISTINCT pcp.id FROM passanger_car_prd pcp
    WHERE pcp.assemblygroupdescription = 'Приготовление смеси'
    LIMIT 10
""")
prd_ids = [r[0] for r in cur.fetchall()]
result['prd_ids'] = prd_ids

# 2. Check if these IDs exist in models table
for pid in prd_ids:
    cur.execute("SELECT id, description, manufacturerid FROM models WHERE id = %s", (pid,))
    row = cur.fetchone()
    result[f'model_{pid}'] = str(row) if row else None

# 3. Check: for a few petrol cars, get their modelid and see if prd has matching entries
cur.execute("""
    SELECT pc.id as car_id, pc.modelid, pc.description
    FROM passanger_cars pc
    WHERE pc.id IN (
        SELECT DISTINCT pca.passangercarid FROM passanger_car_attributes pca
        WHERE pca.displaytitle = 'Fuel type' AND pca.displayvalue = 'бензин'
    )
    LIMIT 10
""")
cars = [(r[0], r[1], r[2]) for r in cur.fetchall()]
result['sample_cars'] = [{'car_id': c[0], 'modelid': c[1], 'desc': c[2]} for c in cars]

# For each car's modelid, check prd
for car in cars:
    car_id, model_id, desc = car
    cur.execute("SELECT COUNT(*) FROM passanger_car_prd WHERE id = %s", (model_id,))
    prd_cnt = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passanger_car_prd WHERE id = %s AND assemblygroupdescription = 'Приготовление смеси'", (model_id,))
    mixture_cnt = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passanger_car_prd WHERE id = %s AND description = 'Датчик, давление наддува'", (model_id,))
    map_cnt = cur.fetchone()[0]
    result[f'car_{car_id}_model_{model_id}'] = {'prd_rows': prd_cnt, 'mixture_rows': mixture_cnt, 'map_rows': map_cnt}

# 4. Also check: passanger_car_engines.id vs passanger_cars.id
cur.execute("""
    SELECT pce.id as eng_table_id, pc.id as car_id
    FROM passanger_car_engines pce
    JOIN passanger_cars pc ON pce.id = pc.id
    WHERE pce.id IN (119512, 28251, 58731)
""")
result['eng_id_matches_car_id'] = [tuple(r) for r in cur.fetchall()]

# 5. What does passanger_car_engines.id actually match?
cur.execute("SELECT id FROM passanger_car_engines LIMIT 5")
result['pce_sample_ids'] = [r[0] for r in cur.fetchall()]

# 6. Get max id from each relevant table
for tbl in ['passanger_cars', 'models', 'passanger_car_engines', 'passanger_car_prd']:
    cur.execute(f"SELECT MAX(id) FROM {tbl}")
    result[f'{tbl}_max_id'] = cur.fetchone()[0]

cur.close()
conn.close()

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_prd_model.json')
with io.open(path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("OK:", path)
