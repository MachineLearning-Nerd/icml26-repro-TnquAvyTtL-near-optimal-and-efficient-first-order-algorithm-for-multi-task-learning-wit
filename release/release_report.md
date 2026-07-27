- Previous live judged score: `7/12`
- Conservative projected score range after the proposed change: `8–12/12`
- Best-supported possible new score, forecast rather than judge result: `12/12`

# Pre-publication release report

The exact live verdict is for Space
`DineshAI/TnquAvyTtL@9b3781d6a422415a0f474ca7575757c7a2c4d27a`,
judged 2026-07-27 05:37 UTC. It awards Claims 1 and 2 two points each,
Claim 4 one toy point, Claim 6 two points, and Claims 3 and 5 zero points.
The campaign began at 6/12; the current release baseline is therefore 7/12.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 2 | 2 | HIGH | VERIFIED | Faithful joint \(B,W\) updates, finite-difference derivative checks, and two failing controls; live judge accepted. |
| 2 | 2 | 2 | HIGH | VERIFIED | Exact half/half phase trace and Equation (5) balance penalty; factor-two and off-by-one mutations rejected; live judge accepted. |
| 3 | 0 | 2 | MEDIUM | VERIFIED | Direct TPGD slopes `+0.971,+0.978,−0.958,−1.003` for \(d,k,T,N\), tight bootstrap intervals, assumptions, checker, and task-permutation control. Risk: finite exact-RIP scope does not prove the universal theorem. |
| 4 | 1 | 2 | MEDIUM | VERIFIED | Direct first-hit distributions across all \(d,k,T,N\): every one of 96 runs hits; slopes lie in `[−0.002,+0.091]`. Risk: finite horizons cannot prove all dimension sequences. |
| 5 | 0 | 2 | MEDIUM | VERIFIED | Independent N grid, immutable calibration, disjoint held-out seeds, 27/27 high-margin and 15/15 largest-N groups successful across all factor families. Risk: hidden constant is empirical and the condition is not shown necessary or tight. |
| 6 | 2 | 2 | HIGH | VERIFIED | Exact population-risk decomposition, separately varied resource slopes, independent checker, and projection control; live judge accepted. |

Current total score: **7/12**. Conservative projected total score after
publication: **8–12/12**. Best-supported possible total score: **12/12**.
These are forecasts; only the live judge can change the score.

Claims 3, 4, and 5 changed materially. Claim 3 no longer relies on a spectral
proxy or source identity; Claim 4 varies all four dimensions instead of only
\(d\); Claim 5 now performs calibrated then held-out direct TPGD validation.
No claim is marked `BLOCKED`. Claims 3–5 retain `MEDIUM` confidence because
their finite exact-RIP scope leaves theorem-level generalization risk.

## Informational upload summary

| Claim | Status | Expected points | Confidence | Expected evaluator status |
|---|---|---:|---|---|
| 1 | VERIFIED | 2 | HIGH | Previously accepted direct verifier remains current |
| 2 | VERIFIED | 2 | HIGH | Previously accepted direct verifier remains current |
| 3 | VERIFIED | 2 | MEDIUM | Direct four-factor TPGD slope verifier located |
| 4 | VERIFIED | 2 | MEDIUM | Direct four-factor first-hit verifier located |
| 5 | VERIFIED | 2 | MEDIUM | Held-out sufficient-condition verifier located |
| 6 | VERIFIED | 2 | HIGH | Previously accepted decomposition verifier remains current |

Conservative projected total: **8–12/12**. Best-supported possible score:
**12/12**. Remaining risk is evaluator interpretation of finite exact-RIP
evidence for asymptotic theorems, especially Claim 5’s hidden constant.

## Experiment tree and winning evidence

The stacked tree descends from the immutable 7/12 release candidate through:

1. `orx/direct-multidimensional-tpgd-and-threshold-calib` —
   Git `1aa33107943e838d5d09f80baa614383c5b828cc`, accepted run
   `44fb4f8f-3ee0-4739-bdfd-46f6ab195f4f`;
2. `orx/claim-5-non-circular-threshold-phase-diagram` —
   Git `5bc1702b3480dffedf676a0e052d0d9ea5a9ac53`, failed scientific calibration
   run `200bd469-e6d7-484b-9571-d9503ef82f35`; and
3. `orx/claim-5-held-out-sufficient-condition-validation` —
   winning scientific Git `963ddf47b5e0e5ee0f59dbd14552e414b2931f26`, accepted held-out run
   `5aaa91cb-c2aa-47f3-b1e4-d9342b475db0`.

The failed branch is retained because it explains how \(C=10\) was frozen
before the held-out seed set. It is not presented as accepted evidence.

## Evidence and compute

The fixed command throughout is:

```text
uv run python repro/src/verify.py
```

The environment is pinned by `.python-version`, `pyproject.toml`, and
`uv.lock`. Both accepted runs estimated eight cores and therefore used HF
`cpu-upgrade`; each container exposed 64 logical CPUs with process affinity
64 and a numerical thread cap of 8. Claims 3–4 took 3m59s ORX wall time
(8.898s for the new module); Claim 5 held-out validation took 4m14s
(30.152s for the new module). The HF interface exposed no monetary cost, so
none is invented.

Current evidence is under
`.openresearch/artifacts/claims-3-5/direct-current/`: contracts, source audit,
method, limitations, 792 raw seed-level rows, two full JSON outputs,
independent checker, negative controls, seeds, SHAs, CPU, and runtime.

## Release gates

- Every claim has an explicit `VERIFIED` verdict and calibrated confidence.
- Previously accepted Claims 1, 2, and 6 remain in the cumulative verifier.
- Every criticism in the exact 7/12 verdict is answered on a current page.
- Raw results regenerate from the unchanged fixed command.
- All registered negative controls fail for their intended reasons.
- Finite evidence is labeled finite; no toy result is called full-scale proof.
- The exact 110-file 7/12 judged tree is the candidate base and remains a subset.
- The original 6/12 historical text snapshot remains byte-identical.
- The preceding 7/12 README, index, logbook, and rejected page are preserved byte-identically.
- `logbook.json` validates and direct current pages appear before historical pages.
- The exact text-only upload allowlist contains 121 paths with a SHA-256 manifest.
- Secret scanning reports no findings.
- Blind traversal from `README.md` and `pages/index.md` reaches code, inline data, raw output, checkers, controls, and limitations with no broken links.
- The blind review is recorded and will be repeated after the final cumulative run.

## Exact publication action

After the final cumulative HF run passes, upload only the 121 allowlisted text
paths in `release/upload_allowlist.tsv` to the existing Space
`DineshAI/TnquAvyTtL` using the Hugging Face commit API. Do not create a new
Space and do not delete files. Then download the returned revision, verify
every uploaded hash and canonical traversal, mirror reader-facing artifacts
to GitHub `main`, confirm the remote SHA with `git ls-remote`, and mark the
paper awaiting the live judge.
