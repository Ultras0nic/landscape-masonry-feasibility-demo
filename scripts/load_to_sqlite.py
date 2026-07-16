"""Load generated CSVs into the enforced SQLite schema."""

from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
DB_PATH = BASE_DIR / "landscape_masonry_demo.db"
SCHEMA_PATH = BASE_DIR / "sql" / "create_tables.sql"

TABLES = {
    "jobs": DATA_DIR / "jobs.csv",
    "material_prices": DATA_DIR / "material_prices.csv",
    "labor_rates": DATA_DIR / "labor_rates.csv",
    "production_rates": DATA_DIR / "production_rates.csv",
    "job_feasibility_summary": OUTPUT_DIR / "job_feasibility_summary.csv",
    "actual_job_results": DATA_DIR / "actual_job_results.csv",
    "preconstruction_action_log": OUTPUT_DIR / "preconstruction_action_log.csv",
}


def main() -> None:
    missing = [str(path) for path in TABLES.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing pipeline inputs: {missing}")

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        for table_name, file_path in TABLES.items():
            frame = pd.read_csv(file_path)
            frame.to_sql(table_name, connection, if_exists="append", index=False)
            print(f"Loaded {len(frame):>3} rows into {table_name}.")

        foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
        if foreign_key_errors:
            raise ValueError(f"Foreign key validation failed: {foreign_key_errors}")

    print(f"Database created with enforced schema: {DB_PATH}")


if __name__ == "__main__":
    main()
