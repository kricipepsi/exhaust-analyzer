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

# 1. Check overlap: how many petrol car IDs from passanger_car_attributes
#    have matching entries in passanger_car_prd?
cur.execute("""
    SELECT COUNT(DISTINCT pca.passangercarid)
    FROM passanger_car_attributes pca
    WHERE pca.displaytitle = 'Fuel type'
      AND pca.displayvalue = 'бензин'
""")
petrol_count = cur.fetchone()[0]
result['petrol_cars'] = petrol_count

cur.execute("""
    SELECT COUNT(DISTINCT id) FROM passanger_car_prd
""")
prd_car_count = cur.fetchone()[0]
result['prd_cars'] = prd_car_count

# How many petrol cars have entries in passanger_car_prd?
cur.execute("""
    SELECT COUNT(DISTINCT pca.passangercarid)
    FROM passanger_car_attributes pca
    JOIN passanger_car_prd pcp ON pca.passangercarid = pcp.id
    WHERE pca.displaytitle = 'Fuel type'
      AND pca.displayvalue = 'бензин'
""")
overlap = cur.fetchone()[0]
result['petrol_cars_with_prd'] = overlap

# 2. How many have mixture prep in passanger_car_prd?
cur.execute("""
    SELECT COUNT(DISTINCT pca.passangercarid)
    FROM passanger_car_attributes pca
    JOIN passanger_car_prd pcp ON pca.passangercarid = pcp.id
    WHERE pca.displaytitle = 'Fuel type'
      AND pca.displayvalue = 'бензин'
      AND pcp.assemblygroupdescription = 'Приготовление смеси'
""")
mixture = cur.fetchone()[0]
result['petrol_cars_with_mixture_prep'] = mixture

# 3. How many have boost pressure sensor?
cur.execute("""
    SELECT COUNT(DISTINCT pca.passangercarid)
    FROM passanger_car_attributes pca
    JOIN passanger_car_prd pcp ON pca.passangercarid = pcp.id
    WHERE pca.displaytitle = 'Fuel type'
      AND pca.displayvalue = 'бензин'
      AND pcp.description = 'Датчик, давление наддува'
""")
map_count = cur.fetchone()[0]
result['petrol_cars_with_map_sensor'] = map_count

# 4. Check: do passanger_car_engines.id values match passanger_car_prd.id values?
# Take a few car IDs from engines and check if they exist in prd
cur.execute("""
    SELECT pce.id, pce.engineid
    FROM passanger_car_engines pce
    WHERE pce.id IN (
        SELECT DISTINCT pca.passangercarid FROM passanger_car_attributes pca
        WHERE pca.displaytitle = 'Fuel type' AND pca.displayvalue = 'бензин'
    )
    LIMIT 10
""")
engine_car_ids = [(r[0], r[1]) for r in cur.fetchall()]
result['sample_engine_car_ids'] = engine_car_ids

# Check if those car IDs exist in passanger_car_prd
for car_id, engine_id in engine_car_ids:
    cur.execute("SELECT COUNT(*) FROM passanger_car_prd WHERE id = %s", (car_id,))
    prd_cnt = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passanger_car_prd WHERE id = %s AND assemblygroupdescription = 'Приготовление смеси'", (car_id,))
    mixture_cnt = cur.fetchone()[0]
    result[f'car_{car_id}'] = {'prd_rows': prd_cnt, 'mixture_rows': mixture_cnt}

# 5. Check distinct passanger_car_prd.id types - are they the same as passanger_car_attributes.passangercarid?
cur.execute("""
    SELECT pcp.id, COUNT(*) as cnt
    FROM passanger_car_prd pcp
    WHERE pcp.assemblygroupdescription = 'Приготовление смеси'
    GROUP BY pcp.id
    LIMIT 10
""")
mixture_car_ids = [(r[0], r[1]) for r in cur.fetchall()]
result['cars_with_mixture_prep'] = mixture_car_ids

cur.close()
conn.close()

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_prd_match.json')
with io.open(path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("OK:", path)
