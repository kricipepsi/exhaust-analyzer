"""
dump_schema.py — run once on Windows to expose TecDoc schema to Claude.
Usage:  python dump_schema.py
Output: tecdoc_schema.json  (table list + columns + 3 sample rows each)
"""

import json

import mysql.connector

MYSQL_HOST     = "127.0.0.1"
MYSQL_PORT     = 3306
MYSQL_USER     = "root"
MYSQL_PASSWORD = ""          # fill in if you have a password
MYSQL_DATABASE = "tecdoc"

SAMPLE_ROWS = 3   # rows to dump per table as preview

def main():
    conn = mysql.connector.connect(
        host=MYSQL_HOST, port=MYSQL_PORT,
        user=MYSQL_USER, password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    cur = conn.cursor()

    # All tables
    cur.execute("SHOW TABLES")
    tables = [row[0] for row in cur.fetchall()]
    print(f"Found {len(tables)} tables.")

    result = {}
    for table in tables:
        # Columns
        cur.execute(f"DESCRIBE `{table}`")
        cols = [{"Field": r[0], "Type": r[1], "Null": r[2], "Key": r[3]} for r in cur.fetchall()]

        # Row count
        cur.execute(f"SELECT COUNT(*) FROM `{table}`")
        row_count = cur.fetchone()[0]

        # Sample rows
        col_names = [c["Field"] for c in cols]
        cur.execute(f"SELECT * FROM `{table}` LIMIT {SAMPLE_ROWS}")
        rows = []
        for row in cur.fetchall():
            rows.append({col_names[i]: str(row[i]) if row[i] is not None else None
                         for i in range(len(col_names))})

        result[table] = {
            "row_count": row_count,
            "columns": cols,
            "sample_rows": rows
        }
        print(f"  {table}: {row_count} rows, {len(cols)} columns")

    cur.close()
    conn.close()

    out = "tecdoc_schema.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nDone. Schema written to {out}")

if __name__ == "__main__":
    main()
