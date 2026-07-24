# Claims 1–2 verification method

`repro/src/faithful_tpgd.py` implements Algorithm 1 directly. Designs are
stored as `X[T,N,d]`, a transpose-only storage difference from the paper.
The loss remains the paper's task-summed objective normalized by `2N`.

The independent checker in `repro/src/claim12_verifier.py` uses central finite
differences on every entry of small deterministic matrices. It separately
checks the unregularized and regularized objectives. It then executes four
iterations at `d=100,k=10,T=100,N=100`, the dimensional configuration in
Figure 1(a), and audits the exact `I,I,II,II` sequence.

Negative controls are:

1. Replace the half correction implied by Equation (5) with the full
   correction printed in an older commented source block. Finite differences
   must reject it.
2. Move the phase switch one iteration early. The phase contract must reject
   it.

Fixed cumulative command:

```text
uv run python repro/src/verify.py
```

The command also reruns all six historical baseline checks. It exits nonzero if
a current check fails or either negative control unexpectedly passes.
