# Limitations and deviations

- This evidence verifies Claims 1–2 as statements about algorithm structure.
  It does not use a four-step trace to claim convergence, statistical
  optimality, or dimension-independent iteration complexity.
- The smoke run uses the dimensions displayed in Figure 1(a), but not its full
  training horizon. Full convergence is evaluated separately.
- Gaussian covariates are used only to provide deterministic valid inputs.
- The implementation follows displayed Equation (5)'s coefficient \(1/8\).
  The arXiv source's older commented full-correction update is a disclosed
  factor-two inconsistency and is explicitly rejected by the derivative
  checker.
- `process_affinity_cpus` was unavailable on this platform. Numerical library
  thread variables were all fixed to one before NumPy import.
