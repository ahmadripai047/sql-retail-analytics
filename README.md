# SQL Analytics Case Study — Online Retail

[Live Dashboard!](https://sql-retail-analytics.streamlit.app/)

> **"Bagaimana pola revenue, customer behaviour, dan product performance di platform e-commerce selama 12 bulan?"**

![Python](https://img.shields.io/badge/Python-3.10+-3776ab?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQL-SQLite-003B57?logo=sqlite&logoColor=white)
![Jupyter](https://img.shields.io/badge/Notebook-Jupyter-F37626?logo=jupyter&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)

---

## Business Problem

Retailer e-commerce UK dengan 5.878 pelanggan aktif di 41 negara ingin memahami:

1. Negara dan produk mana yang paling menguntungkan?
2. Bagaimana pola frekuensi pembelian pelanggan?
3. Siapa pelanggan paling bernilai dan mana yang berisiko churn?
4. Apakah ada pola musiman dalam revenue?

---

## Dataset

- **Sumber:** Online Retail UCI — transaksi 12 bulan (Des 2010 – Des 2011)
- **Volume:** 805.549 transaksi · 36.969 invoice · 5.878 pelanggan · 4.631 produk · 41 negara
- **Kolom utama:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`, `Revenue`
- **Tools:** Python + SQLite — semua analisis menggunakan SQL murni

---

## SQL Concepts Covered

| Konsep | Contoh Penggunaan |
|---|---|
| `GROUP BY` + `HAVING` | Filter produk dengan penjualan konsisten ≥8 bulan |
| Window Function — `RANK()` | Ranking produk terlaris per negara |
| Window Function — `NTILE()` | RFM scoring segmentasi pelanggan |
| Window Function — `LAG()` | Month-over-Month growth calculation |
| Window Function — Running Total | Cumulative revenue trend |
| CTE (Common Table Expression) | Multi-step RFM scoring pipeline |
| `JOIN` | Cohort analysis (first purchase vs return) |
| `CASE WHEN` | Frequency segmentation & Pareto grouping |

---

## Analisis (15 Query)

### Section 1 — Data Overview
- **Q1:** Dataset overview & statistik dasar
- **Q2:** Revenue breakdown per negara

### Section 2 — Product Performance
- **Q3:** Top 10 produk by total revenue
- **Q4:** Best-selling product per negara (`RANK` window function)
- **Q5:** Evergreen products — konsisten laku ≥8 bulan (CTE + HAVING)

### Section 3 — Customer Behaviour
- **Q6:** Top customers by lifetime value
- **Q7:** Purchase frequency distribution & segmentation
- **Q8:** Average Order Value (AOV) per negara

### Section 4 — Time-Based Analysis
- **Q9:** Monthly revenue & active customer trend
- **Q10:** Month-over-Month growth (`LAG` window function)

### Section 5 — RFM Segmentation
- **Q11:** RFM scoring per pelanggan (`NTILE` window function)
- **Q12:** Distribusi segmen RFM + avg monetary per segmen

### Section 6 — Advanced Analysis
- **Q13:** Cohort retention rate by acquisition month (`JOIN` + CTE)
- **Q14:** Cumulative revenue running total
- **Q15:** Pareto 80/20 analysis — produk yang hasilkan 80% revenue

---

## Key Findings

| Temuan | Business Implication |
|---|---|
| UK menghasilkan >70% total revenue | Diversifikasi ke Jerman & Prancis untuk mitigasi risiko konsentrasi |
| Mayoritas pelanggan beli hanya 1–3x | Re-engagement campaign adalah prioritas utama |
| Korelasi kuat antara frekuensi & monetary | Tingkatkan repeat purchase untuk naikan CLV |
| Sebagian besar pelanggan masuk segmen "At Risk" | Win-back campaign dengan penawaran personal |
| Sedikit produk hasilkan 80% revenue (Pareto) | Pastikan top SKU tidak pernah stockout |

---

## Setup Lokal

Dataset otomatis didownload saat pertama kali membuka Streamlit app.
Untuk menjalankan secara lokal:

```bash
# Clone repo
git clone https://github.com/ahmadripai047/sql-retail-analytics.git
cd sql-retail-analytics

# Install dependencies
pip install -r requirements.txt

# Download dataset dari Kaggle
# https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci
# Rename menjadi online_retail.csv, letakkan di folder ini

# Buat database
python setup_db.py

# Buka notebook
jupyter notebook sql_case_study.ipynb

# Atau jalankan dashboard
streamlit run app.py
```

```
sql-retail-analytics/
├── app.py                 ← Streamlit dashboard
├── sql_case_study.ipynb   ← Notebook utama (15 SQL queries + visualisasi)
├── setup_db.py            ← Script generate database SQLite
├── requirements.txt       ← Python dependencies
└── README.md

```
---

## 👤 Author

**Muhammad Rifai, S.Stat**
- GitHub: [@ahmadripai047](https://github.com/ahmadripai047)
- LinkedIn: [in/muhammad-rifai047](https://linkedin.com/in/muhammad-rifai047)

---

*Portfolio | Analytifai | Dataset: Online Retail UCI*