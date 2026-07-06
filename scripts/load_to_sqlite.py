from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
DB_PATH = BASE_DIR / "landscape_masonry_demo.db"

tables = {
    "jobs": DATA_DIR / "jobs.csv",
    "material_prices": DATA_DIR / "material_prices.csv",
    "labor_rates": DATA_DIR / "labor_rates.csv",
    "production_rates": DATA_DIR / "production_rates.csv",
    "actual_job_results": DATA_DIR / "actual_job_results.csv",
    "job_feasibility_summary": OUTPUT_DIR / "job_feasibility_summary.csv",
}

conn = sqlite3.connect(DB_PATH)

for table_name, file_path in tables.items():
    df = pd.read_csv(file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {file_path.name} into table: {table_name}")

conn.close()

print(f"\nDatabase created: {DB_PATH}")