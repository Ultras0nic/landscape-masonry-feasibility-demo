"""Run the documented SQL analysis and fail if any query fails."""

from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "landscape_masonry_demo.db"
SQL_PATH = BASE_DIR / "sql" / "analysis_queries.sql"
OUTPUT_DIR = BASE_DIR / "outputs" / "query_results"

QUERY_NAMES = [
    "jobs_requiring_review",
    "lowest_estimated_margins",
    "state_summary",
    "job_type_summary",
    "estimate_vs_actual",
    "cost_overruns",
    "risk_factor_counts",
    "review_status_counts",
    "below_target_margin",
    "tableau_state_job_type",
    "preconstruction_action_log",
    "post_job_learning",
]


def main() -> None:
    if not DB_PATH.exists() or not SQL_PATH.exists():
        raise FileNotFoundError("Run the pipeline through load_to_sqlite.py first.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for stale_file in OUTPUT_DIR.glob("*.csv"):
        stale_file.unlink()

    lines = [line for line in SQL_PATH.read_text(encoding="utf-8").splitlines() if not line.strip().startswith("--")]
    queries = [query.strip() for query in "\n".join(lines).split(";") if query.strip()]
    if len(queries) != len(QUERY_NAMES):
        raise ValueError(f"Expected {len(QUERY_NAMES)} queries, found {len(queries)}")

    with sqlite3.connect(DB_PATH) as connection:
        for index, (name, query) in enumerate(zip(QUERY_NAMES, queries), start=1):
            frame = pd.read_sql_query(query, connection)
            output_file = OUTPUT_DIR / f"{index:02d}_{name}.csv"
            frame.to_csv(output_file, index=False)
            print(f"Saved {len(frame):>3} rows to {output_file.name}.")


if __name__ == "__main__":
    main()
