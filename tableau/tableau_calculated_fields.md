# Tableau Calculated Fields

Use the persona-specific CSV for each dashboard. Tableau may display snake-case columns with title capitalization.

## Field Look-Ahead

Source: `outputs/preconstruction_action_log.csv`

### Open Action

```text
IF [Status] <> "Done" THEN 1 ELSE 0 END
```

### Due Soon

```text
IF [Lookahead Bucket] = "Due / Overdue"
OR [Lookahead Bucket] = "Next 7 Days"
THEN "Current Look-Ahead"
ELSE "Later"
END
```

### Priority Sort

```text
CASE [Priority]
WHEN "High" THEN 1
WHEN "Medium" THEN 2
ELSE 3
END
```

### Blocking Action

```text
IF [Blocking Flag] = "Yes" AND [Status] <> "Done" THEN 1 ELSE 0 END
```

## Estimator Review

Source: `outputs/estimator_review.csv`

### Estimated Margin

```text
([Quoted Price] - [Estimated Total Cost]) / [Quoted Price]
```

### Margin Gap

```text
[Estimated Margin Pct] - [Target Margin Pct]
```

### Commercial Review

```text
IF [Estimated Margin Pct] < [Target Margin Pct]
THEN "Below Target"
ELSE "Meets Target"
END
```

## Post-Job Learning

Source: `outputs/post_job_variance_review.csv`

### Cost Variance

```text
[Actual Total Cost] - [Estimated Total Cost]
```

### Labor Hour Variance

```text
[Actual Labor Hours] - [Estimated Labor Hours]
```

### Actual Margin

```text
([Quoted Price] - [Actual Total Cost]) / [Quoted Price]
```

### Cost Overrun Flag

```text
IF [Cost Variance] > 0 THEN "Overrun" ELSE "At / Below Estimate" END
```

The post-job results are simulated. Do not label these fields as predictive accuracy or validated model performance.

