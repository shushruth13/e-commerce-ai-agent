import sqlite3
import pandas as pd
import os

# Paths
DB_PATH = 'focus_data.db'
DATASET_DIR = 'Dataset'

# CSV files and their table names
csv_table_map = {
    'Product-Level Total Sales and Metrics (mapped) - Product-Level Total Sales and Metrics (mapped).csv': 'total_sales_metrics',
    'Product-Level Ad Sales and Metrics (mapped) - Product-Level Ad Sales and Metrics (mapped).csv': 'ad_sales_metrics',
    'Product-Level Eligibility Table (mapped) - Product-Level Eligibility Table (mapped).csv': 'eligibility_table',
}

def create_tables(conn):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS total_sales_metrics (
            date TEXT,
            item_id INTEGER,
            total_sales REAL,
            total_units_ordered INTEGER
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ad_sales_metrics (
            date TEXT,
            item_id INTEGER,
            ad_sales REAL,
            impressions INTEGER,
            ad_spend REAL,
            clicks INTEGER,
            units_sold INTEGER
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS eligibility_table (
            eligibility_datetime_utc TEXT,
            item_id INTEGER,
            eligibility TEXT,
            message TEXT
        )
    ''')
    conn.commit()

def import_csv_to_table(conn, csv_path, table_name):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Imported {csv_path} into {table_name}")

def main():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    for csv_file, table_name in csv_table_map.items():
        csv_path = os.path.join(DATASET_DIR, csv_file)
        import_csv_to_table(conn, csv_path, table_name)
    conn.close()
    print(f"Database setup complete: {DB_PATH}")

if __name__ == '__main__':
    main() 