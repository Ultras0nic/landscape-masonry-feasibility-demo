# Dashboard Specification

The dashboard separates current preconstruction work from retrospective learning. Actual cost fields never appear in the preconstruction view.

## 1. Field Look-Ahead

**Audience:** Project Manager, Operations Manager, Foreman / Crew Lead
**Source:** `outputs/preconstruction_action_log.csv`

Default filters:

- Status is not Done
- Look-ahead bucket is Due / Overdue or Next 7 Days
- My jobs / responsible role

Default columns:

`Priority | Job | Blocker | Next Action | Responsible Role | Assignee | Needed By | Status`

KPI cards:

- Blocking actions
- Due / overdue actions
- Next-seven-day actions
- Unassigned actions
- Stale open actions

Interaction: selecting a job shows all concurrent constraints rather than only one primary reason.

## 2. Estimator Review

**Audience:** Estimator / Owner
**Source:** `outputs/estimator_review.csv`

Metrics:

- Quote and estimated total cost
- Material, labor, and equipment cost
- Estimated labor hours and duration
- Estimated margin, target margin, and margin gap
- Site-risk points and component detail
- Review status and planned start

The view should let the estimator inspect and challenge assumptions. It is decision support, not automatic approval.

## 3. Post-Job Learning

**Audience:** Operations Analyst / Manager
**Source:** `outputs/post_job_variance_review.csv`

Metrics:

- Estimated vs actual total cost
- Estimated vs actual labor hours
- Estimated vs actual margin
- Change-event count and cost
- Variance by job type and scenario factor

Label all results as synthetic scenario behavior. Do not present them as predictive performance.

## Mobile design notes

- Put the action before detailed metrics.
- Use short blocker and next-action text.
- Keep one tap from the summary to job detail.
- Preserve filters between visits.
- Show freshness and ownership so the list supports action, not only visibility.
