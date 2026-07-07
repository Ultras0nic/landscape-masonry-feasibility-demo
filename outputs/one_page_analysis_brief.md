# One-Page Analysis Brief

## Project Question

How can a landscape/masonry or construction operations team review job feasibility, estimate cost, flag risk, and identify which jobs need attention before field execution?

## Project Context

This project is a synthetic analytics demo for construction operations and landscape/masonry job review.

The original goal was to help a work lead or estimator understand whether a quoted job is workable, risky, underpriced, or likely to need additional review. After receiving feedback from a construction data analyst, the project was updated to separate two different user needs:

1. Field or jobsite teams need simple, low-friction information that fits into a busy workflow.
2. Estimators, office teams, and operations analysts can work with more detailed cost, risk, and estimate-vs-actual analysis.

Because of this, the project now includes both a detailed feasibility review and a simplified field action queue.

## Key Findings From Synthetic Data

1. Jobs with narrow access, drainage concerns, demolition requirements, slope/grading difficulty, and long material carry distances received higher risk scores.

2. Some jobs appeared workable by size alone but had low estimated margins after material, labor, equipment, and field-risk adjustments.

3. High-risk jobs were more likely to show simulated actual cost overruns compared with estimated cost.

4. Massachusetts jobs had higher estimated costs than Rhode Island jobs because the demo uses higher labor and material assumptions for MA.

5. A simplified field action queue can help project teams quickly see which jobs need attention, why they are risky, who should follow up, and what action should happen next.

## Business Interpretation

The main value of this workflow is not only calculating estimates. It is translating detailed job, cost, and risk data into the right level of information for the right user.

For field or jobsite teams, the useful question is:

What needs attention today, and what should we do next?

For estimators and office teams, the useful question is:

Which assumptions, costs, or risk factors explain the estimate-vs-actual gap?

For operations analysts, the useful question is:

How can we maintain data quality, track exceptions, and design reporting that supports both field teams and office teams?

## Field Action Queue

The project includes a simplified field action queue:

outputs/jobsite_action_queue.csv

This output is designed for project teams or work leads who may not have time to review a full dashboard.

Key fields include:

- Job ID
- Workability status
- Risk score
- Risk category
- Primary risk reason
- Recommended action
- Priority
- Owner role
- Field notes required

The goal is to make the output action-oriented instead of only analytical.

Example business questions:

- Which jobs need site review before approval?
- Which jobs have the highest priority?
- What is the main reason each job is risky?
- Who should follow up?
- What action should happen next?

## Detailed Estimate / Office Review

The detailed review is designed for estimators, office teams, and operations analysts.

Key fields include:

- Quoted price
- Estimated material cost
- Estimated labor cost
- Estimated equipment cost
- Estimated total cost
- Estimated margin
- Actual total cost
- Actual margin
- Cost variance
- Labor hour variance
- Change order flag
- Risk score
- Workability status

This view helps explain why a job may be underpriced, risky, or likely to exceed the original estimate.

## Recommended Dashboard Views

### 1. Field Action View

This view is designed for low-friction use by project teams.

Recommended metrics and fields:

- Jobs requiring site review
- High-priority jobs
- Primary risk reason
- Recommended action
- Owner role
- Field notes required

Main purpose:

Help the field or project team quickly understand what needs attention.

### 2. Estimator Review View

This view is designed for more detailed quote and assumption review.

Recommended metrics and fields:

- Quote vs estimated total cost
- Material, labor, and equipment cost breakdown
- Estimated margin
- Jobs below target margin
- Risk score by job
- Site constraints by job
- Estimate vs actual variance

Main purpose:

Help estimators understand whether the quote, scope, labor assumptions, or site conditions need review.

### 3. Operations Summary View

This view is designed for operations analysts and managers.

Recommended metrics and fields:

- Total jobs reviewed
- Jobs requiring review
- Average estimated margin
- Average risk score
- Average cost variance
- Cost overrun count
- Change order count
- Risk score by state
- Risk score by job type
- Cost overrun by job type

Main purpose:

Help operations teams identify patterns across jobs, states, job types, and risk categories.

## Practical Business Questions

A work lead, estimator, or operations analyst could use this workflow to ask:

- Can equipment access the site?
- Is the material carry distance realistic?
- Is drainage likely to create rework?
- Is demolition included in the quote?
- Is the crew size realistic for the job size?
- Is the quoted price enough for expected labor, materials, and equipment?
- Should the job require another site visit before approval?
- Which jobs are likely to need a change order?
- Which assumptions should be updated for future estimates?

## Key Takeaway

Construction analytics is not only about building a dashboard. The more important challenge is making the data useful for the audience.

Field teams need fast, simple, action-oriented information.

Office teams and estimators need detailed assumptions, cost breakdowns, and variance analysis.

This project shows both layers by combining a detailed feasibility model with a simplified field action queue.

## Next Steps

Future improvements could include:

- Build Tableau dashboard views for both field and estimator audiences
- Add screenshots of the Tableau dashboard to the repository
- Add clearer risk-reason hierarchy
- Add job phase or schedule status
- Add crew productivity history
- Add weather delay risk
- Add customer change-order reasons
- Improve Massachusetts and Rhode Island cost assumptions
- Add more realistic material price tables
- Add user feedback fields for project teams
- Add retaining wall-specific logic carefully without claiming structural engineering judgment