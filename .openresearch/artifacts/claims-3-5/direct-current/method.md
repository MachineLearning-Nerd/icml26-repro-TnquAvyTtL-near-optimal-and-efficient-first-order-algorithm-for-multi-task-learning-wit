# Method

The verifier executes the paper's two-phase TPGD updates directly on sufficient
statistics from an exact-RIP design. Phase I is unregularized; Phase II includes
the Equation (5) balance penalty. No spectral estimator supplies the reported
outcome.

Claims 3 and 4 use six deterministic seeds and ordinary one-factor grids:
\(d=128,256,512,1024\), \(k=2,4,6,8\), \(T=8,16,32,64\), and
\(N=200,400,800,1600\). Claim 3 fits the final parameter-error slope for every
factor and bootstraps seeds 2,000 times. Claim 4 records the first iteration
that reaches relative squared error 0.05. A cyclic task-column permutation is
the negative control.

Claim 5 uses 15 configurations spanning three levels of each of
\(\sigma^2,d+T,k,\kappa,\sigma_k\), the independently fixed N grid
`32,64,128,256,512,1024,2048,4096`, and five seeds per cell (600 TPGD fits).
The failed calibration run on seeds 8501–8505 observed a maximum first-success
ratio of 10, which was frozen before the held-out seeds 8601–8605 were run.
Success means at least four of five seeds meet the registered Procrustes
factor-distance target. Independent reconstruction recomputes all distances
from serialized state; the task-permutation control must fail.

All CPU work ran via Hugging Face `cpu-upgrade`. The fixed command and pinned
environment are recorded in `run_metadata.json`.
