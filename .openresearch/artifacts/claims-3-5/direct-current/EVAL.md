# Evaluator checklist

- Verdicts: Claims 3, 4, and 5 `VERIFIED` under the registered finite,
  assumption-satisfying contracts; confidence `MEDIUM`.
- Fixed command: `uv run python repro/src/verify.py`.
- Pinned environment: `.python-version`, `pyproject.toml`, `uv.lock`.
- Direct code: `repro/src/direct_multidim_tpgd.py` and
  `repro/src/claim5_threshold_phase_diagram.py`.
- Configurations: `repro/src/direct_multidim_config.py` and
  `repro/src/claim5_threshold_config.py`.
- Raw JSON and CSV: this directory.
- Independent checker and controls: `independent_checker_output.json` and
  `negative_control_output.json`.
- Assumptions, exact source, quantifiers, deviations, seeds, SHA, CPU, and
  runtime: `source_audit.md`, `limitations.md`, and `run_metadata.json`.
- Both verifiers raise an exception and the cumulative command exits nonzero
  if any registered gate or negative control fails.
