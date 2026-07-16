"""Generate a reproducible, synthetic flatwork estimating scenario.

The assumptions are illustrative portfolio inputs, not market benchmarks.
"""

from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
SCENARIO_DATE = pd.Timestamp("2026-07-15")
ASSUMPTION_VERSION = "2026-07-demo-v2"

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def main() -> None:
    rng = np.random.default_rng(SEED)

    assumption_note = "Illustrative synthetic assumption; not a vendor quote"
    material_prices = pd.DataFrame(
        [
            ["MA", "pavers", "sqft", 8.50],
            ["MA", "base_gravel", "cubic_yard", 62.00],
            ["MA", "bedding_sand", "cubic_yard", 54.00],
            ["MA", "edging", "linear_ft", 4.25],
            ["MA", "disposal", "cubic_yard", 48.00],
            ["MA", "equipment_day", "day", 185.00],
            ["RI", "pavers", "sqft", 8.00],
            ["RI", "base_gravel", "cubic_yard", 58.00],
            ["RI", "bedding_sand", "cubic_yard", 50.00],
            ["RI", "edging", "linear_ft", 4.00],
            ["RI", "disposal", "cubic_yard", 44.00],
            ["RI", "equipment_day", "day", 170.00],
        ],
        columns=["state", "material_type", "unit", "unit_cost"],
    )
    material_prices["effective_date"] = SCENARIO_DATE.date().isoformat()
    material_prices["assumption_version"] = ASSUMPTION_VERSION
    material_prices["source_note"] = assumption_note

    labor_rates = pd.DataFrame(
        [["MA", 42.00], ["RI", 38.00]],
        columns=["state", "labor_cost_per_hour"],
    )
    labor_rates["effective_date"] = SCENARIO_DATE.date().isoformat()
    labor_rates["assumption_version"] = ASSUMPTION_VERSION
    labor_rates["source_note"] = assumption_note

    # The MVP is intentionally limited to paver flatwork. Retaining walls require
    # wall-specific geometry, drainage, reinforcement, and engineering review.
    production_rates = pd.DataFrame(
        [["Paver Patio", 10.0], ["Walkway", 8.0]],
        columns=["job_type", "sqft_per_labor_hour"],
    )
    production_rates["effective_date"] = SCENARIO_DATE.date().isoformat()
    production_rates["assumption_version"] = ASSUMPTION_VERSION
    production_rates["source_note"] = assumption_note

    cities = {
        "MA": ["Weymouth", "Quincy", "Braintree", "Boston", "Newton", "Framingham", "Worcester"],
        "RI": ["Providence", "Warwick", "Cranston", "Pawtucket", "Newport"],
    }
    rows = []

    for i in range(1, 61):
        state = rng.choice(["MA", "RI"], p=[0.7, 0.3])
        city = rng.choice(cities[state])
        job_type = rng.choice(["Paver Patio", "Walkway"], p=[0.72, 0.28])
        area_sqft = int(rng.integers(180, 751) if job_type == "Paver Patio" else rng.integers(80, 351))
        perimeter_ft = round(np.sqrt(area_sqft) * 4 * rng.uniform(0.85, 1.20), 1)
        base_depth_in = int(rng.choice([4, 6, 8], p=[0.35, 0.50, 0.15]))
        slope_level = rng.choice(["Low", "Medium", "High"], p=[0.55, 0.32, 0.13])
        access_width_ft = round(float(rng.uniform(3.0, 10.0)), 1)
        drainage_concern = rng.choice(["Yes", "No"], p=[0.28, 0.72])
        demo_required = rng.choice(["Yes", "No"], p=[0.35, 0.65])
        carry_distance_ft = int(rng.integers(10, 140))
        crew_size = int(rng.choice([2, 3, 4], p=[0.30, 0.50, 0.20]))
        planned_start = SCENARIO_DATE + pd.Timedelta(days=int(rng.integers(1, 22)))

        state_price_factor = 1.08 if state == "MA" else 1.00
        unit_quote = 24 if job_type == "Paver Patio" else 28
        difficulty_factor = 1.0
        difficulty_factor += {"Low": 0.0, "Medium": 0.10, "High": 0.22}[slope_level]
        difficulty_factor += 0.10 if drainage_concern == "Yes" else 0.0
        difficulty_factor += 0.08 if demo_required == "Yes" else 0.0
        difficulty_factor += 0.08 if access_width_ft < 5 else 0.0

        # Wider quote noise deliberately creates under-target and healthy-margin
        # scenarios so every commercial review branch is exercised.
        quote_factor = float(rng.uniform(0.76, 1.12))
        if i % 10 == 0:
            quote_factor = 0.72
        quoted_price = round(area_sqft * unit_quote * state_price_factor * difficulty_factor * quote_factor, 2)

        rows.append(
            [
                f"J{i:03d}",
                f"{job_type} {i:03d}",
                state,
                city,
                job_type,
                area_sqft,
                perimeter_ft,
                base_depth_in,
                1,
                slope_level,
                access_width_ft,
                drainage_concern,
                demo_required,
                carry_distance_ft,
                crew_size,
                quoted_price,
                0.25,
                "Preconstruction",
                SCENARIO_DATE.date().isoformat(),
                planned_start.date().isoformat(),
                rng.choice(["Yes", "No"], p=[0.86, 0.14]),
                rng.choice(["Yes", "No"], p=[0.82, 0.18]),
                rng.choice(["Confirmed", "Pending", "Not Required"], p=[0.52, 0.18, 0.30]),
                rng.choice(["Approved", "Pending", "Not Required"], p=[0.38, 0.12, 0.50]),
                rng.choice(["Confirmed", "Pending"], p=[0.78, 0.22]),
                rng.choice(["Yes", "No"], p=[0.84, 0.16]),
                ASSUMPTION_VERSION,
            ]
        )

    jobs = pd.DataFrame(
        rows,
        columns=[
            "job_id",
            "job_name",
            "state",
            "city",
            "job_type",
            "area_sqft",
            "perimeter_ft",
            "base_depth_in",
            "sand_depth_in",
            "slope_level",
            "access_width_ft",
            "drainage_concern",
            "demo_required",
            "carry_distance_ft",
            "crew_size",
            "quoted_price",
            "target_margin_pct",
            "project_phase",
            "scenario_date",
            "planned_start_date",
            "scope_approved",
            "site_access_verified",
            "utility_locate_status",
            "permit_status",
            "materials_status",
            "crew_assigned",
            "assumption_version",
        ],
    )

    material_prices.to_csv(DATA_DIR / "material_prices.csv", index=False)
    labor_rates.to_csv(DATA_DIR / "labor_rates.csv", index=False)
    production_rates.to_csv(DATA_DIR / "production_rates.csv", index=False)
    jobs.to_csv(DATA_DIR / "jobs.csv", index=False)
    print(f"Created {len(jobs)} synthetic flatwork jobs with seed {SEED}.")


if __name__ == "__main__":
    main()
