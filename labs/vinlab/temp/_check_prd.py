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

# 1. Find distinct assembly groups
cur.execute("""
    SELECT assemblygroupdescription, COUNT(*) as cnt
    FROM passanger_car_prd
    WHERE assemblygroupdescription LIKE '%иготовлен%'
       OR assemblygroupdescription LIKE '%меси%'
       OR assemblygroupdescription LIKE '%оздух%'
       OR assemblygroupdescription LIKE '%давлен%'
       OR assemblygroupdescription LIKE '%агнета%'
       OR assemblygroupdescription LIKE '%ециркул%'
    GROUP BY assemblygroupdescription
    ORDER BY cnt DESC
""")
result['assembly_groups'] = [(r[0], r[1]) for r in cur.fetchall()]

# 2. All distinct assemblygroupdescription values (first 100)
cur.execute("""
    SELECT assemblygroupdescription, COUNT(*) as cnt
    FROM passanger_car_prd
    GROUP BY assemblygroupdescription
    ORDER BY cnt DESC
    LIMIT 100
""")
result['all_groups_top100'] = [(r[0], r[1]) for r in cur.fetchall()]

# 3. Check prd table for product IDs related to pressure sensors
cur.execute("""
    SELECT id, assemblygroupdescription, description, normalizeddescription
    FROM prd
    WHERE normalizeddescription LIKE '%давлен%'
       OR description LIKE '%давлен%'
       OR normalizeddescription LIKE '%pressure%'
       OR description LIKE '%pressure%'
       OR normalizeddescription LIKE '%MAP%'
       OR description LIKE '%MAP%'
       OR normalizeddescription LIKE '%MAF%'
       OR description LIKE '%MAF%'
       OR assemblygroupdescription LIKE '%давлен%'
       OR assemblygroupdescription LIKE '%оздух%'
    LIMIT 30
""")
result['prd_pressure'] = [(r[0], r[1], r[2], r[3]) for r in cur.fetchall()]

# 4. Check prd for mixture-related
cur.execute("""
    SELECT id, assemblygroupdescription, description, normalizeddescription
    FROM prd
    WHERE assemblygroupdescription LIKE '%иготовлен%'
       OR assemblygroupdescription LIKE '%меси%'
       OR normalizeddescription LIKE '%смеси%'
       OR description LIKE '%смеси%'
    LIMIT 30
""")
result['prd_mixture'] = [(r[0], r[1], r[2], r[3]) for r in cur.fetchall()]

# 5. Sample passanger_car_prd for a petrol car
cur.execute("""
    SELECT pcp.id, pcp.assemblygroupdescription, pcp.description,
           pcp.normalizeddescription, pcp.usagedescription
    FROM passanger_car_prd pcp
    WHERE pcp.id IN (
        SELECT DISTINCT pca.passangercarid FROM passanger_car_attributes pca
        WHERE pca.displaytitle = 'Fuel type' AND pca.displayvalue = 'бензин'
    )
    LIMIT 20
""")
result['sample_car_prd'] = [(r[0], r[1], r[2], r[3], r[4]) for r in cur.fetchall()]

# 6. Search for terms in passanger_car_prd text fields
terms_check = {}
for term in ['MAP', 'MAF', 'давлен', 'воздух', 'смеси', 'boost', 'pressure', 'manifold', 'air mass', 'air flow', 'наддув', 'расходомер']:
    cur.execute(f"""
        SELECT COUNT(*), COUNT(DISTINCT id) FROM passanger_car_prd
        WHERE normalizeddescription LIKE '%{term}%'
           OR description LIKE '%{term}%'
           OR usagedescription LIKE '%{term}%'
           OR assemblygroupdescription LIKE '%{term}%'
    """)
    cnt, cars = cur.fetchone()
    if cnt > 0:
        terms_check[term] = {"rows": cnt, "unique_cars": cars}

result['term_search'] = terms_check

cur.close()
conn.close()

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_prd_result.json')
with io.open(path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print("OK:", path)
