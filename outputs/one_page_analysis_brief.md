# Decision Brief: Persona-Based Construction Analytics

## Objective

Demonstrate how a small landscape or masonry operation could convert synthetic estimating and site-condition data into different decision views for estimators, project teams, and operations analysts.

## Workflow design

The demo separates four lifecycle stages:

1. **Estimate review:** detailed costs, labor assumptions, target margin, and site-risk points.
2. **Preconstruction readiness:** one open action for each missing gate or site constraint.
3. **Field handoff:** a filtered look-ahead showing what needs attention, the next action, the responsible role, and the needed-by date.
4. **Post-job learning:** estimate-versus-actual review using simulated closeout results.

This separation prevents post-job information from leaking into pre-job decisions.

## Scenario observations

- Narrow access, slope, drainage, demolition, and long carry distance add transparent site-risk points.
- Synthetic quote variation deliberately creates both healthy-margin and below-target-margin jobs so commercial review logic is exercised.
- Missing scope, access, utility, permit, materials, or crew prerequisites become blocking readiness actions regardless of numeric site-risk points.
- Massachusetts scenarios have higher modeled rates because the synthetic assumption tables encode higher MA values. This is not a market-price conclusion.
- Closeout outcomes are generated from separate labor, material, and change-event mechanisms. Any resulting overrun pattern is scenario behavior, not validated prediction.

## Operational use

The field-facing view should default to open actions due now or within seven days:

`Priority | Job | Blocker | Next Action | Responsible Role | Needed By | Status`

The estimator view retains detailed cost and margin assumptions. The post-job view supports retrospective questions such as which assumptions need revision and which change-event reasons repeat.

## Controls and limitations

The pipeline validates unique IDs, estimate reconciliation, scenario coverage, action ownership, and the absence of actual-result fields in the preconstruction log. SQLite enforces keys and basic checks.

All data and rates are synthetic. Site-risk points are illustrative rules, not calibrated probabilities. The MVP covers paver patios and walkways only and does not replace estimating, site inspection, utility locating, permitting, engineering, or safety judgment.
