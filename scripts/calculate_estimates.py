"""Create pre-job estimates and a separate synthetic closeout dataset."""

from pathlib import Path

import numpy as np
import pandas as pd


SEED = 99
RISK_MODEL_VERSION = "rules-v2-illustrative"

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def lookup(df: pd.DataFrame, filters: dict[str, object], value: str) -> float:
    matches = df.copy()
    for column, expected in filters.items():
        matches = matches[matches[column] == expected]
    if len(matches) != 1:
        raise ValueError(f"Expected one {value} row for {filters}, found {len(matches)}")
    return float(matches[value].iloc[0])


def risk_components(row: pd.Series) -> list[tuple[str, int]]:
    components: list[tuple[str, int]] = []
    if row["access_width_ft"] < 4:
        components.append(("Very narrow site access", 25))
    elif row["access_width_ft"] < 6:
        components.append(("Narrow site access", 15))
    if row["slope_level"] == "Medium":
        components.append(("Medium slope", 12))
    elif row["slope_level"] == "High":
        components.append(("High slope", 25))
    if row["drainage_concern"] == "Yes":
        components.append(("Drainage concern", 20))
    if row["demo_required"] == "Yes":
        components.append(("Demolition required", 12))
    if row["carry_distance_ft"] > 100:
        components.append(("Very long material carry", 18))
    elif row["carry_distance_ft"] > 60:
        components.append(("Long material carry", 10))
    if row["area_sqft"] > 600:
        components.append(("Large job footprint", 10))
    if row["crew_size"] < 3 and row["area_sqft"] > 350:
        components.append(("Small crew for job size", 10))
    return components


def risk_category(score: int) -> str:
    if score <= 30:
        return "Low Risk"
    if score <= 60:
        return "Needs Review"
    return "High Risk"


def workability_status(score: int, estimated_margin_pct: float) -> str:
    if score >= 80 or estimated_margin_pct < 0.08:
        return "Site Review Required"
    if score >= 60 or estimated_margin_pct < 0.18:
        return "Review Before Approval"
    return "No Additional Review Flagged"


def main() -> None:
    rng = np.random.default_rng(SEED)
    jobs = pd.read_csv(DATA_DIR / "jobs.csv")
    material_prices = pd.read_csv(DATA_DIR / "material_prices.csv")
    labor_rates = pd.read_csv(DATA_DIR / "labor_rates.csv")
    production_rates = pd.read_csv(DATA_DIR / "production_rates.csv")

    unsupported = set(jobs["job_type"]) - {"Paver Patio", "Walkway"}
    if unsupported:
        raise ValueError(f"Unsupported job types for flatwork estimator: {sorted(unsupported)}")

    estimate_records: list[dict[str, object]] = []
    actual_records: list[dict[str, object]] = []

    for _, row in jobs.iterrows():
        state = row["state"]
        area = float(row["area_sqft"])
        perimeter = float(row["perimeter_ft"])

        price = lambda material: lookup(
            material_prices,
            {"state": state, "material_type": material},
            "unit_cost",
        )
        labor_rate = lookup(labor_rates, {"state": state}, "labor_cost_per_hour")
        production_rate = lookup(
            production_rates,
            {"job_type": row["job_type"]},
            "sqft_per_labor_hour",
        )

        paver_sqft = area * 1.08
        gravel_cy = area * (float(row["base_depth_in"]) / 12) / 27 * 1.10
        sand_cy = area * (float(row["sand_depth_in"]) / 12) / 27 * 1.10
        edging_lf = perimeter * 1.05
        material_cost = (
            paver_sqft * price("pavers")
            + gravel_cy * price("base_gravel")
            + sand_cy * price("bedding_sand")
            + edging_lf * price("edging")
        )
        if row["demo_required"] == "Yes":
            material_cost += area * 0.10 / 27 * price("disposal")

        labor_modifier = 1.0
        labor_modifier += {"Low": 0.0, "Medium": 0.12, "High": 0.25}[row["slope_level"]]
        labor_modifier += 0.22 if row["access_width_ft"] < 4 else 0.12 if row["access_width_ft"] < 6 else 0.0
        labor_modifier += 0.18 if row["drainage_concern"] == "Yes" else 0.0
        labor_modifier += 0.15 if row["demo_required"] == "Yes" else 0.0
        labor_modifier += 0.20 if row["carry_distance_ft"] > 100 else 0.10 if row["carry_distance_ft"] > 60 else 0.0

        estimated_labor_hours = round(area / production_rate * labor_modifier, 2)
        estimated_labor_cost = round(estimated_labor_hours * labor_rate, 2)
        estimated_duration_days = round(estimated_labor_hours / (int(row["crew_size"]) * 8), 2)
        equipment_days = max(1, int(np.ceil(estimated_duration_days)))
        equipment_cost = round(equipment_days * price("equipment_day"), 2)
        material_cost = round(material_cost, 2)
        estimated_total_cost = round(material_cost + estimated_labor_cost + equipment_cost, 2)
        quoted_price = float(row["quoted_price"])
        estimated_margin_pct = round((quoted_price - estimated_total_cost) / quoted_price, 3)
        margin_gap_pct = round(estimated_margin_pct - float(row["target_margin_pct"]), 3)

        components = risk_components(row)
        site_risk_points = sum(weight for _, weight in components)
        risk_drivers = " | ".join(name for name, _ in components) or "No scored site risk"
        risk_component_detail = " | ".join(f"{name}={weight}" for name, weight in components) or "No scored site risk=0"
        category = risk_category(site_risk_points)
        status = workability_status(site_risk_points, estimated_margin_pct)

        estimate_records.append(
            {
                "job_id": row["job_id"],
                "job_name": row["job_name"],
                "state": state,
                "city": row["city"],
                "job_type": row["job_type"],
                "project_phase": row["project_phase"],
                "scenario_date": row["scenario_date"],
                "planned_start_date": row["planned_start_date"],
                "area_sqft": area,
                "quoted_price": quoted_price,
                "estimated_material_cost": material_cost,
                "estimated_labor_hours": estimated_labor_hours,
                "estimated_labor_cost": estimated_labor_cost,
                "estimated_equipment_cost": equipment_cost,
                "estimated_total_cost": estimated_total_cost,
                "estimated_margin_pct": estimated_margin_pct,
                "target_margin_pct": float(row["target_margin_pct"]),
                "margin_gap_pct": margin_gap_pct,
                "meets_target_margin": "Yes" if margin_gap_pct >= 0 else "No",
                "estimated_duration_days": estimated_duration_days,
                "site_risk_points": site_risk_points,
                "risk_category": category,
                "risk_drivers": risk_drivers,
                "risk_component_detail": risk_component_detail,
                "risk_model_version": RISK_MODEL_VERSION,
                "workability_status": status,
                "slope_level": row["slope_level"],
                "access_width_ft": float(row["access_width_ft"]),
                "drainage_concern": row["drainage_concern"],
                "demo_required": row["demo_required"],
                "carry_distance_ft": int(row["carry_distance_ft"]),
                "crew_size": int(row["crew_size"]),
                "scope_approved": row["scope_approved"],
                "site_access_verified": row["site_access_verified"],
                "utility_locate_status": row["utility_locate_status"],
                "permit_status": row["permit_status"],
                "materials_status": row["materials_status"],
                "crew_assigned": row["crew_assigned"],
                "assumption_version": row["assumption_version"],
            }
        )

        # These are deliberately simulated closeout outcomes. Separate labor,
        # material, and change-event mechanisms avoid treating every variance as
        # the same phenomenon. They remain scenario logic, not learned effects.
        labor_multiplier = float(rng.normal(1.00, 0.08))
        labor_multiplier += 0.10 if row["access_width_ft"] < 6 else 0.0
        labor_multiplier += 0.10 if row["slope_level"] == "High" else 0.0
        labor_multiplier += 0.08 if row["carry_distance_ft"] > 100 else 0.0
        material_multiplier = float(rng.normal(1.00, 0.04))
        material_multiplier += 0.05 if row["demo_required"] == "Yes" else 0.0

        change_probability = 0.05
        change_probability += 0.18 if row["drainage_concern"] == "Yes" else 0.0
        change_probability += 0.12 if row["demo_required"] == "Yes" else 0.0
        change_probability += 0.08 if row["site_access_verified"] == "No" else 0.0
        change_order_flag = "Yes" if rng.random() < min(change_probability, 0.65) else "No"
        change_order_cost = (
            round(estimated_total_cost * float(rng.uniform(0.03, 0.12)), 2)
            if change_order_flag == "Yes"
            else 0.0
        )

        actual_labor_hours = round(estimated_labor_hours * max(labor_multiplier, 0.70), 2)
        actual_total_cost = round(
            material_cost * max(material_multiplier, 0.80)
            + estimated_labor_cost * max(labor_multiplier, 0.70)
            + equipment_cost * max(labor_multiplier, 1.0)
            + change_order_cost,
            2,
        )
        actual_margin_pct = round((quoted_price - actual_total_cost) / quoted_price, 3)
        actual_records.append(
            {
                "job_id": row["job_id"],
                "actual_labor_hours": actual_labor_hours,
                "actual_total_cost": actual_total_cost,
                "actual_margin_pct": actual_margin_pct,
                "cost_variance": round(actual_total_cost - estimated_total_cost, 2),
                "margin_variance": round(actual_margin_pct - estimated_margin_pct, 3),
                "change_order_flag": change_order_flag,
                "change_order_cost": change_order_cost,
                "outcome_note": "Synthetic closeout scenario",
            }
        )

    summary = pd.DataFrame(estimate_records)
    actuals = pd.DataFrame(actual_records)
    closeout = summary.merge(actuals, on="job_id", how="inner", validate="one_to_one")
    closeout["analysis_stage"] = "Post-job learning"

    summary.to_csv(OUTPUT_DIR / "job_feasibility_summary.csv", index=False)
    actuals.to_csv(DATA_DIR / "actual_job_results.csv", index=False)
    closeout.to_csv(OUTPUT_DIR / "tableau_job_feasibility_summary.csv", index=False)
    closeout.to_csv(OUTPUT_DIR / "post_job_variance_review.csv", index=False)
    print(f"Created estimates and separate synthetic closeout results for {len(summary)} jobs.")


if __name__ == "__main__":
    main()
