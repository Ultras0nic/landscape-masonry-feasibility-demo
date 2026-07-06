# Tableau Calculated Fields

This project uses `outputs/tableau_job_feasibility_summary.csv` as the main Tableau-ready dataset.

## Estimated Margin %

```text
([Quoted Price] - [Estimated Total Cost]) / [Quoted Price]

([Quoted Price] - [Actual Total Cost]) / [Quoted Price]

[Actual Total Cost] - [Estimated Total Cost]

[Actual Labor Hours] - [Estimated Labor Hours]

IF [Risk Score] >= 60 OR [Estimated Margin Pct] < 0.18
THEN "Review"
ELSE "OK"
END

IF [Cost Variance] > 0
THEN "Overrun"
ELSE "No Overrun"
END