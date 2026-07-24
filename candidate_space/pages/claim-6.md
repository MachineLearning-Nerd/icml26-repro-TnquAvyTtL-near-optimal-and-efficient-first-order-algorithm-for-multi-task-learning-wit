# Claim 6 — transfer-risk decomposition

Status: **BLOCKED**. Confidence: **MEDIUM**.

This page supersedes the **Historical rejected baseline** single spectral
transfer example. The current route executes the paper's Algorithm 2
pseudocode after learning the representation with TPGD.

Theorem 5.4 bounds target-task excess risk by a representation approximation
term proportional to \(1/N\) plus a task-specific optimization term
proportional to \(1/K_2\). It inherits the upstream assumptions and requires
the target moment condition in Assumption 3.3.

The fixed command is:

```text
uv run python repro/src/verify.py
```

Executable source:
[transfer decomposition verifier](../repro/src/transfer_decomposition.py).

## Assumptions and direct identity

The upstream exact-RIP design has \(\delta=0\) and balanced truth has
\(\kappa=1\). Target covariates are \(x\sim N(0,I)\), so
\(E[xx^\top Mxx^\top]=2M+\mathrm{tr}(M)I\preceq3\mathrm{tr}(M)I\) for every
positive-semidefinite \(M\), certifying Assumption 3.3 with \(\alpha=3\).

For the population loss with \(H=I\), orthogonal projection gives the exact
Pythagorean decomposition:

\[
\tfrac12\|\widehat B w-\theta\|^2
=\tfrac12\|(I-P_{\widehat B})\theta\|^2
+\tfrac12\|\widehat B(w-w_{\rm opt})\|^2.
\]

## Observed evidence

The 128-row factorial sweep used upstream
\(N\in\{100,200,400,800\}\), target
\(K_2\in\{1000,2000,4000,8000\}\), and eight deterministic seeds.

| Component | Observed slope | Bootstrap 95% interval |
|---|---:|---:|
| Representation vs. upstream \(N\) | -1.022 | [-1.100, -0.942] |
| Optimization vs. target \(K_2\) | -1.091 | [-1.306, -0.887] |

The maximum exact decomposition residual is `1.96e-16`. Replacing the
orthogonal projection anchor by zero leaves an identity gap of `2.90413`,
above the `1e-4` rejection threshold, so the negative control fails as
intended.

## Why the verdict is BLOCKED

Algorithm 2 requires input `h`, but Theorem 5.4 does not instantiate it.
The pseudocode and surrounding prose also differ at the first step-size
halving boundary. This route commits `h=0` and follows the pseudocode, one
defensible interpretation. Finite trials cannot certify the theorem's
universal bound, so the exact risk decomposition is corroborated but Claim 6
remains **BLOCKED**.

Download the
[complete seed-level raw JSON](../.openresearch/artifacts/cumulative/run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json),
[checker output](../.openresearch/artifacts/claim-6/independent_checker_output.json),
[negative control](../.openresearch/artifacts/claim-6/negative_control_output.json),
[claim contract](../.openresearch/artifacts/claim-6/claim_contract.json), and
[run metadata](../.openresearch/artifacts/cumulative/run_metadata.json).

The accepted run is `6661bf06-a416-4eeb-a5be-b446970ca8ad`, Git SHA
`e582fbea5cbce995dcd084eced463e142890721d`, on Hugging Face
`cpu-upgrade`; wall runtime was 3m53s with the numerical thread cap set to 8.
