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

# Get petrol cars that have mixture prep parts (via modelid)
cur.execute("""
    SELECT pc.id as car_id, pca.displayvalue as fuel_type,
           pc.modelid, m.description as model_name,
           pcp.assemblygroupdescription, pcp.description
    FROM passanger_car_attributes pca
    JOIN passanger_cars pc ON pca.passangercarid = pc.id
    JOIN passanger_car_prd pcp ON pc.modelid = pcp.id
    JOIN models m ON pc.modelid = m.id
    WHERE pca.displaytitle = 'Fuel type'
      AND pca.displayvalue = 'бензин'
      AND pcp.assemblygroupdescription = 'Приготовление смеси'
    LIMIT 10
""")
result = {'maf_cars': []}
for r in cur.fetchall():
    result['maf_cars'].append({'car_id': r[0], 'fuel': r[1], 'modelid': r[2],
                                'model': r[3], 'ag': r[4], 'desc': r[5]})

# Same for MAP (boost pressure sensor)
cur.execute("""
    SELECT pc.id as car_id, pca.displayvalue as fuel_type,
           pc.modelid, m.description as model_name,
           pcp.assemblygroupdescription, pcp.description
    FROM passanger_car_attributes pca
    JOIN passanger_cars pc ON pca.passangercarid = pc.id
    JOIN passanger_car_prd pcp ON pc.modelid = pcp.id
    JOIN models m ON pc.modelid = m.id
    WHERE pca.displaytitle = 'Fuel type'
      AND pca.displayvalue = 'бензин'
      AND pcp.description = 'Датчик, давление наддува'
    LIMIT 10
""")
result['map_cars'] = []
for r in cur.fetchall():
    result['map_cars'].append({'car_id': r[0], 'fuel': r[1], 'modelid': r[2],
                                'model': r[3], 'ag': r[4], 'desc': r[5]})

# Now check: for the MAF cars, get their engine linkage and confirm the pipeline
if result['maf_cars']:
    first_car = result['maf_cars'][0]['car_id']
    first_model = result['maf_cars'][0]['modelid']
    cur.execute("""
        SELECT pce.id, pce.engineid, e.description, m.description
        FROM passanger_car_engines pce
        JOIN engines e ON pce.engineid = e.id
        JOIN manufacturers m ON e.manufacturerid = m.id
        WHERE pce.id = %s
    """, (first_car,))
    result['first_maf_car_engine'] = [{'car_id': r[0], 'engine_id': r[1],
                                        'engine_desc': r[2], 'brand': r[3]} for r in cur.fetchall()]

    # Verify PRD lookup by modelid
    cur.execute("""
        SELECT COUNT(*) FROM passanger_car_prd
        WHERE id = %s AND assemblygroupdescription = 'Приготовление смеси'
    """, (first_model,))
    result['model_prd_mixture_count'] = cur.fetchone()[0]

# Count: how many unique petrol engine/model pairs have MAF?
cur.execute("""
    SELECT COUNT(DISTINCT pce.engineid)
    FROM passanger_car_engines pce
    JOIN passanger_cars pc ON pce.id = pc.id
    JOIN passanger_car_attributes pca ON pc.id = pca.passangercarid
    JOIN passanger_car_prd pcp ON pc.modelid = pcp.id
    WHERE pca.displaytitle = 'Fuel type'
      AND pca.displayvalue = 'бензин'
      AND pcp.assemblygroupdescription = 'Приготовление смеси'
""")
result['unique_engines_with_maf'] = cur.fetchone()[0]

cur.execute("""
    SELECT COUNT(DISTINCT pce.engineid)
    FROM passanger_car_engines pce
    JOIN passanger_cars pc ON pce.id = pc.id
    JOIN passanger_car_attributes pca ON pc.id = pca.passangercarid
    JOIN passanger_car_prd pcp ON pc.modelid = pcp.id
    WHERE pca.displaytitle = 'Fuel type'
      AND pca.displayvalue = 'бензин'
      AND pcp.description = 'Датчик, давление наддува'
""")
result['unique_engines_with_map'] = cur.fetchone()[0]

cur.close()
conn.close()

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_maf_map.json')
with io.open(path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("OK:", path)
