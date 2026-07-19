import io
import json
import os
import sys

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

    cur.execute("SELECT displayvalue, COUNT(*) FROM passanger_car_attributes WHERE displaytitle = 'Fuel type' GROUP BY displayvalue ORDER BY COUNT(*) DESC LIMIT 30")
    rows = cur.fetchall()
    out = [{"val": r[0], "cnt": r[1]} for r in rows]

    cur.execute("SELECT displayvalue, COUNT(*) FROM passanger_car_attributes WHERE displaytitle = 'Engine type' GROUP BY displayvalue ORDER BY COUNT(*) DESC LIMIT 30")
    rows2 = cur.fetchall()
    out2 = [{"val": r[0], "cnt": r[1]} for r in rows2]

    cur.close()
    conn.close()

    result = {"fuel_type": out, "engine_type": out2}
    path = os.path.join(os.path.dirname(__file__), '_fueltype_result.json')
    with io.open(path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("OK: written to", path)
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    sys.exit(1)
