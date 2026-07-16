# Workflow Design

## Design principle

Construction analytics should meet each user inside the work they already perform. A detailed estimator view and a mobile field view can use related data without presenting the same interface.

## Lifecycle

### 1. Estimate review

The estimator or owner reviews quantity assumptions, labor production, material and equipment cost, target margin, and site constraints. The output is `outputs/estimator_review.csv`.

### 2. Preconstruction readiness

Each missing prerequisite or site constraint becomes a separate action in `outputs/preconstruction_action_log.csv`. Hard gates are kept separate from numeric site-risk points.

### 3. Field handoff

The project team filters the action log to open items due now or in the next seven days. The default field view should show only:

`Priority | Job | Blocker | Next Action | Responsible Role | Needed By | Status`

### 4. Post-job learning

Actual results enter only after execution. `outputs/post_job_variance_review.csv` supports retrospective review of labor, cost, margin, and synthetic change events.

## Adoption measures for a future real deployment

- Open and stale constraints by planned start date
- Median action closure time
- Percentage of hard gates completed before mobilization
- Field update completion rate
- Estimate-to-actual variance by cost category
- Repeated change-event reasons

