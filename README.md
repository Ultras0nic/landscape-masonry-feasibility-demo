# Landscape & Masonry Estimate Review Demo

This portfolio project demonstrates a reproducible construction-operations workflow using 60 synthetic paver patio and walkway scenarios in Massachusetts and Rhode Island.

Python generates pre-job cost estimates and transparent review flags, produces a low-friction preconstruction constraint log, and simulates post-job results for estimate-versus-actual analysis. SQL and Tableau-ready outputs support detailed office review and retrospective learning.

The design reflects practical feedback from a construction data professional: project teams need concise, action-oriented information that fits their workflow, while estimators need detail, accuracy, and assumptions they can inspect.

> This is a synthetic, rule-based analytics demonstration. It does not determine constructability, replace estimating judgment, or provide engineering, code, permitting, or safety approval.

## Workflow and audiences

```text
Estimate review → Preconstruction readiness → Field handoff → Post-job learning
```

| Stage | Primary user | Main output | Decision supported |
|---|---|---|---|
| Estimate review | Estimator / owner | [`estimator_review.csv`](outputs/estimator_review.csv) | Inspect cost assumptions, margin, and site-risk points |
| Preconstruction readiness | PM / operations / crew lead | [`preconstruction_action_log.csv`](outputs/preconstruction_action_log.csv) | See each blocker, next action, owner, needed-by date, and status |
| Field handoff | Project team | Filtered action log | Focus on open items due now or in the next seven days |
| Post-job learning | Operations analyst | [`post_job_variance_review.csv`](outputs/post_job_variance_review.csv) | Compare estimate and simulated actual results |

The action log is one row per constraint, not one row per job. It deliberately excludes actual cost, margin variance, and change-order results so pre-job decisions cannot use future information.

## What changed after industry feedback

- Split pre-job decisions from post-job outcomes.
- Replaced the all-jobs “field queue” with a row-per-constraint readiness log.
- Added hard readiness gates for scope, access, utility locate, permits, materials, and crew assignment.
- Added priority, blocking flag, responsible role, assignee, needed-by date, look-ahead bucket, status, and last-updated date.
- Kept a detailed estimator view while making the field-facing columns concise.
- Limited the estimator to paver flatwork. Retaining walls were removed because they require different geometry, drainage, reinforcement, and engineering-review inputs.

## Quick start

Requires Python 3.12+.

```bash
python -m pip install -r requirements.txt
python scripts/run_pipeline.py
```

The pipeline regenerates synthetic inputs, estimates, persona views, SQLite tables, SQL results, and a validation report. Individual steps are also runnable:

```bash
python scripts/generate_synthetic_data.py
python scripts/calculate_estimates.py
python scripts/create_action_queue.py
python scripts/load_to_sqlite.py
python scripts/run_sql_queries.py
python scripts/validate_outputs.py
```

## Method summary

The estimator calculates simplified material takeoff, labor hours, equipment days, estimated total cost, and estimated margin. Site conditions are translated into transparent `site_risk_points`, with every driver and point contribution retained in the output.

Commercial margin review and site-risk points are separate signals. Hard readiness gates are also separate: a missing prerequisite can remain blocking even when the numeric site-risk points are low.

The closeout generator uses separate synthetic labor, material, and change-event mechanisms. These are designed scenarios, not model predictions. See [methodology](docs/methodology.md) and the [data dictionary](docs/data_dictionary.md).

## Scenario validation

[`validation_report.json`](outputs/validation_report.json) records reproducibility and data-contract checks. The current fixed-seed scenario contains:

- 60 jobs with unique IDs
- healthy-margin and below-target-margin cases
- all three review statuses
- High, Medium, and Low action priorities
- one-to-many job-to-constraint relationships
- no post-job fields in the preconstruction action log
- reconciled estimate cost components and margin formulas

This is scenario validation, not statistical calibration or predictive-model validation.

## SQL and Tableau

SQLite uses the enforced schema in [`create_tables.sql`](sql/create_tables.sql), including primary keys, foreign keys, checks, and the action log. Twelve queries produce named outputs covering estimate review, readiness actions, state/job-type summaries, and post-job learning.

The Tableau specification uses three views:

1. **Field look-ahead:** Priority, Job, Blocker, Next Action, Owner, Needed By, Status.
2. **Estimator review:** Quote, cost components, labor assumptions, target margin, site-risk drivers, and review status.
3. **Post-job learning:** Estimate vs actual cost and labor, margin variance, and synthetic change events.

See [dashboard notes](dashboard_mockup/dashboard_notes.md) and [Tableau calculated fields](tableau/tableau_calculated_fields.md).

## Repository structure

```text
├── .github/workflows/validate.yml
├── data/                       # synthetic inputs and closeout outcomes
├── docs/
│   ├── ai_extension.md
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── workflow_design.md
├── outputs/
│   ├── estimator_review.csv
│   ├── preconstruction_action_log.csv
│   ├── post_job_variance_review.csv
│   ├── query_results/
│   └── validation_report.json
├── scripts/
│   ├── generate_synthetic_data.py
│   ├── calculate_estimates.py
│   ├── create_action_queue.py
│   ├── load_to_sqlite.py
│   ├── run_sql_queries.py
│   ├── validate_outputs.py
│   └── run_pipeline.py
├── sql/
├── tableau/
├── requirements.txt
└── README.md
```

## Limitations

- All jobs, prices, rates, schedules, and outcomes are synthetic.
- MA/RI differences are encoded assumptions, not current market-price findings.
- Site-risk points are illustrative rules, not calibrated probabilities.
- Simulated actuals demonstrate a feedback workflow; they do not prove risk factors cause overruns.
- The MVP covers paver patios and walkways only.
- No output replaces site inspection, utility locating, permits, engineering, or safety review.

## Responsible AI extension

The deterministic workflow remains authoritative. A future AI feature could convert a short field note into a human-confirmed structured draft and clarification questions; it should never approve feasibility, change quotes, or infer measurements. The bounded design is documented in [`docs/ai_extension.md`](docs/ai_extension.md).
