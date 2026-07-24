# Claims 1–2 — faithful TPGD structure

Status: **pending immutable OpenResearch run**

Exact contract: TPGD jointly updates \(B\) and \(W\) for exactly \(K_1\)
iterations. The first half follows Equation (1); the second half follows
Equation (5), including
\(\|B^\top B-WW^\top\|_F^2/8\).

The executable source is `repro/src/faithful_tpgd.py`; the independent checker
is `repro/src/claim12_verifier.py`; and the fixed command is:

```text
uv run python repro/src/verify.py
```

The checker uses central finite differences, runs a structural trace at the
Figure 1(a) dimensions `d=100,k=10,T=100,N=100`, and requires two negative
controls to fail for the intended reasons. It exits nonzero if any acceptance
condition fails.

Raw values, CPU allocation, runtime, commit SHA, and immutable checker output
will be placed inline after the OpenResearch run. Until then this page makes no
positive verdict.
