"""Validate the generated data contract and write a compact QA report."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
REPORT_PATH = OUTPUT_DIR / "validation_report.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    jobs = pd.read_csv(DATA_DIR / "jobs.csv")
    actuals = pd.read_csv(DATA_DIR / "actual_job_results.csv")
    summary = pd.read_csv(OUTPUT_DIR / "job_feasibility_summary.csv")
    actions = pd.read_csv(OUTPUT_DIR / "preconstruction_action_log.csv")
    estimator = pd.read_csv(OUTPUT_DIR / "estimator_review.csv")
    closeout = pd.read_csv(OUTPUT_DIR / "post_job_variance_review.csv")

    require(jobs["job_id"].is_unique, "jobs.job_id must be unique")
    require(summary["job_id"].is_unique, "summary.job_id must be unique")
    require(actuals["job_id"].is_unique, "actuals.job_id must be unique")
    require(actions["action_id"].is_unique, "action_id must be unique")
    require(set(jobs["job_id"]) == set(summary["job_id"]), "job and summary IDs must match")
    require(set(jobs["job_id"]) == set(actuals["job_id"]), "job and actual IDs must match")
    require(set(estimator["job_id"]) == set(jobs["job_id"]), "estimator view must cover every job")
    require(set(closeout["job_id"]) == set(jobs["job_id"]), "closeout view must cover every job")
    require(set(actions["job_id"]).issubset(set(jobs["job_id"])), "action jobs must exist")

    forbidden_prejob_terms = ("actual", "variance", "change_order")
    leaked = [column for column in actions.columns if any(term in column for term in forbidden_prejob_terms)]
    require(not leaked, f"preconstruction action log contains post-job fields: {leaked}")
    require(set(actions["status"]) == {"Open"}, "generated constraints must start Open")
    require(set(actions["priority"]).issubset({"High", "Medium", "Low"}), "unexpected priority")
    require(actions["blocker"].notna().all(), "every action needs a blocker")
    require(actions["next_action"].notna().all(), "every action needs a next action")
    require(actions["responsible_role"].notna().all(), "every action needs a responsible role")
    require(len(actions) > actions["job_id"].nunique(), "action log should allow multiple constraints per job")

    require(set(jobs["job_type"]).issubset({"Paver Patio", "Walkway"}), "unsupported estimator job type")
    require((summary["estimated_total_cost"] >= 0).all(), "estimated costs cannot be negative")
    require((actuals["actual_total_cost"] >= 0).all(), "actual costs cannot be negative")
    require((summary["estimated_labor_hours"] > 0).all(), "labor hours must be positive")
    require(np.isfinite(summary["estimated_margin_pct"]).all(), "estimated margins must be finite")
    require((summary["meets_target_margin"] == "No").any(), "scenario needs below-target-margin jobs")
    require((summary["meets_target_margin"] == "Yes").any(), "scenario needs healthy-margin jobs")
    require((summary["estimated_margin_pct"] < 0.18).any(), "scenario needs margin-review-threshold jobs")
    require(set(summary["workability_status"]) == {
        "No Additional Review Flagged", "Review Before Approval", "Site Review Required"
    }, "scenario must exercise all review statuses")
    require(set(actions["priority"]) == {"High", "Medium", "Low"}, "scenario must exercise all priorities")
    require((actions["constraint_category"] == "Readiness gate").any(), "scenario needs readiness blockers")
    require((actions["constraint_category"] == "Site constraint").any(), "scenario needs site constraints")

    calculated_cost = (
        summary["estimated_material_cost"]
        + summary["estimated_labor_cost"]
        + summary["estimated_equipment_cost"]
    )
    require(np.allclose(calculated_cost, summary["estimated_total_cost"], atol=0.02), "cost components do not reconcile")
    calculated_margin = (summary["quoted_price"] - summary["estimated_total_cost"]) / summary["quoted_price"]
    require(np.allclose(calculated_margin, summary["estimated_margin_pct"], atol=0.001), "estimated margin does not reconcile")
    component_totals = summary["risk_component_detail"].map(
        lambda detail: sum(int(part.rsplit("=", 1)[1]) for part in str(detail).split(" | "))
    )
    require((component_totals == summary["site_risk_points"]).all(), "site-risk component points do not reconcile")

    report = {
        "status": "passed",
        "job_count": int(len(jobs)),
        "open_action_count": int(len(actions)),
        "jobs_with_open_actions": int(actions["job_id"].nunique()),
        "below_target_margin_jobs": int((summary["meets_target_margin"] == "No").sum()),
        "review_status_counts": summary["workability_status"].value_counts().to_dict(),
        "priority_counts": actions["priority"].value_counts().to_dict(),
        "blocking_action_count": int((actions["blocking_flag"] == "Yes").sum()),
        "current_lookahead_action_count": int(actions["lookahead_bucket"].isin(["Due / Overdue", "Next 7 Days"]).sum()),
        "risk_model_version": str(summary["risk_model_version"].iloc[0]),
        "assumption_version": str(summary["assumption_version"].iloc[0]),
        "note": "Synthetic scenario coverage and data-contract checks; not model validation.",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
