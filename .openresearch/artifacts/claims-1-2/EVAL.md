# Evaluator record: Claims 1–2

Current verdict: **VERIFIED**.

This is a structural verification of exactly the named algorithm, not evidence
for its statistical rates. The dimensional smoke configuration is paper-scale,
but its four-iteration horizon is intentionally short because convergence is
Claim 4. Raw run output, commit SHA, allocated CPU count, and runtime will be
materialized in `raw/claim12_result.json`, `run_metadata.json`,
`independent_checker_output.json`, and `negative_control_output.json`.

Evidence run `be6790eb-dce8-4af4-acc7-390d9b92ceb1` executed commit
`9f277437f7f73e73d4d91f6a38ec917c34994841` using the fixed command
`uv run python repro/src/verify.py`. The current verifier completed in
2.137859417 seconds with its numerical libraries limited to one thread.

Limitations and deviations:

- Gaussian designs are used only to supply valid-shaped inputs.
- No convergence conclusion is drawn.
- The displayed Equation (5) is authoritative for the penalty derivative; the
  factor-two source discrepancy is exposed and tested as a control.
