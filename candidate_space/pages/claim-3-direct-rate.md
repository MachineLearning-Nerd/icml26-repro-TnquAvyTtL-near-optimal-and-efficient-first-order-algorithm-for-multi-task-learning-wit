# Claim 3 — direct TPGD full \(dk/(NT)\) rate

Status: **VERIFIED** under the registered finite exact-RIP contract.
Confidence: **MEDIUM**.

The current verifier supersedes the [Historical rejected 7/12 source-only
certificate](claims-3-5.md). It runs
[TPGD directly](../repro/src/direct_multidim_tpgd.py); no spectral estimator
or formula-generated outcome supplies the result.

## Exact claim and assumptions

Corollary 5.3, under every Theorem 5.1 assumption and \(T>k\), states with
probability at least \(1-\widetilde\delta-C_2e^{-C_3k}\):

\[
\frac1T\sum_{t=1}^T\|\widehat v_t-v_t^*\|^2
\lesssim \frac{\sigma^2dk}{NT}.
\]

The next source paragraph gives the likelihood-method comparison
\(\widetilde O(dk^2/(NT))\), a factor \(k\) larger. The
[source audit](../.openresearch/artifacts/claims-3-5/direct-current/source_audit.md)
records exact anchors and quantifiers. In every experimental cell,
\(\delta=0\), \(T>k\), the truth is balanced, and the spectrum has
\(\kappa=1\); maximum condition-number error is
`8.88e-16` and maximum balance residual is `1.89e-15`.

## Direct four-factor result

Six seeds were run for each value. The final parameter error is measured after
the same two-phase TPGD horizon, then each factor is fit independently. The
strict preregistered tolerance was slope error at most `0.25`.

| Factor | Values | Paper slope | TPGD slope | Seed-bootstrap 95% interval | Gate |
|---|---|---:|---:|---:|---|
| \(d\) | 128, 256, 512, 1024 | +1 | `+0.9707` | `[+0.9486,+0.9952]` | PASS |
| \(k\) | 2, 4, 6, 8 | +1 | `+0.9784` | `[+0.9574,+1.0022]` | PASS |
| \(T\) | 8, 16, 32, 64 | −1 | `−0.9577` | `[−0.9781,−0.9356]` | PASS |
| \(N\) | 200, 400, 800, 1600 | −1 | `−1.0029` | `[−1.0242,−0.9809]` | PASS |

This directly answers the judge’s criticism that the previous page tested
only \(1/N\) or used a spectral proxy. The factor-\(k\) comparison itself is
an exact quotient of the two source rates and is source-audited; the TPGD
\(k\)-sweep above independently recovers the claimed linear dependence.

## Reproduce and inspect

Fixed command:

```text
uv run python repro/src/verify.py
```

The immutable accepted run is
`44fb4f8f-3ee0-4739-bdfd-46f6ab195f4f` at Git
`1aa33107943e838d5d09f80baa614383c5b828cc`. It ran on HF
`cpu-upgrade` in 3m59s; the container exposed 64 logical CPUs and numerical
threads were capped at 8. Seeds are `8301–8306`.

Download the [96 raw rate rows](../.openresearch/artifacts/claims-3-5/direct-current/claim3_rate_rows.csv),
[complete raw JSON](../.openresearch/artifacts/claims-3-5/direct-current/direct_multidim_tpgd.json),
[independent checker](../.openresearch/artifacts/claims-3-5/direct-current/independent_checker_output.json),
[negative controls](../.openresearch/artifacts/claims-3-5/direct-current/negative_control_output.json),
[claim contract](../.openresearch/artifacts/claims-3-5/direct-current/claim_contract.json),
[method](../.openresearch/artifacts/claims-3-5/direct-current/method.md), and
[run metadata](../.openresearch/artifacts/claims-3-5/direct-current/run_metadata.json).
The independent checker differs by at most `6.94e-18`. Cyclically permuting
task response columns yields error `0.4961` against rejection threshold
`0.06633` and fails as intended.

## Limitation

This is rigorous finite, assumption-satisfying corroboration in an exact-RIP
special case, not a formal proof of the universal high-probability theorem.
The base \(d/T=32\) was fixed before outcomes to isolate the leading term.
See all [limitations](../.openresearch/artifacts/claims-3-5/direct-current/limitations.md).
