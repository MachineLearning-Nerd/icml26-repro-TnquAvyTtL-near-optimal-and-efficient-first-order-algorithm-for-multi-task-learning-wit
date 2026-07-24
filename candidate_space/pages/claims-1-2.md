# Claims 1–2 — faithful TPGD structure

Status: **VERIFIED**

Exact contract: TPGD jointly updates \(B\) and \(W\) for exactly \(K_1\)
iterations. The first half follows Equation (1); the second half follows
Equation (5), including
\(\|B^\top B-WW^\top\|_F^2/8\).

The run used `repro/src/faithful_tpgd.py` and
`repro/src/claim12_verifier.py`. Evaluator-visible copies are
[the implementation](../evidence/claims-1-2/faithful_tpgd.py) and
[the standalone verifier](../evidence/claims-1-2/verify_claim12.py). The exact
fixed cumulative command is:

```text
uv run python repro/src/verify.py
```

## Observed evidence

The immutable run used commit
`9f277437f7f73e73d4d91f6a38ec917c34994841`, seeds `1201` and `1202`, and
Figure 1(a) dimensions `d=100,k=10,T=100,N=100`. Its exact phase sequence was
`I, I, II, II`. Correction-gradient norms were `0, 0, 0.00165144,
0.00165141`, so the regularizer was absent in Phase I and active in Phase II.

| Independent derivative check | B relative error | W relative error | Limit |
|---|---:|---:|---:|
| Equation (1), unregularized | 8.51e-10 | 4.85e-10 | 2e-7 |
| Equation (5), regularized | 1.01e-9 | 7.60e-10 | 2e-7 |

The factor-two full-correction control produced relative errors `0.02057` and
`0.01745`, both far above its `0.001` rejection threshold. The off-by-one
control produced `I, II, II, II` and was also rejected.

The verifier took 2.1379 seconds with one numerical thread on the local CPU
(eight host logical CPUs were visible; process affinity was unavailable).
Dependencies are pinned by `.python-version`, `pyproject.toml`, and `uv.lock`.

Download [raw result](../evidence/claims-1-2/result.json),
[independent checker output](../evidence/claims-1-2/checker.json), and
[negative controls](../evidence/claims-1-2/controls.json).

## Exact scope and limitations

Claims 1–2 describe algorithm identity, so this is direct structural evidence
at a paper-scale dimensional configuration. The four-step horizon does **not**
test Claim 4 convergence. Gaussian inputs only instantiate valid shapes. The
implementation follows displayed Equation (5)'s `1/8` coefficient; an older
commented arXiv source block has a factor-two-different update, which is
disclosed and tested above.
