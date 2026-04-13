"""
setup_db.py — Generate SQLite database dari online_retail.csv
Jalankan sekali sebelum membuka notebook.
"""

import sqlite3
import pandas as pd
import os

CSV_FILE = "online_retail.csv"
DB_FILE  = "retail.db"

def main():
    if not os.path.exists(CSV_FILE):
        print(f"ERROR: File '{CSV_FILE}' tidak ditemukan.")
        print("Download dataset dari: https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci")
        print("Atau gunakan file online_retail.csv yang sudah tersedia di repo ini.")
        return

    print("Membaca dataset...")
    df = pd.read_csv(CSV_FILE, encoding="ISO-8859-1")

    # Rename kolom agar sesuai query SQL
    df = df.rename(columns={
        'Price':       'UnitPrice',
        'Customer ID': 'CustomerID',
        'Invoice':     'InvoiceNo'
    })

    # Cleaning dasar
    df = df.dropna(subset=["CustomerID"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]
    df["CustomerID"] = df["CustomerID"].astype(int)
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    print(f"Dataset: {len(df):,} rows, {df['CustomerID'].nunique()} customers")

    # Load ke SQLite
    print("Membuat database SQLite...")
    conn = sqlite3.connect(DB_FILE)
    df.to_sql("transactions", conn, if_exists="replace", index=False)

    # Buat view customer_summary
    conn.execute("""
    CREATE VIEW IF NOT EXISTS customer_summary AS
    SELECT
        CustomerID,
        Country,
        COUNT(DISTINCT InvoiceNo)             AS total_orders,
        SUM(Quantity)                         AS total_qty,
        ROUND(SUM(Revenue), 2)                AS total_revenue,
        ROUND(AVG(Revenue), 2)                AS avg_order_value,
        MIN(InvoiceDate)                      AS first_purchase,
        MAX(InvoiceDate)                      AS last_purchase
    FROM transactions
    GROUP BY CustomerID, Country
    """)
    conn.commit()
    conn.close()

    print(f"Database '{DB_FILE}' siap digunakan.")
    print("   Buka sql_case_study.ipynb untuk mulai analisis.")

if __name__ == "__main__":
    main()
