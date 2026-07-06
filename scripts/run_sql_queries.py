from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "landscape_masonry_demo.db"
SQL_PATH = BASE_DIR / "sql" / "analysis_queries.sql"
OUTPUT_DIR = BASE_DIR / "outputs" / "query_results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Using database: {DB_PATH}")
print(f"Using SQL file: {SQL_PATH}")

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

if not SQL_PATH.exists():
    raise FileNotFoundError(f"SQL file not found: {SQL_PATH}")

conn = sqlite3.connect(DB_PATH)

sql_text = SQL_PATH.read_text(encoding="utf-8")

clean_lines = []
for line in sql_text.splitlines():
    if not line.strip().startswith("--"):
        clean_lines.append(line)

clean_sql = "\n".join(clean_lines)
queries = [q.strip() for q in clean_sql.split(";") if q.strip()]

print(f"Found {len(queries)} SQL queries.")

for i, query in enumerate(queries, start=1):
    try:
        df = pd.read_sql_query(query, conn)
        output_file = OUTPUT_DIR / f"query_{i:02d}.csv"
        df.to_csv(output_file, index=False)

        print(f"\nQuery {i} result:")
        print(df.head(10))
        print(f"Saved to: {output_file}")

    except Exception as e:
        print(f"\nQuery {i} failed.")
        print(query)
        print(f"Error: {e}")

conn.close()
print("\nDone.")