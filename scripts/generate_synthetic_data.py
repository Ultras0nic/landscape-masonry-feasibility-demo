from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# -----------------------------
# State-level assumptions
# These can be updated later for MA vs RI market differences.
# -----------------------------

material_prices = pd.DataFrame([
    # Massachusetts
    ["MA", "pavers", "sqft", 8.50],
    ["MA", "base_gravel", "cubic_yard", 62.00],
    ["MA", "bedding_sand", "cubic_yard", 54.00],
    ["MA", "edging", "linear_ft", 4.25],
    ["MA", "disposal", "cubic_yard", 48.00],
    ["MA", "equipment_day", "day", 185.00],

    # Rhode Island
    ["RI", "pavers", "sqft", 8.00],
    ["RI", "base_gravel", "cubic_yard", 58.00],
    ["RI", "bedding_sand", "cubic_yard", 50.00],
    ["RI", "edging", "linear_ft", 4.00],
    ["RI", "disposal", "cubic_yard", 44.00],
    ["RI", "equipment_day", "day", 170.00],
], columns=["state", "material_type", "unit", "unit_cost"])

labor_rates = pd.DataFrame([
    ["MA", 42.00],
    ["RI", 38.00],
], columns=["state", "labor_cost_per_hour"])

production_rates = pd.DataFrame([
    ["Paver Patio", 10.0],
    ["Walkway", 8.0],
    ["Small Retaining Wall", 5.5],
], columns=["job_type", "sqft_per_labor_hour"])

cities = {
    "MA": ["Weymouth", "Quincy", "Braintree", "Boston", "Newton", "Framingham", "Worcester"],
    "RI": ["Providence", "Warwick", "Cranston", "Pawtucket", "Newport"]
}

job_types = ["Paver Patio", "Walkway", "Small Retaining Wall"]
slope_levels = ["Low", "Medium", "High"]

jobs = []

for i in range(1, 61):
    state = np.random.choice(["MA", "RI"], p=[0.7, 0.3])
    city = np.random.choice(cities[state])
    job_type = np.random.choice(job_types, p=[0.6, 0.25, 0.15])

    if job_type == "Paver Patio":
        area_sqft = np.random.randint(180, 750)
    elif job_type == "Walkway":
        area_sqft = np.random.randint(80, 350)
    else:
        area_sqft = np.random.randint(120, 500)

    perimeter_ft = round(np.sqrt(area_sqft) * 4 * np.random.uniform(0.85, 1.20), 1)

    base_depth_in = np.random.choice([4, 6, 8], p=[0.35, 0.50, 0.15])
    sand_depth_in = 1

    slope_level = np.random.choice(slope_levels, p=[0.55, 0.32, 0.13])
    access_width_ft = round(np.random.uniform(3.0, 10.0), 1)
    drainage_concern = np.random.choice(["Yes", "No"], p=[0.28, 0.72])
    demo_required = np.random.choice(["Yes", "No"], p=[0.35, 0.65])
    carry_distance_ft = np.random.randint(10, 140)
    crew_size = np.random.choice([2, 3, 4], p=[0.30, 0.50, 0.20])
    target_margin_pct = 0.25

    # Rough quote generation, intentionally imperfect.
    state_price_factor = 1.08 if state == "MA" else 1.00
    job_type_factor = {
        "Paver Patio": 24,
        "Walkway": 28,
        "Small Retaining Wall": 36
    }[job_type]

    difficulty_factor = 1.0
    if slope_level == "Medium":
        difficulty_factor += 0.10
    elif slope_level == "High":
        difficulty_factor += 0.22

    if drainage_concern == "Yes":
        difficulty_factor += 0.10
    if demo_required == "Yes":
        difficulty_factor += 0.08
    if access_width_ft < 5:
        difficulty_factor += 0.08

    quoted_price = round(area_sqft * job_type_factor * state_price_factor * difficulty_factor * np.random.uniform(0.92, 1.12), 2)

    jobs.append([
        f"J{i:03d}",
        state,
        city,
        job_type,
        area_sqft,
        perimeter_ft,
        base_depth_in,
        sand_depth_in,
        slope_level,
        access_width_ft,
        drainage_concern,
        demo_required,
        carry_distance_ft,
        crew_size,
        quoted_price,
        target_margin_pct
    ])

jobs_df = pd.DataFrame(jobs, columns=[
    "job_id",
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
    "target_margin_pct"
])

material_prices.to_csv(DATA_DIR / "material_prices.csv", index=False)
labor_rates.to_csv(DATA_DIR / "labor_rates.csv", index=False)
production_rates.to_csv(DATA_DIR / "production_rates.csv", index=False)
jobs_df.to_csv(DATA_DIR / "jobs.csv", index=False)

print("Synthetic landscape/masonry job data created in data/")