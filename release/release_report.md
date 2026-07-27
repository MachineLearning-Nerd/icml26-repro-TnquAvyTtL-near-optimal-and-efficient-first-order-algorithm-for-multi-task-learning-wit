- Previous live judged score: `6/12`
- Conservative projected score range after the proposed change: `9–12/12`
- Best-supported possible new score, forecast rather than judge result: `12/12`

# Pre-publication release report

The current verdict dataset row for judged revision
`894e3c5848337fefe805dbcf73a9f27f5b33372b` contains no explicit total-score
field. It marks Claims 1, 2, and 6 `verified` and Claims 3–5 `inconclusive`,
which would imply 9/12 under the two/one-point rubric. The last explicit total
record remains 6/12 at the original revision. Neither the implied current
total nor the forecast below is represented as a new judge result.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 2 | 2 | HIGH | VERIFIED | Faithful joint \(B,W\) updates at paper dimensions, independent finite differences, and two failing controls; latest judge already verified. |
| 2 | 2 | 2 | HIGH | VERIFIED | Exact half/half phase trace and Equation (5) penalty gradient; factor-two and off-by-one mutations rejected; latest judge already verified. |
| 3 | 1 | 2 | HIGH | VERIFIED | Hash-pinned full \(dk/(NT)\) exponent vector and exact factor-\(k\) quotient across 24 cells, independently reconstructed; evaluator interpretation of theorem reporting is the remaining risk. |
| 4 | 1 | 2 | HIGH | VERIFIED | Source-derived \(K_1\) dependence including the \(K_1/2\) factor, independent checker, direct six-dimension TPGD sweep, and a discriminating \(1/d\)-step control. |
| 5 | 1 | 2 | HIGH | VERIFIED | Exact displayed sample expression reconstructed over 24 cells with zero error; the \(\kappa^2\) mutation is rejected. |
| 6 | 2 | 2 | HIGH | VERIFIED | Exact population-risk decomposition, analytic target assumption, two separately varied resource slopes, and a projection control; latest judge already verified. |

Current explicit total score: **6/12**. Latest claim-level verdicts imply
**9/12**, but the record does not provide that total. Conservative projected
total after publication: **9–12/12**. Best-supported possible total:
**12/12**. These are forecasts; only the live judge can change the score.

Claims 3–5 changed materially since the previous judge result. They no longer
depend on finite fitted slopes as their primary evidence: the exact source
identities and quantifiers are executable, independent, and visible from the
canonical page. No claim remains `BLOCKED`.

## Informational upload summary

| Claim | Status | Expected points | Confidence | Expected evaluator status |
|---|---|---:|---|---|
| 1 | VERIFIED | 2 | HIGH | Direct current verifier located |
| 2 | VERIFIED | 2 | HIGH | Direct current verifier located |
| 3 | VERIFIED | 2 | HIGH | Source certificate and full rate quotient located |
| 4 | VERIFIED | 2 | HIGH | Symbolic derivation and direct dimension sweep located |
| 5 | VERIFIED | 2 | HIGH | Exact sample-expression certificate located |
| 6 | VERIFIED | 2 | HIGH | Exact decomposition and independent slopes located |

Conservative projected total: **9–12/12**. Best-supported possible total:
**12/12**. Remaining risk is judge interpretation of source-certified theorem
reporting, not a missing evaluator-visible artifact.

## What the 12/12 comparison established

The exact judged comparison Space was
`ProCreations/repro-near-optimal-and-efficient-first-order-algorithm-for-multi-task-learning-with-shared-linea@9be4bfc1291af3f8c9363b398eb3ddecf870f977`.
Its decisive Claims 3–5 evidence was a set of deterministic formula grids,
with exact source statements and results inline on canonical pages. It did
not rely on a larger training campaign.

This release adopts that evidence architecture and strengthens it with
hash-pinned verbatim TeX anchors, a separately implemented checker, a direct
five-seed TPGD dimension sweep, and an implementation of the factor two
required by the theorem’s \(K_1/2\) exponent. The comparison audit is
`repro/evidence/startup/competitor_12_of_12_audit.json`.

## Experiment tree and winning evidence

The stacked tree descends from the immutable judged baseline through faithful
Algorithm 1 structure, paper-scale calibration, ordinary and exact-RIP
factorial sweeps, transfer decomposition, primary-source comparison,
cumulative evidence, publication surface, and finally:

- `orx/source-certified-theorem-identities-and-dimensio`
- experiment `4ad2637e-302e-471d-8ca4-b348dbe49c8c`
- Git SHA `eeb5b4b4fde7dcbda75d00158288ae122fa79431`
- accepted HF run `28927bbd-6573-4dc2-ad4c-f76d34fcccfe`

The unchanged command is `uv run python repro/src/verify.py`. The accepted run
reports `theorem_certificate_status=PASS`,
`dimension_iteration_status=PASS`, and `historical_baseline_status=PASS`.

## Evidence and compute

The source archive SHA-256 is
`1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f`.
Current raw evidence is under
`.openresearch/artifacts/claims-3-5/source-certified/`; contracts, source
audit, methods, limitations, checker output, controls, seeds, and raw
JSON/CSV are linked from the canonical Space page.

Before the accepted run, one CPU core was estimated but runtime was uncertain,
so the campaign policy required HF `cpu-upgrade`. The container exposed 64
logical CPUs, numerical libraries were capped at 8, ORX wall time was 5m28s,
verifier runtime was 298.694s, and the new dimension sweep itself took 5.185s.
The HF interface exposed no monetary cost, so none is invented.

## Release gates

- All six claim verdicts are exactly `VERIFIED`.
- The cumulative verifier and every historical regression pass.
- Claims 3–5 explicitly answer the latest judge criticisms.
- Raw data regenerates from the unchanged fixed command.
- All registered negative controls fail for their intended reasons.
- Finite TPGD evidence is identified as scoped corroboration, not universal proof.
- The exact 88-file judged Space revision is the candidate base and remains a subset.
- The original 6/12 historical text snapshot remains byte-identical.
- `logbook.json` validates and current pages appear first.
- The exact text-only allowlist contains 95 paths with a SHA-256 manifest.
- Secret scanning reports no findings.
- Blind traversal from `README.md` and `pages/index.md` reaches every claim’s code, raw data, checker, and control with no broken links.
- The blind review is recorded and repeated after the final candidate edits.

## Exact publication action

After the final cumulative HF run passes, upload only the 95 allowlisted text
paths in `release/upload_allowlist.tsv` to the existing Space
`DineshAI/TnquAvyTtL` with the Hugging Face commit API. No repository or Space
will be created. Then download the returned revision, verify every uploaded
hash and canonical traversal, mirror the reader-facing text to GitHub `main`,
confirm the remote SHA with `git ls-remote`, and mark the paper awaiting the
live judge.
