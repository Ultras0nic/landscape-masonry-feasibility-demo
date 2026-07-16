"""Run the complete reproducible demo pipeline."""

from pathlib import Path
import subprocess
import sys


BASE_DIR = Path(__file__).resolve().parents[1]
STEPS = [
    "generate_synthetic_data.py",
    "calculate_estimates.py",
    "create_action_queue.py",
    "load_to_sqlite.py",
    "run_sql_queries.py",
    "validate_outputs.py",
]


def main() -> None:
    for step in STEPS:
        print(f"\n=== {step} ===")
        subprocess.run([sys.executable, str(BASE_DIR / "scripts" / step)], check=True, cwd=BASE_DIR)
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
