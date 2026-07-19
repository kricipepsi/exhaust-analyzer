"""Load TecDoc CSV data into MySQL for VINLab."""
import csv
from pathlib import Path

import mysql.connector

CSV_DIR = Path("E:/TecDoc/csv")
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "tecdoc",
    "allow_local_infile": True,
    "charset": "utf8mb4",
}

TABLES = {
    "manufacturers": [
        "id", "canbedisplayed", "description", "fulldescription", "haslink",
        "isaxle", "iscommercialvehicle", "isengine", "ismotorbike",
        "ispassengercar", "istransporter", "isvgl", "matchcode",
    ],
    "models": [
        "id", "canbedisplayed", "constructioninterval", "description",
        "fulldescription", "haslink", "isaxle", "iscommercialvehicle",
        "isengine", "ismotorbike", "ispassengercar", "istransporter",
        "manufacturerid",
    ],
    "engines": [
        "id", "canbedisplayed", "constructioninterval", "description",
        "fulldescription", "haslink", "haslinkitem", "isaxle",
        "iscommercialvehicle", "iscvmanufacturerid", "isengine",
        "ismotorbike", "ispassengercar", "istransporter",
        "manufacturerid", "salesdescription",
    ],
    "passanger_cars": [
        "id", "canbedisplayed", "constructioninterval", "description",
        "fulldescription", "haslink", "isaxle", "iscommercialvehicle",
        "iscvmanufacturerid", "isengine", "ismotorbike",
        "ispassengercar", "istransporter", "modelid",
    ],
    "passanger_car_attributes": [
        "passangercarid", "attributegroup", "attributetype",
        "displaytitle", "displayvalue",
    ],
    "engine_attributes": [
        "engineid", "attributegroup", "attributetype",
        "displaytitle", "displayvalue",
    ],
    "passanger_car_engines": [
        "id", "engineid",
    ],
    "prd": [
        "id", "assemblygroupdescription", "description",
        "normalizeddescription", "usagedescription",
    ],
    "passanger_car_prd": [
        "id", "assemblygroupdescription", "description",
        "normalizeddescription", "usagedescription",
    ],
    "engine_prd": [
        "id", "assemblygroupdescription", "description",
        "normalizeddescription", "usagedescription",
    ],
}


def load_table(cursor, table_name, columns):
    csv_path = CSV_DIR / f"{table_name}.csv"
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return 0

    # Truncate first
    cursor.execute(f"TRUNCATE TABLE `{table_name}`")

    placeholders = ", ".join(["%s"] * len(columns))
    col_names = ", ".join(f"`{c}`" for c in columns)
    sql = f"INSERT INTO `{table_name}` ({col_names}) VALUES ({placeholders})"

    count = 0
    batch = []
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            # Pad or truncate row to match column count
            if len(row) < len(columns):
                row.extend([None] * (len(columns) - len(row)))
            batch.append(tuple(row[:len(columns)]))
            count += 1
            if len(batch) >= 5000:
                cursor.executemany(sql, batch)
                batch = []
                print(f"  {table_name}: {count} rows...", end="\r")

    if batch:
        cursor.executemany(sql, batch)

    print(f"  {table_name}: {count} rows loaded.   ")
    return count


def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    total = 0
    for table_name, columns in TABLES.items():
        print(f"Loading {table_name}...")
        try:
            rows = load_table(cursor, table_name, columns)
            conn.commit()
            total += rows
        except Exception as e:
            print(f"  ERROR loading {table_name}: {e}")
            conn.rollback()

    conn.close()
    print(f"\nTotal rows loaded: {total}")


if __name__ == "__main__":
    main()
