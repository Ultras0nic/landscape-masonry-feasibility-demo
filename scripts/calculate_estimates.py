from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(99)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

jobs = pd.read_csv(DATA_DIR / "jobs.csv")
material_prices = pd.read_csv(DATA_DIR / "material_prices.csv")
labor_rates = pd.read_csv(DATA_DIR / "labor_rates.csv")
production_rates = pd.read_csv(DATA_DIR / "production_rates.csv")


def get_material_price(state, material_type):
    row = material_prices[
        (material_prices["state"] == state) &
        (material_prices["material_type"] == material_type)
    ]
    return float(row["unit_cost"].iloc[0])


def get_labor_rate(state):
    row = labor_rates[labor_rates["state"] == state]
    return float(row["labor_cost_per_hour"].iloc[0])


def get_production_rate(job_type):
    row = production_rates[production_rates["job_type"] == job_type]
    return float(row["sqft_per_labor_hour"].iloc[0])


def calculate_risk_score(row):
    risk = 0

    if row["access_width_ft"] < 4:
        risk += 25
    elif row["access_width_ft"] < 6:
        risk += 15

    if row["slope_level"] == "Medium":
        risk += 12
    elif row["slope_level"] == "High":
        risk += 25

    if row["drainage_concern"] == "Yes":
        risk += 20

    if row["demo_required"] == "Yes":
        risk += 12

    if row["carry_distance_ft"] > 100:
        risk += 18
    elif row["carry_distance_ft"] > 60:
        risk += 10

    if row["area_sqft"] > 600:
        risk += 10

    if row["crew_size"] < 3 and row["area_sqft"] > 350:
        risk += 10

    return risk


def risk_category(score):
    if score <= 30:
        return "Low Risk"
    elif score <= 60:
        return "Needs Review"
    else:
        return "High Risk"


def workability_status(risk_score, estimated_margin_pct):
    if risk_score >= 80 or estimated_margin_pct < 0.08:
        return "Requires Site Review"
    elif risk_score >= 60 or estimated_margin_pct < 0.18:
        return "Review Before Approval"
    else:
        return "Workable"


records = []
actual_records = []

for _, row in jobs.iterrows():
    state = row["state"]
    area = row["area_sqft"]
    perimeter = row["perimeter_ft"]

    paver_cost = get_material_price(state, "pavers")
    gravel_cost = get_material_price(state, "base_gravel")
    sand_cost = get_material_price(state, "bedding_sand")
    edging_cost = get_material_price(state, "edging")
    disposal_cost = get_material_price(state, "disposal")
    equipment_day_cost = get_material_price(state, "equipment_day")
    labor_rate = get_labor_rate(state)
    production_rate = get_production_rate(row["job_type"])

    # Material takeoff
    paver_sqft = area * 1.08
    gravel_cy = area * (row["base_depth_in"] / 12) / 27 * 1.10
    sand_cy = area * (row["sand_depth_in"] / 12) / 27 * 1.10
    edging_lf = perimeter * 1.05

    material_cost = (
        paver_sqft * paver_cost +
        gravel_cy * gravel_cost +
        sand_cy * sand_cost +
        edging_lf * edging_cost
    )

    if row["demo_required"] == "Yes":
        disposal_cy = area * 0.10 / 27
        material_cost += disposal_cy * disposal_cost

    # Labor modifier
    labor_modifier = 1.0

    if row["slope_level"] == "Medium":
        labor_modifier += 0.12
    elif row["slope_level"] == "High":
        labor_modifier += 0.25

    if row["access_width_ft"] < 4:
        labor_modifier += 0.22
    elif row["access_width_ft"] < 6:
        labor_modifier += 0.12

    if row["drainage_concern"] == "Yes":
        labor_modifier += 0.18

    if row["demo_required"] == "Yes":
        labor_modifier += 0.15

    if row["carry_distance_ft"] > 100:
        labor_modifier += 0.20
    elif row["carry_distance_ft"] > 60:
        labor_modifier += 0.10

    estimated_labor_hours = round((area / production_rate) * labor_modifier, 2)
    estimated_labor_cost = round(estimated_labor_hours * labor_rate, 2)

    estimated_duration_days = round(estimated_labor_hours / (row["crew_size"] * 8), 2)

    equipment_days = max(1, np.ceil(estimated_duration_days))
    equipment_cost = equipment_days * equipment_day_cost

    estimated_total_cost = round(material_cost + estimated_labor_cost + equipment_cost, 2)

    quoted_price = row["quoted_price"]
    estimated_margin_pct = round((quoted_price - estimated_total_cost) / quoted_price, 3)

    risk_score = calculate_risk_score(row)
    category = risk_category(risk_score)
    status = workability_status(risk_score, estimated_margin_pct)

    # Simulated actual results
    actual_cost_multiplier = np.random.normal(1.00, 0.08)

    if risk_score > 60:
        actual_cost_multiplier += np.random.uniform(0.05, 0.18)

    if row["drainage_concern"] == "Yes":
        actual_cost_multiplier += np.random.uniform(0.02, 0.10)

    if row["demo_required"] == "Yes":
        actual_cost_multiplier += np.random.uniform(0.02, 0.08)

    actual_total_cost = round(estimated_total_cost * actual_cost_multiplier, 2)
    actual_labor_hours = round(estimated_labor_hours * actual_cost_multiplier, 2)
    actual_margin_pct = round((quoted_price - actual_total_cost) / quoted_price, 3)
    cost_variance = round(actual_total_cost - estimated_total_cost, 2)
    margin_variance = round(actual_margin_pct - estimated_margin_pct, 3)

    change_order_flag = "Yes" if (risk_score > 60 and actual_cost_multiplier > 1.10) else "No"

    records.append([
        row["job_id"],
        state,
        row["city"],
        row["job_type"],
        area,
        row["quoted_price"],
        round(material_cost, 2),
        estimated_labor_hours,
        estimated_labor_cost,
        round(equipment_cost, 2),
        estimated_total_cost,
        estimated_margin_pct,
        estimated_duration_days,
        risk_score,
        category,
        status,
        row["slope_level"],
        row["access_width_ft"],
        row["drainage_concern"],
        row["demo_required"],
        row["carry_distance_ft"],
        row["crew_size"],
        row["target_margin_pct"]
    ])

    actual_records.append([
        row["job_id"],
        actual_labor_hours,
        actual_total_cost,
        actual_margin_pct,
        cost_variance,
        margin_variance,
        change_order_flag
    ])

summary = pd.DataFrame(records, columns=[
    "job_id",
    "state",
    "city",
    "job_type",
    "area_sqft",
    "quoted_price",
    "estimated_material_cost",
    "estimated_labor_hours",
    "estimated_labor_cost",
    "estimated_equipment_cost",
    "estimated_total_cost",
    "estimated_margin_pct",
    "estimated_duration_days",
    "risk_score",
    "risk_category",
    "workability_status",
    "slope_level",
    "access_width_ft",
    "drainage_concern",
    "demo_required",
    "carry_distance_ft",
    "crew_size",
    "target_margin_pct"
])

actuals = pd.DataFrame(actual_records, columns=[
    "job_id",
    "actual_labor_hours",
    "actual_total_cost",
    "actual_margin_pct",
    "cost_variance",
    "margin_variance",
    "change_order_flag"
])

summary.to_csv(OUTPUT_DIR / "job_feasibility_summary.csv", index=False)
actuals.to_csv(DATA_DIR / "actual_job_results.csv", index=False)

# Tableau-ready combined dataset
tableau_df = summary.merge(actuals, on="job_id", how="left")
tableau_df.to_csv(OUTPUT_DIR / "tableau_job_feasibility_summary.csv", index=False)

print("Estimate, risk, actual result, and Tableau-ready files created.")