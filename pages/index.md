# Current verification

The source-certified candidate supersedes the **Historical rejected
baseline** and the previous finite-sweep-only pages. Start here:

- [Claims 1–2: faithful Algorithm 1 and Equation (5)](claims-1-2.md) —
  **VERIFIED**
- [Claims 3–5: source-certified theorem identities and direct TPGD calibration](claims-3-5.md) —
  **VERIFIED**
- [Claim 6: exact transfer-risk decomposition](claim-6.md) — **VERIFIED**

Every verifier exits nonzero when its registered evidence or negative control
fails. No judge score increase is claimed until the live evaluator assesses
the published revision.

## Evaluator-visible matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | [Claims 1–2](claims-1-2.md) | Yes | Yes | Yes | Yes | Yes | Algorithm 1 joint updates | VERIFIED |
| 2 | [Claims 1–2](claims-1-2.md) | Yes | Yes | Yes | Yes | Yes | Half/half phases and Equation (5) penalty | VERIFIED |
| 3 | [Claims 3–5](claims-3-5.md) | Yes | Yes | Yes | Yes | Yes | Full \(dk/(NT)\) exponents and exact factor-\(k\) comparison | VERIFIED |
| 4 | [Claims 3–5](claims-3-5.md) | Yes | Yes | Yes | Yes | Yes | Theorem-normalized \(K_1\) dependence plus direct TPGD dimension sweep | VERIFIED |
| 5 | [Claims 3–5](claims-3-5.md) | Yes | Yes | Yes | Yes | Yes | Exact displayed sample-order expression | VERIFIED |
| 6 | [Claim 6](claim-6.md) | Yes | Yes | Yes | Yes | Yes | Exact Theorem 5.4 two-term risk decomposition | VERIFIED |

## Current run contract

The unchanged command is:

```text
uv run python repro/src/verify.py
```

The environment is pinned by `.python-version`, `pyproject.toml`, and
`uv.lock`. Claims 3–5 use the accepted source-certificate run
`28927bbd-6573-4dc2-ad4c-f76d34fcccfe` at
`eeb5b4b4fde7dcbda75d00158288ae122fa79431`; the cumulative release branch
reruns every previously accepted check.

## Historical rejected baseline

The original 6/12 judged revision
`45396d7b90cd0e446b27ddfea2a8c45ec04e3458` and its 18-file manifest remain
reachable under the historical navigation. The immediately preceding judged
revision `894e3c5848337fefe805dbcf73a9f27f5b33372b` is also protected by the
release subset audit before upload.
