import io
import json
import os

import mysql.connector

try:
    conn = mysql.connector.connect(
        host=os.environ.get('TECDOC_HOST','127.0.0.1'),
        port=int(os.environ.get('TECDOC_PORT','3306')),
        user=os.environ.get('TECDOC_USER','root'),
        password=os.environ.get('TECDOC_PASS',''),
        database=os.environ.get('TECDOC_DB','tecdoc'),
        connection_timeout=10)
    cur = conn.cursor()
    tables = ['passanger_car_engines', 'passanger_car_prd', 'prd',
              'passanger_cars', 'engines', 'engine_prd']
    result = {}
    for tbl in tables:
        cur.execute(f"SHOW COLUMNS FROM {tbl}")
        cols = [{"field": r[0], "type": r[1]} for r in cur.fetchall()]
        result[tbl] = cols
    cur.close()
    conn.close()
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_schema_result.json')
    with io.open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("OK:", path)
except Exception:
    import traceback
    traceback.print_exc()
