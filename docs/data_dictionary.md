# Data Dictionary

## Core inputs

| File | Grain | Purpose |
|---|---|---|
| `data/jobs.csv` | One row per planned job | Scope, site conditions, readiness gates, quote, and schedule |
| `data/material_prices.csv` | State and material | Versioned illustrative unit-cost assumptions |
| `data/labor_rates.csv` | State | Versioned illustrative labor-rate assumptions |
| `data/production_rates.csv` | Job type | Versioned illustrative production assumptions |
| `data/actual_job_results.csv` | One row per completed job | Synthetic closeout outcomes |

## Persona outputs

| File | Grain | Important fields |
|---|---|---|
| `outputs/estimator_review.csv` | One row per job | Cost components, labor hours, margin gap, site-risk points, drivers |
| `outputs/preconstruction_action_log.csv` | One row per open constraint | Priority, blocker, next action, responsible role, assignee, needed by, status, blocking flag |
| `outputs/post_job_variance_review.csv` | One row per completed job | Estimated and actual cost/labor/margin, change event |

## Key definitions

- **Site-risk points:** Sum of transparent illustrative rule points; not a probability.
- **Blocking flag:** Indicates a missing readiness prerequisite, independent of priority.
- **Priority:** Combines action severity with time to planned start.
- **Look-ahead bucket:** `Due / Overdue`, `Next 7 Days`, or `Later` based on needed-by date.
- **Margin gap:** Estimated margin minus target margin.
- **Review status:** Operational review flag only; not constructability or engineering approval.

