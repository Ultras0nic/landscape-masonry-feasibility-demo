# Methodology and Assumptions

## Scope

The estimator supports paver patios and walkways. Retaining walls are intentionally excluded because a credible wall estimate needs height, face area, excavation, drainage aggregate, cap, reinforcement, bearing conditions, and possible engineering review.

## Synthetic inputs

The generator uses fixed seeds and an as-of date of 2026-07-15. Rate tables carry an effective date, version, and explicit synthetic-source note. They are not vendor quotes or market benchmarks.

## Estimate logic

The calculation includes pavers with waste, base gravel, bedding sand, edging, disposal when demolition is required, labor hours adjusted for site conditions, and equipment days. The logic is simplified for portfolio demonstration.

## Site-risk points

Rules add points for access, slope, drainage, demolition, carry distance, job size, and crew-size mismatch. The total is stored as `site_risk_points`; drivers and individual point contributions are retained. The points are not probabilities and are not calibrated on historical construction jobs.

Review labels are:

- `No Additional Review Flagged`
- `Review Before Approval`
- `Site Review Required`

Commercial margin rules and hard readiness gates are evaluated separately.

## Synthetic closeout outcomes

Labor productivity, material variance, and change events are simulated separately. Scenario factors influence these outcomes by design. Estimate-versus-actual patterns therefore demonstrate a feedback workflow and must not be described as discovered causal or predictive relationships.

## Validation

`scripts/validate_outputs.py` checks IDs, joins, nonnegative values, formula reconciliation, scenario coverage, priority coverage, foreign-key-compatible records, and absence of post-job fields in the preconstruction action log.

