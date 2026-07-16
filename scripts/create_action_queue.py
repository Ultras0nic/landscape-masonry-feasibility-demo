"""Build persona-specific preconstruction views without using post-job actuals."""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
SUMMARY_PATH = OUTPUT_DIR / "job_feasibility_summary.csv"
ACTION_LOG_PATH = OUTPUT_DIR / "preconstruction_action_log.csv"
ESTIMATOR_PATH = OUTPUT_DIR / "estimator_review.csv"


GATE_RULES = [
    ("scope_approved", "Yes", "SCOPE", "Scope is not approved", "Confirm approved scope before mobilization", "Estimator / Owner"),
    ("site_access_verified", "Yes", "ACCESS_GATE", "Site access and staging are not verified", "Verify access, staging, and equipment path", "Project Manager"),
    ("utility_locate_status", ("Confirmed", "Not Required"), "UTILITY", "Utility locate is pending", "Confirm utility locate before excavation", "Project Manager"),
    ("permit_status", ("Approved", "Not Required"), "PERMIT", "Permit or inspection status is pending", "Resolve permit and inspection requirement", "Operations Manager"),
    ("materials_status", "Confirmed", "MATERIAL", "Materials are not confirmed", "Confirm selection, availability, and delivery", "Estimator / Owner"),
    ("crew_assigned", "Yes", "CREW", "Crew is not assigned", "Assign crew and required equipment", "Operations Manager"),
]

RISK_ACTIONS = {
    "Very narrow site access": ("ACCESS_RISK", "Very narrow site access", "Confirm equipment path and material staging", "Foreman / Crew Lead", "High"),
    "Narrow site access": ("ACCESS_RISK", "Narrow site access", "Confirm equipment path and material staging", "Foreman / Crew Lead", "Low"),
    "Medium slope": ("SLOPE", "Medium slope may reduce productivity", "Review grade and labor allowance in the field plan", "Project Manager", "Low"),
    "High slope": ("SLOPE", "High slope requires additional review", "Complete site review before approval", "Project Manager", "High"),
    "Drainage concern": ("DRAINAGE", "Drainage concern is unresolved", "Confirm drainage approach before scheduling", "Project Manager", "High"),
    "Demolition required": ("DEMO", "Demolition scope must be confirmed", "Confirm demolition, disposal, and haul-off scope", "Estimator / Owner", "Low"),
    "Very long material carry": ("CARRY", "Very long material carry may affect labor", "Review labor and staging plan", "Foreman / Crew Lead", "High"),
    "Long material carry": ("CARRY", "Long material carry may affect labor", "Review labor and staging plan", "Foreman / Crew Lead", "Low"),
    "Large job footprint": ("SIZE", "Large job footprint needs production review", "Confirm crew, equipment, and duration assumptions", "Operations Manager", "Low"),
    "Small crew for job size": ("CREW_SIZE", "Crew may be small for the job size", "Review crew plan and production assumption", "Operations Manager", "High"),
}


def value_is_ready(value: object, ready: object) -> bool:
    return value in ready if isinstance(ready, tuple) else value == ready


def lookahead_bucket(days_to_start: int) -> str:
    if days_to_start <= 0:
        return "Due / Overdue"
    if days_to_start <= 7:
        return "Next 7 Days"
    return "Later"


def adjusted_priority(base: str, days_to_start: int, hard_gate: bool) -> str:
    if hard_gate and days_to_start <= 7:
        return "High"
    if base == "High":
        return "High"
    if days_to_start <= 7:
        return "Medium"
    return base


def main() -> None:
    summary = pd.read_csv(SUMMARY_PATH)
    actions: list[dict[str, object]] = []

    for _, row in summary.iterrows():
        scenario_date = pd.Timestamp(row["scenario_date"])
        planned_start = pd.Timestamp(row["planned_start_date"])
        needed_by = planned_start - pd.Timedelta(days=2)
        days_to_start = int((planned_start - scenario_date).days)
        job_actions: list[dict[str, object]] = []

        for field, ready, code, blocker, next_action, owner in GATE_RULES:
            if not value_is_ready(row[field], ready):
                job_actions.append(
                    {
                        "reason_code": code,
                        "constraint_category": "Readiness gate",
                        "blocker": blocker,
                        "next_action": next_action,
                        "responsible_role": owner,
                        "base_priority": "Medium",
                        "hard_gate": True,
                        "source_field": field,
                    }
                )

        if row["meets_target_margin"] == "No":
            job_actions.append(
                {
                    "reason_code": "MARGIN",
                    "constraint_category": "Commercial review",
                    "blocker": "Estimated margin is below target",
                    "next_action": "Review quote, scope, allowance, and cost assumptions",
                    "responsible_role": "Estimator / Owner",
                    "base_priority": "Medium" if row["estimated_margin_pct"] >= 0.10 else "High",
                    "hard_gate": False,
                    "source_field": "estimated_margin_pct",
                }
            )

        for driver in str(row["risk_drivers"]).split(" | "):
            if driver in RISK_ACTIONS:
                code, blocker, next_action, owner, base_priority = RISK_ACTIONS[driver]
                job_actions.append(
                    {
                        "reason_code": code,
                        "constraint_category": "Site constraint",
                        "blocker": blocker,
                        "next_action": next_action,
                        "responsible_role": owner,
                        "base_priority": base_priority,
                        "hard_gate": False,
                        "source_field": "risk_drivers",
                    }
                )

        for action_number, action in enumerate(job_actions, start=1):
            priority = adjusted_priority(action["base_priority"], days_to_start, action["hard_gate"])
            actions.append(
                {
                    "action_id": f"A-{row['job_id']}-{action_number:02d}",
                    "priority": priority,
                    "job_id": row["job_id"],
                    "job_name": row["job_name"],
                    "site": f"{row['city']}, {row['state']}",
                    "blocker": action["blocker"],
                    "next_action": action["next_action"],
                    "responsible_role": action["responsible_role"],
                    "assignee": "Unassigned",
                    "needed_by": needed_by.date().isoformat(),
                    "status": "Open",
                    "last_updated": scenario_date.date().isoformat(),
                    "lookahead_bucket": lookahead_bucket(int((needed_by - scenario_date).days)),
                    "escalation_flag": "Yes" if priority == "High" else "No",
                    "blocking_flag": "Yes" if action["hard_gate"] else "No",
                    "project_phase": row["project_phase"],
                    "planned_start_date": planned_start.date().isoformat(),
                    "constraint_category": action["constraint_category"],
                    "reason_code": action["reason_code"],
                    "source_field": action["source_field"],
                }
            )

    action_log = pd.DataFrame(actions)
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    action_log["_priority_order"] = action_log["priority"].map(priority_order)
    action_log = action_log.sort_values(
        ["_priority_order", "needed_by", "job_id", "action_id"]
    ).drop(columns="_priority_order")

    estimator_columns = [
        "job_id",
        "job_name",
        "state",
        "city",
        "job_type",
        "planned_start_date",
        "quoted_price",
        "estimated_material_cost",
        "estimated_labor_hours",
        "estimated_labor_cost",
        "estimated_equipment_cost",
        "estimated_total_cost",
        "estimated_margin_pct",
        "target_margin_pct",
        "margin_gap_pct",
        "meets_target_margin",
        "site_risk_points",
        "risk_category",
        "risk_drivers",
        "risk_component_detail",
        "workability_status",
        "assumption_version",
        "risk_model_version",
    ]
    estimator_review = summary[estimator_columns].sort_values(
        ["meets_target_margin", "site_risk_points", "estimated_margin_pct"],
        ascending=[True, False, True],
    )

    action_log.to_csv(ACTION_LOG_PATH, index=False)
    estimator_review.to_csv(ESTIMATOR_PATH, index=False)
    print(f"Created {len(action_log)} open constraints across {action_log['job_id'].nunique()} jobs.")
    print(f"Created estimator review for {len(estimator_review)} jobs.")


if __name__ == "__main__":
    main()
