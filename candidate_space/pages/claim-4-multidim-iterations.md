# Claim 4 — direct TPGD iteration independence

Status: **VERIFIED** under the registered finite exact-RIP contract.
Confidence: **MEDIUM**.

The previous 7/12 page varied only \(d\). The current
[direct TPGD verifier](../repro/src/direct_multidim_tpgd.py) varies all four
problem dimensions \(d,k,T,N\) over four values with six seeds each, while
holding condition number, normalized step choices, target, and exact-RIP
construction fixed.

## Exact source interpretation

Theorem 5.1 requires
\(\eta_1\lesssim1/(\kappa^5\sigma_1)\),
\(K_1\gtrsim1/(\eta_1\sigma_k)\), and
\(\eta_2\lesssim1/\sigma_1\), with a Phase-II exponent \(K_1/2\).
At fixed \(\kappa\), these settings contain no polynomial \(d,k,T,N\)
dependence; initialization contributes only suppressed logarithms. The
[source audit](../.openresearch/artifacts/claims-3-5/direct-current/source_audit.md)
therefore registers the empirical test at fixed \(\kappa=1\).

## First-hit result

Success means first reaching relative squared parameter error `0.05` within
600 total TPGD iterations. Every one of the 96 runs hit the target.

| Varied factor | Values | Median first-hit iterations | Log-log slope | Max/min median | Gate |
|---|---|---|---:|---:|---|
| \(d\) | 128, 256, 512, 1024 | 141, 168, 164, 175.5 | `+0.0913` | `1.245` | PASS |
| \(k\) | 2, 4, 6, 8 | 161, 164, 161.5, 188.5 | `+0.0852` | `1.171` | PASS |
| \(T\) | 8, 16, 32, 64 | 160.5, 164, 168.5, 176.5 | `+0.0450` | `1.100` | PASS |
| \(N\) | 200, 400, 800, 1600 | 164.5, 164.5, 164, 164 | `−0.0018` | `1.003` | PASS |

The registered limits were absolute slope at most `0.25`, median ratio at
most `2`, and six of six successes in every cell. A cyclic task-response
permutation fails the shared-parameter target as intended; this rules out a
verifier that passes without using the correct task correspondence.

## Reproduce and inspect

```text
uv run python repro/src/verify.py
```

Accepted HF `cpu-upgrade` run:
`44fb4f8f-3ee0-4739-bdfd-46f6ab195f4f`; Git:
`1aa33107943e838d5d09f80baa614383c5b828cc`; ORX wall time:
3m59s; module time: 8.898s; estimated cores: 8; container logical CPUs: 64;
numerical thread cap: 8; seeds: `8301–8306`.

Download the [96 raw iteration rows](../.openresearch/artifacts/claims-3-5/direct-current/claim4_iteration_rows.csv),
[complete result](../.openresearch/artifacts/claims-3-5/direct-current/direct_multidim_tpgd.json),
[checker](../.openresearch/artifacts/claims-3-5/direct-current/independent_checker_output.json),
[control](../.openresearch/artifacts/claims-3-5/direct-current/negative_control_output.json),
[configuration](../repro/src/direct_multidim_config.py), and
[evaluation checklist](../.openresearch/artifacts/claims-3-5/direct-current/EVAL.md).
The verifier raises and the fixed command exits nonzero if any factor,
assumption, checker, or control gate fails.

Finite first-hit measurements corroborate, but do not formally prove, a
dimension-uniform asymptotic theorem.
