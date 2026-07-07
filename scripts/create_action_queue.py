from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"

summary_path = OUTPUT_DIR / "tableau_job_feasibility_summary.csv"
output_path = OUTPUT_DIR / "jobsite_action_queue.csv"

df = pd.read_csv(summary_path)

def get_primary_risk_reason(row):
    reasons = []

    if row["access_width_ft"] < 6:
        reasons.append("Narrow site access")
    if row["drainage_concern"] == "Yes":
        reasons.append("Drainage concern")
    if row["demo_required"] == "Yes":
        reasons.append("Demolition required")
    if row["carry_distance_ft"] > 60:
        reasons.append("Long material carry distance")
    if row["slope_level"] in ["Medium", "High"]:
        reasons.append("Slope / grading difficulty")
    if row["estimated_margin_pct"] < row["target_margin_pct"]:
        reasons.append("Below target margin")
    if row["cost_variance"] > 0:
        reasons.append("Actual cost overrun risk")

    if len(reasons) == 0:
        return "No major risk flagged"

    return "; ".join(reasons[:2])


def get_recommended_action(row):
    if row["workability_status"] == "Requires Site Review":
        return "Schedule site review before approval"
    if row["estimated_margin_pct"] < 0.10:
        return "Review quote and scope assumptions"
    if row["drainage_concern"] == "Yes":
        return "Confirm drainage plan before scheduling"
    if row["access_width_ft"] < 6:
        return "Confirm equipment access and material staging"
    if row["carry_distance_ft"] > 60:
        return "Review labor hours for material movement"
    if row["demo_required"] == "Yes":
        return "Confirm demolition scope and disposal needs"
    if row["cost_variance"] > 0:
        return "Compare estimate assumptions with actual cost"
    return "Proceed with standard review"


def get_priority(row):
    if row["workability_status"] == "Requires Site Review":
        return "High"
    if row["risk_score"] >= 60:
        return "High"
    if row["estimated_margin_pct"] < row["target_margin_pct"]:
        return "Medium"
    if row["workability_status"] == "Review Before Approval":
        return "Medium"
    return "Low"


def get_owner_role(row):
    if row["workability_status"] == "Requires Site Review":
        return "Work Lead / Project Manager"
    if row["estimated_margin_pct"] < row["target_margin_pct"]:
        return "Estimator / Office Team"
    if row["drainage_concern"] == "Yes":
        return "Work Lead"
    if row["cost_variance"] > 0:
        return "Operations Analyst"
    return "Project Team"


action_queue = df.copy()

action_queue["primary_risk_reason"] = action_queue.apply(get_primary_risk_reason, axis=1)
action_queue["recommended_action"] = action_queue.apply(get_recommended_action, axis=1)
action_queue["priority"] = action_queue.apply(get_priority, axis=1)
action_queue["owner_role"] = action_queue.apply(get_owner_role, axis=1)
action_queue["field_notes_required"] = action_queue["priority"].apply(
    lambda x: "Yes" if x in ["High", "Medium"] else "No"
)

action_queue = action_queue[
    [
        "job_id",
        "state",
        "city",
        "job_type",
        "workability_status",
        "risk_score",
        "risk_category",
        "estimated_margin_pct",
        "actual_margin_pct",
        "cost_variance",
        "primary_risk_reason",
        "recommended_action",
        "priority",
        "owner_role",
        "field_notes_required",
    ]
]

action_queue = action_queue.sort_values(
    by=["priority", "risk_score"],
    ascending=[True, False]
)

priority_order = {"High": 1, "Medium": 2, "Low": 3}
action_queue["priority_order"] = action_queue["priority"].map(priority_order)
action_queue = action_queue.sort_values(
    by=["priority_order", "risk_score"],
    ascending=[True, False]
).drop(columns=["priority_order"])

action_queue.to_csv(output_path, index=False)

print(f"Jobsite action queue created: {output_path}")