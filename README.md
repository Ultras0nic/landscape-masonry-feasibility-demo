# Landscape & Masonry Job Feasibility Demo

## Project Overview

This project is a synthetic construction operations analytics demo for landscape and masonry job feasibility review.

The goal is to model how a work lead, foreman, estimator, or operations analyst might review whether a job is workable, risky, underpriced, or likely to need additional site review before field execution.

This project focuses on analytics and business decision support. It does not replace architectural, engineering, structural, or safety judgment.

All data is synthetic and created for portfolio demonstration purposes.

## Business Context

Landscape and masonry companies often receive client requests or design ideas before confirming whether the work can be completed efficiently in the field.

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

In this workflow, the architect or designer may focus on the design. The construction work lead needs to understand whether the job is practical to execute with available crew, tools, site access, budget, and schedule.

This demo supports that field planning and quote review process.

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

The business challenge is to identify these risks before the job starts, so the team can review the quote, request another site visit, clarify scope, or plan labor more realistically.

## Analyst Questions

This project answers questions such as:

1. Which jobs are workable, need review, or require site review?
2. Which jobs have the lowest estimated margin?
3. Which site conditions are associated with higher risk scores?
4. How do Massachusetts and Rhode Island jobs differ under the current assumptions?
5. Which jobs show simulated actual cost overruns?
6. Which jobs may need quote review before approval?
7. What data should be shown in a Tableau dashboard for work leads?

## Tools Used

- Python
- pandas
- NumPy
- SQL
- SQLite
- CSV outputs
- Tableau-ready dataset
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

### 4. Load data into SQLite

```bash
python scripts/load_to_sqlite.py
```

This creates a local SQLite database:

```text
landscape_masonry_demo.db
```

### 5. Run SQL analysis queries

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
```

The main analysis table is:

```text
outputs/job_feasibility_summary.csv
```

The Tableau-ready dataset is:

```text
outputs/tableau_job_feasibility_summary.csv
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
- Cost variance
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

Workability status is classified as:

```text
Workable
Review Before Approval
Requires Site Review
```

## SQL Analysis

The SQL analysis answers business-facing questions such as:

- Which jobs require review before approval?
- Which jobs have the lowest estimated margin?
- What is the average risk and margin by state?
- What is the average risk and margin by job type?
- Which jobs had simulated cost overruns?
- Which risk factors are most common?
- Which jobs are below target margin?

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

1. Jobs with narrow access, drainage concerns, demolition requirements, and long material carry distances received higher risk scores.

2. Some jobs appeared workable by size alone but had low estimated margins after material, labor, equipment, and risk adjustments.

3. High-risk jobs were more likely to show simulated actual cost overruns compared with estimated cost.

4. Massachusetts jobs had higher estimated costs than Rhode Island jobs because the demo uses higher labor and material assumptions for MA.

5. A pre-job review dashboard could help a work lead identify jobs that need quote review, site inspection, or customer clarification before scheduling.

## Tableau Dashboard Plan

The Tableau-ready dataset is:

```text
outputs/tableau_job_feasibility_summary.csv
```

The dashboard is planned around five pages:

### 1. Job Feasibility Overview

- Total jobs reviewed
- Jobs requiring site review
- Jobs below target margin
- Average estimated margin
- Average risk score
- Change order rate

### 2. Estimate Breakdown

- Quoted price vs estimated total cost
- Estimated material cost by job
- Estimated labor cost by job
- Estimated equipment cost by job
- Estimated margin by job

### 3. Field Risk Review

- Risk score by job
- Risk score by state
- Risk score by job type
- Access width vs estimated labor hours
- Drainage concern vs cost overrun
- Demolition required vs cost overrun

### 4. Estimate vs Actual

- Estimated cost vs actual cost
- Estimated margin vs actual margin
- Cost variance by job
- Labor hour variance by job
- Change order flag by risk category

### 5. State Assumption Review

- Massachusetts vs Rhode Island average estimated cost
- Massachusetts vs Rhode Island average risk score
- Massachusetts vs Rhode Island average estimated margin
- Material and labor cost assumption comparison

## Key Skills Demonstrated

- Synthetic data generation
- Data cleaning and transformation
- Cost estimation logic
- Rule-based risk scoring
- SQL analysis
- SQLite workflow
- Tableau-ready data preparation
- Operations analytics
- Estimate vs actual variance analysis
- Business communication
- Dashboard planning

## Limitations

This project uses synthetic data and simplified assumptions.

It does not represent real construction bids, real material prices, real labor rates, structural engineering rules, building codes, or safety requirements.

The purpose is to demonstrate how an analyst could structure construction operations data, estimate job feasibility, flag risks, and communicate findings for business review.

## Possible Next Steps

Future improvements could include:

- Adding retaining wall-specific logic
- Adding weather delay risk
- Adding crew productivity history
- Adding real local material price assumptions
- Adding customer change-order reasons
- Creating a Tableau Public dashboard
- Adding screenshots of dashboard pages
- Improving Massachusetts and Rhode Island assumption tables
- Building a Streamlit version for interactive job review