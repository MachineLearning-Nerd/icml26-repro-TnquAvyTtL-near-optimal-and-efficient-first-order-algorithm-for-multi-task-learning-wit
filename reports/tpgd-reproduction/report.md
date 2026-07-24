# Direct TPGD evidence strengthens the reproduction—but four theorem claims remain blocked

![Exact-RIP TPGD scaling exponents](images/headline_slopes.png)

The strongest result is also the clearest limit of this campaign. On an
exact-RIP, condition-number-one construction, faithful TPGD recovers the
paper's \(1/N\) and linear-in-\(k\) error exponents. The finite \(T\) and \(d\)
sweeps move in the claimed directions but have substantially smaller
magnitudes. These experiments replace the previous spectral proxies, yet they
do not prove the paper's universal high-probability theorems.

## The question

The paper studies multi-task linear regression where task vectors share a
rank-\(k\) representation \(B^*\). It claims that a two-phase first-order
method, TPGD, reaches population parameter error
\(\widetilde O(dk/(NT))\), converges in \(\widetilde O(1)\) iterations, obeys a
specific sample-order condition, and yields a two-term transfer-risk bound.

The live judged artifact received 6/12 because every claim was supported only
by a toy or proxy check. This campaign asked a stricter question: which claims
can be marked `VERIFIED` under machine-checkable contracts, and which must
remain `BLOCKED` despite stronger numerical evidence?

## Implementation: the paper's two-phase update

The implementation jointly updates \(B\in\mathbb R^{d\times k}\) and
\(W\in\mathbb R^{k\times T}\). The first half of \(K_1\) follows the
unregularized likelihood gradient. The second half adds the gradient of

\[
\frac18\|B^\top B-WW^\top\|_F^2.
\]

Central finite differences agree with the implementation at relative errors
below \(1.1\times10^{-9}\). A factor-two correction mutation and an
off-by-one phase switch are both rejected. This directly verifies the
algorithm identity and phase contract in Claims 1–2.

![TPGD calibration trajectory](images/tpgd_trajectory.png)

At the paper's Figure 1(a) dimensions \(d=100,k=10,T=100,N=100\), parameter
error falls from 9.542 to 0.002301 over 650 iterations. The balance residual
collapses after the phase switch. This is a calibration result, not evidence
that 650 is universally dimension-independent.

## Exact-RIP route: removing an assumption failure

The first factorial experiment used ordinary finite Gaussian designs. It
produced useful trends, but its realized RIP constants were all larger than
one, so it did not satisfy Theorem 5.1's premise.

The stronger route sets \(X_t=\sqrt N[P_t;0]\) with signed permutation
\(P_t\). Then \(X_t^\top X_t/N=I\) exactly and \(\delta=0\). A balanced truth
matrix makes every nonzero singular value equal to \(\sqrt{T/k}\), hence
\(\kappa=1\). Explicit-design and sufficient-statistic gradients agree to
\(1.67\times10^{-16}\); deleting one design direction yields \(\delta=1\) and
is rejected.

Across 70 five-seed fits, the observed slopes were:

| Varied factor | Observed slope | Bootstrap 95% interval | Claimed direction |
|---|---:|---:|---:|
| \(N\) | -1.001 | [-1.008, -0.994] | -1 |
| \(k\) | +0.972 | [+0.942, +1.003] | +1 |
| \(T\) | -0.610 | [-0.650, -0.575] | -1 |
| \(d\) | +0.421 | [+0.379, +0.460] | +1 |

The factor-\(k\) literature comparison was checked separately rather than
inferred from these slopes. Primary-source formulas from Tripuraneni et al.
and Thekumparampil et al. reduce to \(dk^2/(NT)\) under the paper's notation;
their quotient by \(dk/(NT)\) is exactly \(k\). This verifies the comparison
arithmetic, not Theorem 5.1 itself.

## Sample complexity without circular sample selection

![Independent sample threshold](images/sample_threshold.png)

The operational target—parameter error below 0.1 for at least four of five
seeds—and the sample grid were committed before outcomes. First hits occur at
\(N=100,300,600\) for noise standard deviations \(0.5,1.0,1.5\). Only after
measuring those hits was the paper's sample expression evaluated. The
observed-threshold versus expression log slope is 0.813.

This is calibrated support for the formula's dependence, but the theorem
contains hidden constants and an initialization condition with unspecified
comparison constants. Claim 5 therefore remains `BLOCKED`.

## Transfer: an exact decomposition, not a universal bound

![Transfer-risk decomposition](images/transfer_decomposition.png)

For Gaussian target covariates, \(H=I\) and Assumption 3.3 has the analytic
certificate
\(E[xx^\top Mxx^\top]=2M+\mathrm{tr}(M)I\preceq3\mathrm{tr}(M)I\).
Across 128 rows, the population Pythagorean decomposition closes to
\(1.96\times10^{-16}\). Its representation component scales as
\(N^{-1.022}\), while its optimization component scales as
\(K_2^{-1.091}\). Replacing the projection anchor by zero leaves a gap of
2.904 and is rejected.

The paper does not instantiate Algorithm 2's required `h`, and its prose and
pseudocode disagree at a step-size boundary. The experiment commits `h=0`
and follows the pseudocode, so Claim 6 remains `BLOCKED`.

## Claim-by-claim assessment

| Claim | Result | Why |
|---|---|---|
| 1 | VERIFIED | Joint \(B,W\) updates and two-phase execution are directly checked. |
| 2 | VERIFIED | Equation (5)'s penalty gradient, phase boundary, and controls pass. |
| 3 | BLOCKED | Faithful four-factor evidence and factor-\(k\) algebra pass; the universal theorem lacks a proof certificate. |
| 4 | BLOCKED | First-hit counts are stable on tested grids; hidden logarithms/constants prevent universal verification. |
| 5 | BLOCKED | Independent threshold calibration supports the dependence; unspecified constants remain. |
| 6 | BLOCKED | Exact risk decomposition and independent scaling pass; Algorithm 2 is underspecified and finite trials are not proof. |

The conservative and best-supported publication forecast is an improvement
from the current 6/12 to 8/12, upgrading only the two rigorously verified
structural claims. This is not a judge result. The live judge alone can change
the score.

## Reproducibility and provenance

The fixed command for every node is:

```text
uv run python repro/src/verify.py
```

The accepted scientific run is
`6661bf06-a416-4eeb-a5be-b446970ca8ad` at Git SHA
`e582fbea5cbce995dcd084eced463e142890721d`. It ran on Hugging Face
`cpu-upgrade`; eight cores were estimated, 64 logical CPUs were visible, and
numerical libraries were capped at eight threads. Wall runtime was 3m53s and
verifier runtime was 204.456s. The locked environment uses Python 3.12.12,
NumPy 2.2.6, and the repository's `uv.lock`.

The [complete seed-level raw JSON](../../.openresearch/artifacts/cumulative/run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json)
has SHA-256
`c531785bbfcf8103625e27de8863e36df5221cd5970f5eb2ec174adc3def85c5`.
The cumulative packaging regression is on branch
[`orx/materialized-cumulative-claim-evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-TnquAvyTtL-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-wit/tree/orx/materialized-cumulative-claim-evidence);
the exact-RIP route and transfer route are its ancestors in the recorded
OpenResearch tree.
