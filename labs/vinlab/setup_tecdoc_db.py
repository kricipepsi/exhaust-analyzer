"""Create tecdoc tables and load CSV data. One-shot setup."""
import csv
from pathlib import Path

import mysql.connector

CSV_DIR = Path("E:/TecDoc/csv")
DB_CONFIG = {
    "host": "127.0.0.1", "port": 3306, "user": "root",
    "password": "", "database": "tecdoc", "allow_local_infile": True,
    "charset": "utf8mb4",
}

TABLES = {
    "manufacturers": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "id INT", "canbedisplayed VARCHAR(10)",
        "description VARCHAR(255)", "fulldescription VARCHAR(512)", "haslink VARCHAR(10)",
        "isaxle VARCHAR(10)", "iscommercialvehicle VARCHAR(10)", "isengine VARCHAR(10)",
        "ismotorbike VARCHAR(10)", "ispassengercar VARCHAR(10)", "istransporter VARCHAR(10)",
        "isvgl VARCHAR(10)", "matchcode VARCHAR(255)",
    ],
    "models": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "id INT", "canbedisplayed VARCHAR(10)",
        "constructioninterval VARCHAR(255)", "description VARCHAR(255)",
        "fulldescription VARCHAR(512)", "haslink VARCHAR(10)", "isaxle VARCHAR(10)",
        "iscommercialvehicle VARCHAR(10)", "isengine VARCHAR(10)", "ismotorbike VARCHAR(10)",
        "ispassengercar VARCHAR(10)", "istransporter VARCHAR(10)", "manufacturerid INT",
    ],
    "engines": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "id INT", "canbedisplayed VARCHAR(10)",
        "constructioninterval VARCHAR(255)", "description VARCHAR(255)",
        "fulldescription VARCHAR(512)", "haslink VARCHAR(10)", "haslinkitem VARCHAR(10)",
        "isaxle VARCHAR(10)", "iscommercialvehicle VARCHAR(10)", "iscvmanufacturerid VARCHAR(10)",
        "isengine VARCHAR(10)", "ismotorbike VARCHAR(10)", "ispassengercar VARCHAR(10)",
        "istransporter VARCHAR(10)", "manufacturerid INT", "salesdescription TEXT",
    ],
    "passanger_cars": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "id INT", "canbedisplayed VARCHAR(10)",
        "constructioninterval VARCHAR(255)", "description VARCHAR(255)",
        "fulldescription VARCHAR(512)", "haslink VARCHAR(10)", "isaxle VARCHAR(10)",
        "iscommercialvehicle VARCHAR(10)", "iscvmanufacturerid VARCHAR(10)",
        "isengine VARCHAR(10)", "ismotorbike VARCHAR(10)", "ispassengercar VARCHAR(10)",
        "istransporter VARCHAR(10)", "modelid INT",
    ],
    "passanger_car_attributes": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "passangercarid INT",
        "attributegroup VARCHAR(255)", "attributetype VARCHAR(255)",
        "displaytitle VARCHAR(255)", "displayvalue TEXT",
    ],
    "engine_attributes": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "engineid INT",
        "attributegroup VARCHAR(255)", "attributetype VARCHAR(255)",
        "displaytitle VARCHAR(255)", "displayvalue TEXT",
    ],
    "passanger_car_engines": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "id INT", "engineid INT",
    ],
    "prd": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "id INT",
        "assemblygroupdescription TEXT", "description TEXT",
        "normalizeddescription TEXT", "usagedescription TEXT",
    ],
    "passanger_car_prd": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "id INT",
        "assemblygroupdescription TEXT", "description TEXT",
        "normalizeddescription TEXT", "usagedescription TEXT",
    ],
    "engine_prd": [
        "row_id INT AUTO_INCREMENT PRIMARY KEY", "id INT",
        "assemblygroupdescription TEXT", "description TEXT",
        "normalizeddescription TEXT", "usagedescription TEXT",
    ],
}


def create_tables(cursor):
    for table_name, columns in TABLES.items():
        col_def = ", ".join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({col_def}) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
        cursor.execute(sql)
        print(f"  Created table: {table_name}")


def load_table(cursor, table_name, total_columns):
    """total_columns includes row_id auto-increment. CSV has total_columns-1 cols."""
    csv_path = CSV_DIR / f"{table_name}.csv"
    if not csv_path.exists():
        print(f"  SKIP: {csv_path} not found")
        return 0

    cursor.execute(f"TRUNCATE TABLE `{table_name}`")
    data_columns = total_columns - 1  # exclude row_id
    placeholders = ", ".join(["%s"] * total_columns)
    sql = f"INSERT INTO `{table_name}` VALUES ({placeholders})"

    count = 0
    batch = []
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) < data_columns:
                row.extend([None] * (data_columns - len(row)))
            batch.append(tuple([None] + list(row[:data_columns])))
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

    print("Creating tables...")
    for t in TABLES:
        col_def = ", ".join(TABLES[t])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS `{t}` ({col_def}) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")

    print("\nLoading data...")
    total = 0
    for table_name in TABLES:
        cols = [c for c in TABLES[table_name]]
        try:
            rows = load_table(cursor, table_name, len(cols))
            conn.commit()
            total += rows
        except Exception as e:
            print(f"  ERROR loading {table_name}: {e}")
            conn.rollback()
            raise

    conn.close()
    print(f"\nTotal rows loaded: {total}")


if __name__ == "__main__":
    main()
