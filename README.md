# Landscape & Masonry Job Feasibility Demo

## Project Overview

This project is a synthetic construction operations analytics demo for landscape and masonry job feasibility review.

The goal is to model how a work lead, foreman, estimator, project team, or operations analyst might review whether a job is workable, risky, underpriced, or likely to need additional site review before field execution.

This project focuses on analytics and business decision support. It does not replace architectural, engineering, structural, building code, or safety judgment.

All data is synthetic and created for portfolio demonstration purposes.

## Business Context

Landscape, masonry, and construction teams often receive client requests, design ideas, or early project scopes before confirming whether the work can be completed efficiently in the field.

A simplified workflow looks like:

```text
Client request / design idea
→ Site condition review
→ Material takeoff
→ Labor and crew estimate
→ Equipment and access check
→ Quote risk review
→ Field execution
→ Estimate vs actual comparison
→ Lessons for future bids
```

In this workflow, the architect or designer may focus on the design. The construction work lead, estimator, or project team needs to understand whether the job is practical to execute with available crew, tools, site access, budget, and schedule.

This demo supports that field planning, quote review, and operations analytics process.

## Business Problem

Small construction, landscaping, and masonry jobs can lose margin when field conditions are underestimated.

Common issues include:

- Narrow equipment access
- Long material carry distance
- Drainage concerns
- Demolition not fully included in the quote
- Slope or grading difficulty
- Crew size mismatch
- Labor-hour underestimation
- Material cost differences by state or market
- Actual cost exceeding estimated cost
- Change orders or scope clarifications after work begins

The business challenge is to identify these risks before the job starts, so the team can review the quote, request another site visit, clarify scope, adjust assumptions, or plan labor more realistically.

## User Persona Design

This project is designed around an important construction analytics lesson: the same data should be presented differently depending on the user.

### Field / Jobsite Team

Project teams and jobsite users often have limited time to sit at a desk and analyze detailed dashboards. For this audience, analytics should be simple, fast, and action-oriented.

The field view focuses on:

- What needs attention?
- Why is it risky?
- What action should be taken next?
- Who should own the follow-up?

This project includes a simplified field action queue:

```text
outputs/jobsite_action_queue.csv
```

### Estimator / Office Team

Estimators and office teams can usually work with more detail. They may need to review assumptions, cost breakdowns, labor logic, margins, and estimate-vs-actual differences.

The estimator review view focuses on:

- Quote vs estimated cost
- Material, labor, and equipment breakdown
- Estimated margin
- Estimate vs actual variance
- Common drivers of underestimation

### Operations Analyst

The operations analyst supports both groups by maintaining data quality, tracking exceptions, reviewing variance, and designing reporting workflows that fit how teams actually work.

The goal is not to replace field judgment or estimating experience. The goal is to create low-friction analytics that fit into the workflow and help teams catch risk earlier.

## Analyst Questions

This project answers questions such as:

1. Which jobs are workable, need review, or require site review?
2. Which jobs have the lowest estimated margin?
3. Which site conditions are associated with higher risk scores?
4. How do Massachusetts and Rhode Island jobs differ under the current assumptions?
5. Which jobs show simulated actual cost overruns?
6. Which jobs may need quote review before approval?
7. Which jobs should appear in a simple field action queue?
8. What data should be shown to field teams versus estimators or office teams?
9. What information should be prepared for a Tableau dashboard?

## Tools Used

- Python
- pandas
- NumPy
- SQL
- SQLite
- CSV outputs
- Tableau-ready dataset
- Tableau calculated field planning
- GitHub documentation

## Repository Structure

```text
landscape-masonry-feasibility-demo/
├── data/
│   ├── jobs.csv
│   ├── material_prices.csv
│   ├── labor_rates.csv
│   ├── production_rates.csv
│   └── actual_job_results.csv
├── scripts/
│   ├── generate_synthetic_data.py
│   ├── calculate_estimates.py
│   ├── create_action_queue.py
│   ├── load_to_sqlite.py
│   └── run_sql_queries.py
├── sql/
│   ├── create_tables.sql
│   └── analysis_queries.sql
├── docs/
│   ├── business_context.md
│   ├── assumptions.md
│   ├── data_dictionary.md
│   └── field_terms.md
├── outputs/
│   ├── job_feasibility_summary.csv
│   ├── tableau_job_feasibility_summary.csv
│   ├── jobsite_action_queue.csv
│   ├── one_page_analysis_brief.md
│   └── query_results/
├── dashboard_mockup/
│   └── dashboard_notes.md
├── tableau/
│   ├── tableau_calculated_fields.md
│   └── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

## Data Note

The CSV files in this project are synthetic and included for demonstration purposes.

The SQLite database file is not included in the repository because it can be regenerated locally by running the scripts.

## How to Run This Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate synthetic job data

```bash
python scripts/generate_synthetic_data.py
```

This creates synthetic input files in the `data/` folder, including job records, material prices, labor rates, and production rates.

### 3. Calculate estimates and risk scores

```bash
python scripts/calculate_estimates.py
```

This creates:

```text
outputs/job_feasibility_summary.csv
data/actual_job_results.csv
outputs/tableau_job_feasibility_summary.csv
```

### 4. Create field action queue

```bash
python scripts/create_action_queue.py
```

This creates:

```text
outputs/jobsite_action_queue.csv
```

The field action queue is a simplified output designed for project teams or work leads who need fast, low-friction information.

### 5. Load data into SQLite

```bash
python scripts/load_to_sqlite.py
```

This creates a local SQLite database:

```text
landscape_masonry_demo.db
```

### 6. Run SQL analysis queries

```bash
python scripts/run_sql_queries.py
```

This runs the queries in:

```text
sql/analysis_queries.sql
```

and saves results to:

```text
outputs/query_results/
```

## Data Model

The project uses a simplified data model:

```text
jobs
→ material_prices
→ labor_rates
→ production_rates
→ job_feasibility_summary
→ actual_job_results
→ jobsite_action_queue
```

The main analysis table is:

```text
outputs/job_feasibility_summary.csv
```

The Tableau-ready dataset is:

```text
outputs/tableau_job_feasibility_summary.csv
```

The simplified field-facing output is:

```text
outputs/jobsite_action_queue.csv
```

## Estimation Logic

The demo estimates:

- Material cost
- Labor hours
- Labor cost
- Equipment cost
- Estimated total cost
- Estimated margin
- Risk score
- Workability status
- Simulated actual cost
- Actual margin
- Cost variance
- Margin variance
- Change order flag

The calculation logic uses simplified assumptions for Massachusetts and Rhode Island. These assumptions can be updated later as the project becomes more realistic.

## Risk Scoring Logic

The risk score is based on field conditions such as:

- Narrow access width
- Medium or high slope
- Drainage concern
- Demolition required
- Long material carry distance
- Large job size
- Small crew size for larger jobs
- Estimated margin below target

Workability status is classified as:

```text
Workable
Review Before Approval
Requires Site Review
```

## Field Action Queue Logic

The field action queue translates detailed risk and cost data into a simple action-oriented output.

Key fields include:

- Job ID
- State
- City
- Job type
- Workability status
- Risk score
- Risk category
- Estimated margin
- Actual margin
- Cost variance
- Primary risk reason
- Recommended action
- Priority
- Owner role
- Field notes required

This output is designed to answer:

```text
Which jobs need attention, why, and what should happen next?
```

Examples of recommended actions include:

- Schedule site review before approval
- Review quote and scope assumptions
- Confirm drainage plan before scheduling
- Confirm equipment access and material staging
- Review labor hours for material movement
- Confirm demolition scope and disposal needs
- Compare estimate assumptions with actual cost

## SQL Analysis

The SQL analysis answers business-facing questions such as:

- Which jobs require review before approval?
- Which jobs have the lowest estimated margin?
- What is the average risk and margin by state?
- What is the average risk and margin by job type?
- Which jobs had simulated cost overruns?
- Which risk factors are most common?
- Which jobs are below target margin?
- Which jobs should be prioritized in a field action queue?

Query outputs are saved in:

```text
outputs/query_results/
```

## Key Findings From Synthetic Data

A short business summary is available in:

```text
outputs/one_page_analysis_brief.md
```

Main findings include:

1. Jobs with narrow access, drainage concerns, demolition requirements, slope/grading difficulty, and long material carry distances received higher risk scores.

2. Some jobs appeared workable by size alone but had low estimated margins after material, labor, equipment, and field-risk adjustments.

3. High-risk jobs were more likely to show simulated actual cost overruns compared with estimated cost.

4. Massachusetts jobs had higher estimated costs than Rhode Island jobs because the demo uses higher labor and material assumptions for MA.

5. A simplified field action queue can help project teams quickly see which jobs need attention, why they are risky, who should follow up, and what action should happen next.

## Tableau Dashboard Plan

The Tableau-ready dataset is:

```text
outputs/tableau_job_feasibility_summary.csv
```

A simplified field action queue is also included:

```text
outputs/jobsite_action_queue.csv
```

The dashboard is designed with two different user needs in mind.

### 1. Field Action View

This view is designed for project teams and jobsite users who need fast, low-friction information.

Key fields:

- Job ID
- City
- Job type
- Workability status
- Risk score
- Primary risk reason
- Recommended action
- Priority
- Owner role
- Field notes required

Main question:

```text
Which jobs need attention, why, and what should happen next?
```

### 2. Estimator Review View

This view is designed for estimators, office teams, and operations analysts who need more detail.

Key metrics:

- Quoted price
- Estimated total cost
- Estimated material cost
- Estimated labor cost
- Estimated equipment cost
- Estimated margin
- Actual total cost
- Cost variance
- Actual margin
- Change order flag

Main question:

```text
Where did the estimate differ from the actual result, and what assumptions should be reviewed?
```

### 3. Operations Summary View

This view helps operations leaders understand patterns across jobs.

Focus areas:

- Jobs below target margin
- High-risk jobs by state
- Risk score by job type
- Cost overrun by job type
- Common risk factors
- Estimate-vs-actual variance trends
- Change order count

## Key Skills Demonstrated

- Synthetic data generation
- Data cleaning and transformation
- Cost estimation logic
- Rule-based risk scoring
- SQL analysis
- SQLite workflow
- Tableau-ready data preparation
- Field action queue design
- Operations analytics
- Estimate vs actual variance analysis
- User persona-based dashboard planning
- Business communication
- Construction workflow research

## Limitations

This project uses synthetic data and simplified assumptions.

It does not represent real construction bids, real material prices, real labor rates, structural engineering rules, building codes, permitting requirements, or safety requirements.

The purpose is to demonstrate how an analyst could structure construction operations data, estimate job feasibility, flag risks, create low-friction action outputs, and communicate findings for business review.

## Possible Next Steps

Future improvements could include:

- Building Tableau dashboard views for both field and estimator audiences
- Adding screenshots of the Tableau dashboard to the repository
- Adding clearer risk-reason hierarchy
- Adding job phase or schedule status
- Adding crew productivity history
- Adding weather delay risk
- Adding customer change-order reasons
- Adding real local material price assumptions
- Improving Massachusetts and Rhode Island assumption tables
- Adding user feedback fields for project teams
- Adding retaining wall-specific logic carefully without claiming structural engineering judgment
- Building a Streamlit version for interactive job review