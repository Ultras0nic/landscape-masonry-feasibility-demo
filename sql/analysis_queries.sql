-- Query 1: Jobs that require review before approval
SELECT
    job_id,
    state,
    city,
    job_type,
    quoted_price,
    estimated_total_cost,
    estimated_margin_pct,
    risk_score,
    risk_category,
    workability_status
FROM job_feasibility_summary
WHERE workability_status <> 'Workable'
ORDER BY risk_score DESC, estimated_margin_pct ASC;

-- Query 2: Lowest estimated margin jobs
SELECT
    job_id,
    state,
    city,
    job_type,
    quoted_price,
    estimated_total_cost,
    estimated_margin_pct,
    target_margin_pct
FROM job_feasibility_summary
ORDER BY estimated_margin_pct ASC
LIMIT 15;

-- Query 3: Average risk and margin by state
SELECT
    state,
    COUNT(*) AS job_count,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(estimated_margin_pct), 3) AS avg_estimated_margin,
    ROUND(AVG(estimated_total_cost), 2) AS avg_estimated_cost
FROM job_feasibility_summary
GROUP BY state
ORDER BY avg_risk_score DESC;

-- Query 4: Average risk and margin by job type
SELECT
    job_type,
    COUNT(*) AS job_count,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(estimated_margin_pct), 3) AS avg_estimated_margin,
    ROUND(AVG(estimated_labor_hours), 2) AS avg_labor_hours
FROM job_feasibility_summary
GROUP BY job_type
ORDER BY avg_risk_score DESC;

-- Query 5: Estimate vs actual cost comparison
SELECT
    s.job_id,
    s.state,
    s.city,
    s.job_type,
    s.quoted_price,
    s.estimated_total_cost,
    a.actual_total_cost,
    a.cost_variance,
    s.estimated_margin_pct,
    a.actual_margin_pct,
    a.margin_variance,
    a.change_order_flag
FROM job_feasibility_summary s
JOIN actual_job_results a
    ON s.job_id = a.job_id
ORDER BY a.cost_variance DESC;

-- Query 6: Jobs with cost overrun
SELECT
    s.job_id,
    s.state,
    s.city,
    s.job_type,
    s.risk_score,
    s.risk_category,
    s.drainage_concern,
    s.demo_required,
    s.access_width_ft,
    s.carry_distance_ft,
    s.estimated_total_cost,
    a.actual_total_cost,
    a.cost_variance,
    a.change_order_flag
FROM job_feasibility_summary s
JOIN actual_job_results a
    ON s.job_id = a.job_id
WHERE a.cost_variance > 0
ORDER BY a.cost_variance DESC;

-- Query 7: Risk factor summary
SELECT
    SUM(CASE WHEN access_width_ft < 6 THEN 1 ELSE 0 END) AS narrow_access_jobs,
    SUM(CASE WHEN drainage_concern = 'Yes' THEN 1 ELSE 0 END) AS drainage_concern_jobs,
    SUM(CASE WHEN demo_required = 'Yes' THEN 1 ELSE 0 END) AS demo_required_jobs,
    SUM(CASE WHEN carry_distance_ft > 60 THEN 1 ELSE 0 END) AS long_carry_distance_jobs,
    SUM(CASE WHEN slope_level IN ('Medium', 'High') THEN 1 ELSE 0 END) AS slope_risk_jobs
FROM job_feasibility_summary;

-- Query 8: Workability status count
SELECT
    workability_status,
    COUNT(*) AS job_count,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(estimated_margin_pct), 3) AS avg_estimated_margin
FROM job_feasibility_summary
GROUP BY workability_status
ORDER BY job_count DESC;

-- Query 9: Jobs below target margin
SELECT
    job_id,
    state,
    city,
    job_type,
    quoted_price,
    estimated_total_cost,
    estimated_margin_pct,
    target_margin_pct,
    risk_score,
    workability_status
FROM job_feasibility_summary
WHERE estimated_margin_pct < target_margin_pct
ORDER BY estimated_margin_pct ASC;

-- Query 10: Tableau summary by state and job type
SELECT
    state,
    job_type,
    COUNT(*) AS job_count,
    ROUND(AVG(quoted_price), 2) AS avg_quoted_price,
    ROUND(AVG(estimated_total_cost), 2) AS avg_estimated_total_cost,
    ROUND(AVG(estimated_margin_pct), 3) AS avg_estimated_margin,
    ROUND(AVG(risk_score), 2) AS avg_risk_score
FROM job_feasibility_summary
GROUP BY state, job_type
ORDER BY state, job_type;