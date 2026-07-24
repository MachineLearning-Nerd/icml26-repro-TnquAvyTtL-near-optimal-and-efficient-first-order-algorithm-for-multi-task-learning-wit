# Claims 3–5 — direct TPGD theorem calibration

Status: **BLOCKED** for Claims 3, 4, and 5. Confidence: **MEDIUM**.

These pages supersede the **Historical rejected baseline** spectral proxies.
The current checks run Algorithm 1 itself, using the fixed command:

```text
uv run python repro/src/verify.py
```

Executable sources are
[the ordinary-design factorial verifier](../repro/src/factorial_sweep.py),
[the exact-RIP verifier](../repro/src/exact_rip_sweep.py), and
[the rate-comparison checker](../repro/src/rate_comparison_audit.py).

## Exact contracts

- **Claim 3:** Theorem 5.1 and Corollary 5.3 assert population parameter error
  \(\widetilde O(\sigma^2dk/(NT))\), under their displayed assumptions, and
  compare it with cited \(\widetilde O(dk^2/(NT))\) rates.
- **Claim 4:** for constant condition number, the claimed iteration count is
  \(\widetilde O(1)\), meaning dimension-independent apart from hidden
  logarithmic factors and theorem constants.
- **Claim 5:** the displayed sufficient per-task sample order is
  \(\sigma^2(d+T)k\kappa^4/\sigma_k^2(\Sigma^*)\).

The source anchors are Theorem 5.1, Corollary 5.3, and their surrounding
Section 5.1 discussion in arXiv 2605.00473. The source tar SHA-256 is
`1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f`.

## Assumption-satisfying route

For every task, \(X=\sqrt N[P;0]\), where \(P\) is a signed permutation.
Therefore \(X^\top X/N=I\) and the exact RIP constant is \(\delta=0\).
The balanced ground truth has all nonzero singular values
\(\sqrt{T/k}\), hence \(\kappa=1\). An explicit-matrix gradient reconstruction
agrees with the sufficient-statistic implementation to
`1.67e-16`. Deleting one design direction gives \(\delta=1\), and the
certificate rejects that control.

## Observed evidence

Five-seed independent sweeps produced these log-log slopes:

| Varied factor | Observed slope | Bootstrap 95% interval | Paper direction |
|---|---:|---:|---:|
| \(N\) | -1.001 | [-1.008, -0.994] | -1 |
| \(k\) | +0.972 | [+0.942, +1.003] | +1 |
| \(T\) | -0.610 | [-0.650, -0.575] | -1 |
| \(d\) | +0.421 | [+0.379, +0.460] | +1 |

The \(N\) and \(k\) exponents align closely; the finite \(T\) and \(d\)
exponents have the claimed direction but not unit magnitude. All predeclared
groups reached the independent relative-error first-hit target, with medians
of 175–200 iterations.

For the sample threshold, the first grid values with at least four of five
seeds below error 0.1 were:

| Noise standard deviation | First successful \(N\) |
|---:|---:|
| 0.5 | 100 |
| 1.0 | 300 |
| 1.5 | 600 |

The log slope of observed threshold versus the theorem expression was 0.813.
The grid and target were committed before outcomes; no theorem-derived sample
count was used to choose the first hit.

Two primary-source rates were independently audited. Tripuraneni et al.
Theorem 1 gives \(dr^2/n_1\), and Thekumparampil et al. Remark 2 gives a
prediction term proportional to \(dr^2/(mt)\). With \(r=k\) and total source
samples \(n_1=mt=NT\), both become \(dk^2/(NT)\); division by \(dk/(NT)\)
is exactly \(k\). Mutating the prior rate to \(dk/(NT)\) eliminates the
factor and is rejected.

## Why the verdict is BLOCKED

These are substantial, assumption-audited corroborations, not a proof of a
universally quantified high-probability theorem. The initialization condition
and \(\widetilde O\) notation contain unspecified constants, and no
machine-checkable proof certificate is available. Claim 3's algebraic
comparison subclaim is verified, but Claims 3–5 remain **BLOCKED** overall.

Download the
[complete seed-level raw JSON](../.openresearch/artifacts/cumulative/run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json),
[checker output](../.openresearch/artifacts/claims-3-5/independent_checker_output.json),
[negative controls](../.openresearch/artifacts/claims-3-5/negative_control_output.json),
and [run metadata](../.openresearch/artifacts/cumulative/run_metadata.json).

The accepted run is `6661bf06-a416-4eeb-a5be-b446970ca8ad`, Git SHA
`e582fbea5cbce995dcd084eced463e142890721d`, on Hugging Face
`cpu-upgrade`. Eight cores were estimated; 64 logical CPUs were visible and
numerical libraries were capped at 8. Wall runtime was 3m53s and verifier
runtime was 204.456s.
