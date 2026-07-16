# Responsible AI Extension

The current project is transparent, deterministic analytics. AI is not needed for cost calculation or approval decisions.

A bounded future feature could turn a short field note into a **draft** structured observation. For example, a note about a narrow gate and uncertain demolition scope could draft `access_width`, `demolition_scope`, `uncertainty`, and clarification questions.

Required safeguards:

- Preserve the original note and require human confirmation.
- Extract only supported fields; never invent measurements or conditions.
- Send uncertain cases to `Needs clarification`.
- Never approve feasibility, alter a quote, schedule work, or make engineering, code, or safety decisions.
- Remove customer names, addresses, and sensitive project data before any external API use.
- Evaluate missing fields, unsupported claims, and human correction rate before deployment.

A later estimator feature could retrieve similar completed synthetic cases for explanation, but it should not be called cost prediction without sufficient real historical data and out-of-sample validation.

