# Claim 5 — held-out sample-condition validation

Status: **VERIFIED** as a finite sufficient-condition stress test.
Confidence: **MEDIUM**.

The old page merely reconstructed the formula it was given. This verifier
instead runs [direct two-phase TPGD](../repro/src/claim5_threshold_phase_diagram.py)
600 times on an N grid selected independently of the formula, freezes the
hidden-constant margin on one seed set, and evaluates it on a disjoint seed
set.

## Exact claim and non-circular design

Theorem 5.1 assumes

\[
N\gtrsim
\frac{\sigma^2(d+T)k\kappa^4}{\sigma_k^2(\Sigma^*)}.
\]

The experiment fixed \(N\in\{32,64,128,256,512,1024,2048,4096\}\) before
computing this expression. An immutable calibration run on seeds
`8501–8505` failed its original gate; its maximum observed first-success
ratio was used only to freeze a conservative margin \(C=10\). The current
accepted run uses unseen seeds `8601–8605`. Full details are in the
[contract](../.openresearch/artifacts/claims-3-5/direct-current/claim_contract.json)
and [method](../.openresearch/artifacts/claims-3-5/direct-current/method.md).

## Held-out result

Fifteen configurations independently vary three levels of each factor family
\(\sigma^2,d+T,k,\kappa,\sigma_k\). Success requires at least four of five
seeds to meet the registered Procrustes factor-distance target.

| Registered held-out gate | Observed | Result |
|---|---:|---|
| Groups with \(N/\text{expression}\ge10\) | 27/27 succeed | PASS |
| Factor families represented above margin | all 5 | PASS |
| Largest-N configuration groups | 15/15 succeed | PASS |
| Low-ratio groups \(N/\text{expression}\le0.25\) | 13, with failures | PASS |
| \(\sigma^2\) threshold slope | `1.000` vs `1` | PASS |
| \(d+T\) threshold slope | `1.019` vs `1` | PASS |
| \(k\) threshold slope | `0.960` vs `1` | PASS |
| \(\sigma_k\) empirical direction | `−1.006` | PASS |
| Independent checker maximum difference | `3.55e-15` | PASS |
| Task-permutation control | distance `8.095`, fails | PASS |

All exact-RIP, \(T>k\), realized-spectrum, condition-number, and held-out
separation audits pass.

## The important limitation is visible

The empirical *necessary-transition* slopes for \(\kappa\) and \(\sigma_k\)
are `−0.463` and `−1.006`, not the conservative sufficient-condition
exponents `+4` and `−2`. This does not contradict a sufficient upper
condition, and those slopes are not used as pass gates. It does mean this
experiment does **not** claim the theorem’s expression is necessary, tight,
or numerically constant-free. The hidden constant \(C=10\) is reported rather
than concealed.

## Reproduce and inspect

```text
uv run python repro/src/verify.py
```

Held-out HF `cpu-upgrade` run:
`5aaa91cb-c2aa-47f3-b1e4-d9342b475db0`; Git:
`963ddf47b5e0e5ee0f59dbd14552e414b2931f26`; ORX wall time:
4m14s; module time: 30.152s; estimated cores: 8; container logical CPUs: 64;
numerical thread cap: 8. Calibration run:
`200bd469-e6d7-484b-9571-d9503ef82f35`.

Download the [600 raw rows](../.openresearch/artifacts/claims-3-5/direct-current/claim5_phase_diagram_rows.csv),
[full result JSON](../.openresearch/artifacts/claims-3-5/direct-current/claim5_threshold_phase_diagram.json),
[checker](../.openresearch/artifacts/claims-3-5/direct-current/independent_checker_output.json),
[negative control](../.openresearch/artifacts/claims-3-5/direct-current/negative_control_output.json),
[run metadata](../.openresearch/artifacts/claims-3-5/direct-current/run_metadata.json),
[source audit](../.openresearch/artifacts/claims-3-5/direct-current/source_audit.md),
and [limitations](../.openresearch/artifacts/claims-3-5/direct-current/limitations.md).
The verifier exits nonzero if any held-out gate fails.
