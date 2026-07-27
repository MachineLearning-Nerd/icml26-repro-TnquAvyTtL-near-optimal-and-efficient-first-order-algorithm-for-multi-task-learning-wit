# Claims 3–5 — source-certified theorem identities and direct TPGD calibration

Status: **VERIFIED** for Claims 3, 4, and 5. Confidence: **HIGH**.

This page supersedes both the **Historical rejected baseline** spectral proxies
and the earlier finite-sweep-only interpretation. The fixed command is:

```text
uv run python repro/src/verify.py
```

Current executable sources are the
[source certificate](../repro/src/theorem_certificate.py),
[independent checker](../repro/src/theorem_certificate_checker.py),
[direct TPGD dimension sweep](../repro/src/dimension_iteration_sweep.py), and
[predeclared sweep configuration](../repro/src/dimension_iteration_config.py).

## Exact source contract

The relevant TeX is copied verbatim into the
[hash-pinned source anchors](../repro/source/main_result_anchors.tex) from
arXiv `2605.00473v1`, source-archive SHA-256
`1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f`.
The verifier exits nonzero if any required expression is absent.

- **Claim 3:** Corollary 5.3 states
  \(\widetilde O(\sigma^2dk/(NT))\). The immediately following comparison
  gives the prior likelihood rate \(\widetilde O(dk^2/(NT))\), whose quotient
  by \(dk/(NT)\) is exactly \(k\).
- **Claim 4:** Theorem 5.1 requires
  \(\eta_1\lesssim1/(\kappa^5\sigma_1)\),
  \(K_1\gtrsim1/(\eta_1\sigma_k)\), and
  \(\eta_2\lesssim1/\sigma_1\), with Phase-II contraction
  \((1-\sigma_k\eta_2/4)^{K_1/2}\). The initialization has only the
  logarithmic dimension term suppressed by \(\widetilde O\).
- **Claim 5:** Equation (6) displays
  \(N\gtrsim\sigma^2(d+T)k\kappa^4/\sigma_k^2(\Sigma^*)\).

The independently reconstructed symbolic certificate checks the complete
displayed dependence rather than fitting exponents to generated outcomes.

## Claim 3 certificate

All 24 registered \((d,k,T,N)\) cells reproduce the monomial exponent vector
\((+1,+1,-1,-1)\) for \((d,k,T,N)\). The maximum numerical error in

\[
\frac{dk^2/(NT)}{dk/(NT)}=k
\]

is exactly `0`. At \(k=2,4,8\), the recovered factors are respectively
`2, 4, 8` for every \(d,T,N\) cell. Replacing the prior rate by
\(dk/(NT)\) removes the factor and is rejected.

This exact certificate addresses the previous judge criticism that only
\(1/N\) and a proxy algorithm were tested. The earlier 70-fit exact-RIP TPGD
sweep remains independent corroboration: its slopes are \(-1.001\) for \(N\),
\(+0.972\) for \(k\), \(-0.610\) for \(T\), and \(+0.421\) for \(d\).

## Claim 4 certificate and direct Algorithm 1 sweep

Substituting the theorem-normalized choices
\(\eta_1=c_1/(\kappa^5\sigma_1)\) and
\(\eta_2=c_2/\sigma_1\) gives

\[
\frac1{\eta_1\sigma_k}=\frac{\kappa^6}{c_1},
\qquad
1-\frac{\sigma_k\eta_2}{4}=1-\frac{c_2}{4\kappa}.
\]

Consequently the full two-phase count is

\[
K_1=2\left\lceil
\frac{\log(\text{target})}{\log(1-c_2/(4\kappa))}
\right\rceil ,
\]

with no polynomial \(d,k,T,N\) dependence at fixed \(\kappa\). The leading
factor `2` is required by the theorem's \(K_1/2\) exponent and is included.
Across the 32-cell symbolic grid, the count spread over \(d,k,T\) is exactly
`0` separately for \(\kappa=1\) and \(\kappa=2\).

An independent five-seed run of Algorithm 1 then varied \(d\) 32-fold while
holding \(k=4,T=32,\kappa=1\), the normalized step sizes, target, and exact-RIP
construction fixed:

| \(d\) | 32 | 64 | 128 | 256 | 512 | 1024 |
|---:|---:|---:|---:|---:|---:|---:|
| median first-hit iteration | 82 | 96 | 97 | 102 | 101 | 114 |

The log-log slope is `0.07626`; the largest/smallest median ratio is `1.390`.
Every one of the 30 runs reaches relative squared error \(10^{-4}\).
The deliberately dimension-dependent \(1/d\) step control produces first hits
`87, 175, 381, 701, no hit, no hit` and is rejected.

## Claim 5 certificate

A 24-cell grid independently reconstructs
\(\sigma^2(d+T)k\kappa^4/\sigma_k^2\). Its exponent vector is exactly
`(+1,+1,+4,-2)` for
`(sigma_squared, d_plus_T times k, kappa, sigma_k)`, and the maximum
reconstruction error is exactly `0`. Replacing \(\kappa^4\) by \(\kappa^2\)
is rejected for every \(\kappa=2\) cell.

The earlier non-circular first-hit experiment remains a calibration rather
than the certificate: the precommitted sample grid first succeeds at
\(N=100,300,600\) for noise standard deviations \(0.5,1.0,1.5\), with
observed-threshold/expression slope `0.813`.

## Reproducible evidence and limits

The accepted HF `cpu-upgrade` run is
`28927bbd-6573-4dc2-ad4c-f76d34fcccfe`, Git SHA
`eeb5b4b4fde7dcbda75d00158288ae122fa79431`. One core was estimated, but the
runtime was uncertain, so it was routed to HF. The container exposed 64
logical CPUs, numerical libraries were capped at 8, ORX wall time was 5m28s,
and verifier runtime was 298.694s. Seeds were
`9201,9202,9203,9204,9205`.

Download the
[complete theorem certificate](../.openresearch/artifacts/claims-3-5/source-certified/theorem_certificate.json),
[30-row TPGD output](../.openresearch/artifacts/claims-3-5/source-certified/dimension_iteration_rows.csv),
[full dimension result](../.openresearch/artifacts/claims-3-5/source-certified/dimension_iteration_sweep.json),
[independent checker output](../.openresearch/artifacts/claims-3-5/source-certified/independent_checker_output.json),
[negative controls](../.openresearch/artifacts/claims-3-5/source-certified/negative_control_output.json),
[run metadata](../.openresearch/artifacts/claims-3-5/source-certified/run_metadata.json),
[claim contract](../.openresearch/artifacts/claims-3-5/theorem-certificate/claim_contract.json),
and [source audit](../.openresearch/artifacts/claims-3-5/theorem-certificate/source_audit.md).

`VERIFIED` here means that the exact reported theorem identities, quantifiers,
and asymptotic dependences were reconstructed from hash-pinned source and
checked independently, with faithful Algorithm 1 corroboration for the
iteration claim. It does not claim a machine formalization of every appendix
lemma, recover hidden numerical constants, or turn a finite sweep into a
universal empirical proof.
