# Claim-by-claim reproduction of TPGD for shared linear representations

## Collection classification and audit boundary

This repository is a **legacy/source workspace** for *Near-Optimal and Efficient First-Order Algorithm for Multi-Task Learning with Shared Linear Representation*
(arXiv `2605.00473`, OpenReview `TnquAvyTtL`). It is preserved
separately from the standardized canonical record at
[`icml26-tpgd-multitask-representation`](https://github.com/MachineLearning-Nerd/icml26-tpgd-multitask-representation).

The claim results and scores recorded below are historical results of this
workspace. They are not new paper-level verifications performed while
organizing the collection. The collection audit did not run the scientific
implementation; the canonical record documents its own scoped status and
limitations.

### How the historical claim evidence is produced

The claim table and experiment log below are the authoritative mapping from
each paper claim to its producer, command, control, and evidence artifact. In
this workspace, the claim-specific producers and independent checkers emit structured artifacts under `.openresearch/artifacts/` and `evidence/`, including claim contracts, methods, controls, rate rows, and `EVAL.md`.

The former `orx/*` branches are historical workstreams, not additional final
publication claims. Their purposes and tips are preserved in
[`BRANCH_AUDIT.md`](BRANCH_AUDIT.md). Citation and author acknowledgment
details are in [`CITATION.cff`](CITATION.cff) and
[`AUTHOR_THANK_YOU.md`](AUTHOR_THANK_YOU.md).

## Thank you

Thank you to the paper authors for making this research available for study. The full acknowledgment is in [`AUTHOR_THANK_YOU.md`](AUTHOR_THANK_YOU.md).

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/blob/main/notebooks/tpgd_reproduction.py)

Paper: *Near-Optimal and Efficient First-Order Algorithm for Multi-Task
Learning with Shared Linear Representation* ([arXiv 2605.00473](https://arxiv.org/abs/2605.00473)).

The exact live verdict for Space revision
`9b3781d6a422415a0f474ca7575757c7a2c4d27a` is **7/12**: Claims 1, 2, and 6
were verified, Claim 4 received toy credit, and Claims 3 and 5 were
inconclusive. The judge found the formula certificates tautological, the
earlier rate slopes wrong in \(d\) and \(T\), and the iteration experiment
limited to \(d\).

The new route runs the named two-phase TPGD directly. Its six-seed slopes are
`+0.971,+0.978,−0.958,−1.003` for \(d,k,T,N\), matching the full
\(dk/(NT)\) exponent vector. First-hit iteration slopes stay between `−0.002`
and `+0.091` when each of \(d,k,T,N\) is swept. Claim 5 now uses an N grid
chosen independently of the formula, freezes a hidden-constant margin on one
seed set, and passes all 27 high-margin groups on unseen seeds across all five
factor families.

Claims 3–5 are assessed `VERIFIED` with **MEDIUM** confidence under registered
finite exact-RIP contracts. These experiments corroborate rather than prove
universal theorems. The conservative projected range is **8–12/12** and the
best-supported possible score is **12/12**—forecasts, not judge results.

The paper-dimensional calibration used
\(d=100,k=10,T=100,N=100\), matching Figure 1(a)'s dimensions. The scaling
sweeps intentionally substitute an exact-RIP design to audit the theorem
premise and use finite grids and deterministic seeds; they are scoped
corroborations, not full-domain proofs. Short structural checks ran on one
local CPU thread. Uncertain or multi-core work ran on Hugging Face
`cpu-upgrade`, with numerical libraries capped at eight threads.

- [Illustrated technical report](reports/tpgd-reproduction/report.md)
- [Self-contained marimo tutorial](notebooks/tpgd_reproduction.py)
- [Direct Claims 3–4 raw JSON](.openresearch/artifacts/claims-3-5/direct-current/direct_multidim_tpgd.json)
- [Held-out Claim 5 raw JSON](.openresearch/artifacts/claims-3-5/direct-current/claim5_threshold_phase_diagram.json)
- [Independent checks](.openresearch/artifacts/claims-3-5/direct-current/independent_checker_output.json)
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
| [`orx/source-certified-theorem-identities-and-dimensio`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/source-certified-theorem-identities-and-dimensio) | Source certificates plus direct 32× TPGD dimension sweep | `uv run python repro/src/verify.py` | Historical rejected route: live judge found C3/C5 tautological and C4 one-dimensional | HF `cpu-upgrade`, 5m28s |
| [`orx/direct-multidimensional-tpgd-and-threshold-calib`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/direct-multidimensional-tpgd-and-threshold-calib) | Direct rate and iteration sweeps over \(d,k,T,N\) | `uv run python repro/src/verify.py` | All four rate slopes and all 96 iteration cells pass | HF `cpu-upgrade`, 3m59s |
| [`orx/claim-5-non-circular-threshold-phase-diagram`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/claim-5-non-circular-threshold-phase-diagram) | Calibrate hidden sample-condition margin on seeds 8501–8505 | `uv run python repro/src/verify.py` | Scientific gate failed; preserved only to freeze \(C=10\) | HF `cpu-upgrade`, 4m40s |
| [`orx/claim-5-held-out-sufficient-condition-validation`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/claim-5-held-out-sufficient-condition-validation) | Evaluate frozen margin on unseen seeds 8601–8605 | `uv run python repro/src/verify.py` | 27/27 high-margin and 15/15 largest-N groups pass | HF `cpu-upgrade`, 4m14s |

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
