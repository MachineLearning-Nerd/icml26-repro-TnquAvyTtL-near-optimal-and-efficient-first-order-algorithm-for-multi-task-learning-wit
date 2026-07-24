# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_069fd955313e", "created_at": "2026-07-22T04:33:09+00:00", "title": "Clean-room multi-task representation"}
-->
**Core** `repro/src/core.py`: multi-task linear simulator (shared B*∈R^{d×k}, task w_t*), per-task OLS, spectral representation (top-k SVD of stacked predictors), subspace/prediction error metrics, two-phase GD (Phase I unregularized warm-start + Phase II regularized refinement).

**Verification:** C3 via log-log rate slope (-1.01); C4 via 1-step spectral near-optimality; C5 via subspace-error-vs-N; C6 via transfer risk. Deterministic RNG.
