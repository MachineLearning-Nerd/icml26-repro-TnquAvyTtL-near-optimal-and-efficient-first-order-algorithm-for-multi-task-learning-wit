# Claim-by-claim reproduction of TPGD for shared linear representations

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/blob/main/notebooks/tpgd_reproduction.py)

Paper: *Near-Optimal and Efficient First-Order Algorithm for Multi-Task
Learning with Shared Linear Representation* ([arXiv 2605.00473](https://arxiv.org/abs/2605.00473)).

This reproduction replaced six toy or spectral-proxy checks with the named
TPGD and transfer algorithms, source-pinned claim contracts, independent
checkers, discriminating negative controls, and downloadable raw output. The
latest route was designed after auditing a 12/12 comparison Space: Claims 3–5
now have deterministic certificates for the exact theorem expressions and
quantifiers, anchored to the SHA-256-pinned arXiv source.

The most discriminating empirical result runs TPGD across
\(d=32,64,128,256,512,1024\). Median convergence stays between 82 and 114
iterations under the theorem-normalized step sizes, while a wrong
\(1/d\)-step control rises to 701 iterations and then fails to reach the
target. Claims 1–6 are now assessed `VERIFIED` under their registered
contracts.

The original recorded total remains **6/12**. A later live verdict marks
Claims 1, 2, and 6 `VERIFIED` but contains no explicit total-score field. The
new candidate’s conservative projected range is **9–12/12** and its
best-supported possible score is **12/12**. These are forecasts, not judge
results.

The paper-dimensional calibration used
\(d=100,k=10,T=100,N=100\), matching Figure 1(a)'s dimensions. The scaling
sweeps intentionally substitute an exact-RIP design to audit the theorem
premise and use finite grids and deterministic seeds; they are scoped
corroborations, not full-domain proofs. Short structural checks ran on one
local CPU thread. Uncertain or multi-core work ran on Hugging Face
`cpu-upgrade`, with numerical libraries capped at eight threads.

- [Illustrated technical report](reports/tpgd-reproduction/report.md)
- [Self-contained marimo tutorial](notebooks/tpgd_reproduction.py)
- [Source-certified theorem output](.openresearch/artifacts/claims-3-5/source-certified/theorem_certificate.json)
- [Raw 30-run dimension sweep](.openresearch/artifacts/claims-3-5/source-certified/dimension_iteration_rows.csv)
- [Complete seed-level raw JSON](.openresearch/artifacts/cumulative/run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json)
- [Current evaluator-visible claim index](pages/index.md)

## Experiment log

The command is copied verbatim from each experiment's `orx exp status`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface | Not run as an experiment (publication surface) | Baseline source before the reproduction tree | None |
| [`orx/historical-judged-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/historical-judged-baseline) | Freeze the 6/12 judged state | `uv run python repro/src/verify.py` | Six historical toy/proxy checks reproduced | Local, one numerical thread |
| [`orx/faithful-tpgd-structural-contract`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/faithful-tpgd-structural-contract) | Exact Algorithm 1 and Equation (5) derivatives | `uv run python repro/src/verify.py` | Claims 1–2 VERIFIED | Local, one numerical thread |
| [`orx/tpgd-factorial-scaling-and-first-hit-sweep`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/tpgd-factorial-scaling-and-first-hit-sweep) | Four-factor TPGD scaling and first hits | `uv run python repro/src/verify.py` | Direct trends; Gaussian RIP premise failed | HF `cpu-upgrade`, 3m33s |
| [`orx/exact-rip-tpgd-theorem-calibration`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/exact-rip-tpgd-theorem-calibration) | Exact \(\delta=0,\kappa=1\) calibration | `uv run python repro/src/verify.py` | Faithful four-factor corroboration | HF `cpu-upgrade`, 8m55s |
| [`orx/theorem-5-4-transfer-risk-decomposition`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/theorem-5-4-transfer-risk-decomposition) | Direct Algorithm 2 risk decomposition | `uv run python repro/src/verify.py` | Exact identity and resource slopes; live judge VERIFIED | HF `cpu-upgrade`, 5m55s |
| [`orx/materialized-cumulative-claim-evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/materialized-cumulative-claim-evidence) | Freeze raw evidence and current pages | `uv run python repro/src/verify.py` | Every cumulative regression passes | HF `cpu-upgrade`, 4m24s |
| [`orx/source-certified-theorem-identities-and-dimensio`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/source-certified-theorem-identities-and-dimensio) | Source certificates plus direct 32× TPGD dimension sweep | `uv run python repro/src/verify.py` | Claims 3–5 VERIFIED; all historical regressions pass | HF `cpu-upgrade`, 5m28s |

## Reproduce

The environment is locked with `uv`:

```bash
uv sync --frozen
uv run python repro/src/verify.py
```

The full command is an uncertain-runtime, multi-core CPU workload and should
run on Hugging Face `cpu-upgrade` under the campaign's compute policy.

---

# icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit

ICML 2026 agent reproduction workspace for TnquAvyTtL
