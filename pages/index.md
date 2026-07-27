# Current direct TPGD verification

The live judge scored the preceding revision `7/12`: Claims 1, 2, and 6 were
verified; Claim 4 received toy credit; Claims 3 and 5 were inconclusive. This
candidate directly addresses those three criticisms:

- [Claims 1–2: faithful Algorithm 1 and Equation (5)](claims-1-2.md) —
  **VERIFIED**, already accepted live
- [Claim 3: direct four-factor \(dk/(NT)\) rate](claim-3-direct-rate.md) —
  **VERIFIED**, confidence **MEDIUM**
- [Claim 4: first-hit iterations across \(d,k,T,N\)](claim-4-multidim-iterations.md) —
  **VERIFIED**, confidence **MEDIUM**
- [Claim 5: calibrated then held-out sufficient-condition test](claim-5-heldout-condition.md) —
  **VERIFIED**, confidence **MEDIUM**
- [Claim 6: exact transfer-risk decomposition](claim-6.md) — **VERIFIED**,
  already accepted live

Every verifier exits nonzero when its registered evidence or negative control
fails. No judge score increase is claimed until the live evaluator assesses
the published revision.

## Evaluator-visible matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | [Claims 1–2](claims-1-2.md) | Yes | Yes | Yes | Yes | Yes | Algorithm 1 joint updates | VERIFIED |
| 2 | [Claims 1–2](claims-1-2.md) | Yes | Yes | Yes | Yes | Yes | Half/half phases and Equation (5) penalty | VERIFIED |
| 3 | [Claim 3](claim-3-direct-rate.md) | Yes | Yes | Yes | Yes | Yes | Direct TPGD slopes for all \(d,k,T,N\) factors | VERIFIED |
| 4 | [Claim 4](claim-4-multidim-iterations.md) | Yes | Yes | Yes | Yes | Yes | Direct TPGD first-hit scaling over \(d,k,T,N\) | VERIFIED |
| 5 | [Claim 5](claim-5-heldout-condition.md) | Yes | Yes | Yes | Yes | Yes | Held-out direct TPGD sufficient-condition stress test | VERIFIED |
| 6 | [Claim 6](claim-6.md) | Yes | Yes | Yes | Yes | Yes | Exact Theorem 5.4 two-term risk decomposition | VERIFIED |

## Current run contract

The unchanged command is:

```text
uv run python repro/src/verify.py
```

The environment is pinned by `.python-version`, `pyproject.toml`, and
`uv.lock`. Claims 3–4 use direct run
`44fb4f8f-3ee0-4739-bdfd-46f6ab195f4f`; Claim 5 uses held-out run
`5aaa91cb-c2aa-47f3-b1e4-d9342b475db0`. The cumulative release branch reruns
every previously accepted check.

## Historical rejected baseline

The [rejected 7/12 Claims 3–5 page](claims-3-5.md) is preserved at its original
path and clearly labeled **Historical rejected baseline**. The exact preceding
README, index, logbook, and rejected page are additionally hash-protected under
`historical/judged-9b378/`. The original 6/12 judged revision
`45396d7b90cd0e446b27ddfea2a8c45ec04e3458` and its 18-file manifest remain
reachable under historical navigation. The complete 110-file tree of judged
revision `9b3781d6a422415a0f474ca7575757c7a2c4d27a` is hash-protected and checked
as a subset of the assembled candidate before upload.
