PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS post_job_variance_review;
DROP TABLE IF EXISTS preconstruction_action_log;
DROP TABLE IF EXISTS actual_job_results;
DROP TABLE IF EXISTS job_feasibility_summary;
DROP TABLE IF EXISTS production_rates;
DROP TABLE IF EXISTS labor_rates;
DROP TABLE IF EXISTS material_prices;
DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    job_name TEXT NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('MA', 'RI')),
    city TEXT NOT NULL,
    job_type TEXT NOT NULL CHECK (job_type IN ('Paver Patio', 'Walkway')),
    area_sqft REAL NOT NULL CHECK (area_sqft > 0),
    perimeter_ft REAL NOT NULL CHECK (perimeter_ft > 0),
    base_depth_in REAL NOT NULL CHECK (base_depth_in > 0),
    sand_depth_in REAL NOT NULL CHECK (sand_depth_in > 0),
    slope_level TEXT NOT NULL,
    access_width_ft REAL NOT NULL CHECK (access_width_ft > 0),
    drainage_concern TEXT NOT NULL,
    demo_required TEXT NOT NULL,
    carry_distance_ft REAL NOT NULL CHECK (carry_distance_ft >= 0),
    crew_size INTEGER NOT NULL CHECK (crew_size > 0),
    quoted_price REAL NOT NULL CHECK (quoted_price > 0),
    target_margin_pct REAL NOT NULL,
    project_phase TEXT NOT NULL,
    scenario_date TEXT NOT NULL,
    planned_start_date TEXT NOT NULL,
    scope_approved TEXT NOT NULL,
    site_access_verified TEXT NOT NULL,
    utility_locate_status TEXT NOT NULL,
    permit_status TEXT NOT NULL,
    materials_status TEXT NOT NULL,
    crew_assigned TEXT NOT NULL,
    assumption_version TEXT NOT NULL
);

CREATE TABLE material_prices (
    state TEXT NOT NULL,
    material_type TEXT NOT NULL,
    unit TEXT NOT NULL,
    unit_cost REAL NOT NULL CHECK (unit_cost >= 0),
    effective_date TEXT NOT NULL,
    assumption_version TEXT NOT NULL,
    source_note TEXT NOT NULL,
    PRIMARY KEY (state, material_type)
);

CREATE TABLE labor_rates (
    state TEXT PRIMARY KEY,
    labor_cost_per_hour REAL NOT NULL CHECK (labor_cost_per_hour >= 0),
    effective_date TEXT NOT NULL,
    assumption_version TEXT NOT NULL,
    source_note TEXT NOT NULL
);

CREATE TABLE production_rates (
    job_type TEXT PRIMARY KEY,
    sqft_per_labor_hour REAL NOT NULL CHECK (sqft_per_labor_hour > 0),
    effective_date TEXT NOT NULL,
    assumption_version TEXT NOT NULL,
    source_note TEXT NOT NULL
);

CREATE TABLE job_feasibility_summary (
    job_id TEXT PRIMARY KEY REFERENCES jobs(job_id),
    job_name TEXT NOT NULL,
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    job_type TEXT NOT NULL,
    project_phase TEXT NOT NULL,
    scenario_date TEXT NOT NULL,
    planned_start_date TEXT NOT NULL,
    area_sqft REAL NOT NULL,
    quoted_price REAL NOT NULL,
    estimated_material_cost REAL NOT NULL,
    estimated_labor_hours REAL NOT NULL,
    estimated_labor_cost REAL NOT NULL,
    estimated_equipment_cost REAL NOT NULL,
    estimated_total_cost REAL NOT NULL,
    estimated_margin_pct REAL NOT NULL,
    target_margin_pct REAL NOT NULL,
    margin_gap_pct REAL NOT NULL,
    meets_target_margin TEXT NOT NULL,
    estimated_duration_days REAL NOT NULL,
    site_risk_points INTEGER NOT NULL CHECK (site_risk_points >= 0),
    risk_category TEXT NOT NULL,
    risk_drivers TEXT NOT NULL,
    risk_component_detail TEXT NOT NULL,
    risk_model_version TEXT NOT NULL,
    workability_status TEXT NOT NULL,
    slope_level TEXT NOT NULL,
    access_width_ft REAL NOT NULL,
    drainage_concern TEXT NOT NULL,
    demo_required TEXT NOT NULL,
    carry_distance_ft REAL NOT NULL,
    crew_size INTEGER NOT NULL,
    scope_approved TEXT NOT NULL,
    site_access_verified TEXT NOT NULL,
    utility_locate_status TEXT NOT NULL,
    permit_status TEXT NOT NULL,
    materials_status TEXT NOT NULL,
    crew_assigned TEXT NOT NULL,
    assumption_version TEXT NOT NULL
);

CREATE TABLE actual_job_results (
    job_id TEXT PRIMARY KEY REFERENCES jobs(job_id),
    actual_labor_hours REAL NOT NULL CHECK (actual_labor_hours > 0),
    actual_total_cost REAL NOT NULL CHECK (actual_total_cost >= 0),
    actual_margin_pct REAL NOT NULL,
    cost_variance REAL NOT NULL,
    margin_variance REAL NOT NULL,
    change_order_flag TEXT NOT NULL,
    change_order_cost REAL NOT NULL CHECK (change_order_cost >= 0),
    outcome_note TEXT NOT NULL
);

CREATE TABLE preconstruction_action_log (
    action_id TEXT PRIMARY KEY,
    priority TEXT NOT NULL CHECK (priority IN ('High', 'Medium', 'Low')),
    job_id TEXT NOT NULL REFERENCES jobs(job_id),
    job_name TEXT NOT NULL,
    site TEXT NOT NULL,
    blocker TEXT NOT NULL,
    next_action TEXT NOT NULL,
    responsible_role TEXT NOT NULL,
    assignee TEXT NOT NULL,
    needed_by TEXT NOT NULL,
    status TEXT NOT NULL,
    last_updated TEXT NOT NULL,
    lookahead_bucket TEXT NOT NULL,
    escalation_flag TEXT NOT NULL,
    blocking_flag TEXT NOT NULL,
    project_phase TEXT NOT NULL,
    planned_start_date TEXT NOT NULL,
    constraint_category TEXT NOT NULL,
    reason_code TEXT NOT NULL,
    source_field TEXT NOT NULL
);

CREATE INDEX idx_action_log_lookahead
    ON preconstruction_action_log(status, needed_by, priority);

CREATE VIEW post_job_variance_review AS
SELECT
    s.job_id,
    s.job_name,
    s.state,
    s.city,
    s.job_type,
    s.estimated_total_cost,
    a.actual_total_cost,
    a.cost_variance,
    s.estimated_labor_hours,
    a.actual_labor_hours,
    s.estimated_margin_pct,
    a.actual_margin_pct,
    a.margin_variance,
    a.change_order_flag,
    a.change_order_cost,
    s.site_risk_points,
    s.risk_drivers
FROM job_feasibility_summary AS s
JOIN actual_job_results AS a USING (job_id);
