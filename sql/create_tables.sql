DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS material_prices;
DROP TABLE IF EXISTS labor_rates;
DROP TABLE IF EXISTS production_rates;
DROP TABLE IF EXISTS job_feasibility_summary;
DROP TABLE IF EXISTS actual_job_results;

CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    state TEXT,
    city TEXT,
    job_type TEXT,
    area_sqft REAL,
    perimeter_ft REAL,
    base_depth_in REAL,
    sand_depth_in REAL,
    slope_level TEXT,
    access_width_ft REAL,
    drainage_concern TEXT,
    demo_required TEXT,
    carry_distance_ft REAL,
    crew_size INTEGER,
    quoted_price REAL,
    target_margin_pct REAL
);

CREATE TABLE material_prices (
    state TEXT,
    material_type TEXT,
    unit TEXT,
    unit_cost REAL
);

CREATE TABLE labor_rates (
    state TEXT,
    labor_cost_per_hour REAL
);

CREATE TABLE production_rates (
    job_type TEXT,
    sqft_per_labor_hour REAL
);

CREATE TABLE job_feasibility_summary (
    job_id TEXT PRIMARY KEY,
    state TEXT,
    city TEXT,
    job_type TEXT,
    area_sqft REAL,
    quoted_price REAL,
    estimated_material_cost REAL,
    estimated_labor_hours REAL,
    estimated_labor_cost REAL,
    estimated_equipment_cost REAL,
    estimated_total_cost REAL,
    estimated_margin_pct REAL,
    estimated_duration_days REAL,
    risk_score REAL,
    risk_category TEXT,
    workability_status TEXT,
    slope_level TEXT,
    access_width_ft REAL,
    drainage_concern TEXT,
    demo_required TEXT,
    carry_distance_ft REAL,
    crew_size INTEGER,
    target_margin_pct REAL
);

CREATE TABLE actual_job_results (
    job_id TEXT PRIMARY KEY,
    actual_labor_hours REAL,
    actual_total_cost REAL,
    actual_margin_pct REAL,
    cost_variance REAL,
    margin_variance REAL,
    change_order_flag TEXT
);