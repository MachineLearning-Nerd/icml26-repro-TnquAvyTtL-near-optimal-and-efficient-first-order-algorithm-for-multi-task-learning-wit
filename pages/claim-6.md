# Claim 6 — transfer-risk decomposition

Status: **VERIFIED**. Confidence: **HIGH**.

This page supersedes the **Historical rejected baseline** single spectral
transfer example. The current route executes the paper's Algorithm 2 after
learning the representation with TPGD and independently checks the exact
population-risk decomposition named in the claim.

The fixed command is:

```text
uv run python repro/src/verify.py
```

Executable source:
[transfer decomposition verifier](../repro/src/transfer_decomposition.py).

## Exact contract and assumptions

Theorem 5.4 decomposes target excess risk into a representation approximation
term controlled by upstream \(N\) and a target optimization term controlled by
\(K_2\). The upstream exact-RIP design has \(\delta=0\), balanced truth has
\(\kappa=1\), and target covariates are \(x\sim N(0,I)\). Therefore

\[
E[xx^\top Mxx^\top]=2M+\operatorname{tr}(M)I
\preceq3\operatorname{tr}(M)I
\]

for every positive-semidefinite \(M\), certifying Assumption 3.3 with
\(\alpha=3\).

For the population loss with \(H=I\), orthogonal projection gives the exact
Pythagorean identity

\[
\tfrac12\|\widehat B w-\theta\|^2
=\tfrac12\|(I-P_{\widehat B})\theta\|^2
+\tfrac12\|\widehat B(w-w_{\rm opt})\|^2.
\]

The first right-hand term is the representation approximation error and the
second is the task-specific optimization error.

## Observed and independently checked evidence

The 128-row factorial sweep used upstream
\(N\in\{100,200,400,800\}\), target
\(K_2\in\{1000,2000,4000,8000\}\), and eight deterministic seeds.

| Component | Observed slope | Bootstrap 95% interval | Theorem dependence |
|---|---:|---:|---:|
| Representation vs. upstream \(N\) | -1.022 | [-1.100, -0.942] | -1 |
| Optimization vs. target \(K_2\) | -1.091 | [-1.306, -0.887] | -1 |

The maximum exact decomposition residual is `1.96e-16`. Replacing the
orthogonal projection anchor by zero leaves an identity gap of `2.90413`,
above the `1e-4` rejection threshold, so the negative control fails for the
intended reason.

Download the
[complete seed-level raw JSON](../.openresearch/artifacts/cumulative/run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json),
[current independent checker output](../.openresearch/artifacts/claim-6/current/independent_checker_output.json),
[negative control](../.openresearch/artifacts/claim-6/negative_control_output.json),
[current claim contract](../.openresearch/artifacts/claim-6/current/claim_contract.json), and
[current source audit](../.openresearch/artifacts/claim-6/current/source_audit.md).

The accepted decomposition run is
`6661bf06-a416-4eeb-a5be-b446970ca8ad`, Git SHA
`e582fbea5cbce995dcd084eced463e142890721d`, on HF `cpu-upgrade`. Numerical
libraries were capped at 8 threads; ORX wall time was 3m53s and verifier
runtime was 204.456s.

Algorithm 2 requires an input `h` that Theorem 5.4 does not instantiate, and
the prose and pseudocode differ at the first step-size-halving boundary. The
registered route discloses `h=0` and follows the pseudocode. This ambiguity
affects one implementation convention, not the independently verified
two-term population-risk identity and its separately varied resource
dependences.
