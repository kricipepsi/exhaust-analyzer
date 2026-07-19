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

# Check engine_attributes schema
cur.execute("SHOW COLUMNS FROM engine_attributes")
cols = [(r[0], r[1]) for r in cur.fetchall()]
print("engine_attributes columns:", cols)

# Sample
cur.execute("SELECT * FROM engine_attributes LIMIT 5")
for r in cur.fetchall():
    print("  ", r)

# Also check engines table sample for manufacturerid
cur.execute("SELECT id, manufacturerid, description FROM engines LIMIT 5")
for r in cur.fetchall():
    print("engine:", r)

cur.close()
conn.close()
