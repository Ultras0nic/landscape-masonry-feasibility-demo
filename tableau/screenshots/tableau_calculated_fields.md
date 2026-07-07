# Tableau Calculated Fields

This project uses `outputs/tableau_job_feasibility_summary.csv` as the main Tableau-ready dataset.

A simplified field action queue is also included:

```text
outputs/jobsite_action_queue.csv
```

These calculated fields can be created in Tableau after connecting to the CSV file.

Note: Tableau may display column names with spaces instead of underscores. For example, `quoted_price` may appear as `Quoted Price`.

---

## Estimated Margin %

```text
([Quoted Price] - [Estimated Total Cost]) / [Quoted Price]
```

Purpose:

This shows the expected profit margin before the job is completed.

---

## Actual Margin %

```text
([Quoted Price] - [Actual Total Cost]) / [Quoted Price]
```

Purpose:

This shows the actual margin after simulated job results are available.

---

## Cost Variance

```text
[Actual Total Cost] - [Estimated Total Cost]
```

Purpose:

This shows whether the job cost more or less than estimated.

Positive value = cost overrun  
Negative value = cost savings

---

## Labor Hour Variance

```text
[Actual Labor Hours] - [Estimated Labor Hours]
```

Purpose:

This shows whether labor hours were underestimated or overestimated.

---

## Needs Review Flag

```text
IF [Risk Score] >= 60 OR [Estimated Margin Pct] < 0.18
THEN "Review"
ELSE "OK"
END
```

Purpose:

This creates a simple review flag for jobs with high risk or low estimated margin.

---

## Cost Overrun Flag

```text
IF [Cost Variance] > 0
THEN "Overrun"
ELSE "No Overrun"
END
```

Purpose:

This identifies jobs where actual cost was higher than estimated cost.

---

## Priority Group

```text
IF [Risk Score] >= 60 THEN "High"
ELSEIF [Estimated Margin Pct] < 0.18 THEN "Medium"
ELSE "Low"
END
```

Purpose:

This gives Tableau a simple priority field for dashboard filtering.

---

## Field Action Label

```text
IF [Workability Status] = "Requires Site Review" THEN "Site Review Needed"
ELSEIF [Workability Status] = "Review Before Approval" THEN "Review Before Approval"
ELSE "Standard Review"
END
```

Purpose:

This creates a simple label for the field-facing dashboard view.

---

## Recommended Tableau Views

### Field Action View

Use `outputs/jobsite_action_queue.csv`.

This view should answer:

```text
Which jobs need attention, why, and what should happen next?
```

Recommended fields:

- Job ID
- City
- Job Type
- Workability Status
- Risk Score
- Primary Risk Reason
- Recommended Action
- Priority
- Owner Role
- Field Notes Required

### Estimator Review View

Use `outputs/tableau_job_feasibility_summary.csv`.

This view should answer:

```text
Where did the estimate differ from the actual result, and what assumptions should be reviewed?
```

Recommended fields:

- Quoted Price
- Estimated Total Cost
- Estimated Material Cost
- Estimated Labor Cost
- Estimated Equipment Cost
- Estimated Margin Pct
- Actual Total Cost
- Cost Variance
- Actual Margin Pct
- Change Order Flag

### Operations Summary View

Use `outputs/tableau_job_feasibility_summary.csv`.

This view should answer:

```text
What patterns appear across jobs, states, job types, and risk categories?
```

Recommended metrics:

- Total Jobs
- Jobs Requiring Review
- Average Estimated Margin
- Average Risk Score
- Average Cost Variance
- Cost Overrun Count
- Change Order Count