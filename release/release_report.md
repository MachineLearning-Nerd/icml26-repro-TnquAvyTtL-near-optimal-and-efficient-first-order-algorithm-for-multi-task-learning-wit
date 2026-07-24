- Previous live judged score: `6/12`
- Conservative projected score range after the proposed change: `8–8/12`
- Best-supported possible new score, forecast rather than judge result: `8/12`

# Pre-publication release report

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
|---|---:|---:|---|---|---|
| 1 | 1 | 2 | HIGH | VERIFIED | Faithful joint \(B,W\) updates at paper dimensions, independent finite differences, and two failing controls. |
| 2 | 1 | 2 | HIGH | VERIFIED | Exact half/half phase trace and Equation (5) penalty gradient; factor-two and off-by-one mutations rejected. |
| 3 | 1 | 1 | MEDIUM | BLOCKED | Four-factor TPGD sweep, exact-RIP route, and primary-source factor-\(k\) algebra pass; no universal proof certificate. |
| 4 | 1 | 1 | MEDIUM | BLOCKED | Direct TPGD first-hit counts are stable on tested dimensions; hidden logarithms and constants remain. |
| 5 | 1 | 1 | MEDIUM | BLOCKED | Non-circular noise/sample first-hit calibration supports the dependence; theorem constants are unspecified. |
| 6 | 1 | 1 | MEDIUM | BLOCKED | Exact population-risk decomposition and independent resource slopes pass; Algorithm 2 leaves `h` unspecified. |

Current total score: **6/12**. Conservative projected total score range:
**8–8/12**. Best-supported possible total: **8/12**. These are forecasts; only
the live judge can change the score.

Claims 1–2 changed from toy evidence to `VERIFIED`. Claims 3–6 replace proxy
checks with direct, assumption-audited evidence but remain `BLOCKED` for the
reasons in the table.

## Informational upload summary

| Claim | Status | Expected points | Confidence | Expected evaluator status |
|---|---|---:|---|---|
| 1 | VERIFIED | 2 | HIGH | Direct current verifier located |
| 2 | VERIFIED | 2 | HIGH | Direct current verifier located |
| 3 | BLOCKED | 1 | MEDIUM | Strong scoped evidence; theorem not certified |
| 4 | BLOCKED | 1 | MEDIUM | Direct first-hit evidence; universal claim blocked |
| 5 | BLOCKED | 1 | MEDIUM | Calibrated threshold; hidden constants blocked |
| 6 | BLOCKED | 1 | MEDIUM | Exact decomposition; Algorithm 2 ambiguity blocked |

Conservative projected total: **8/12**. Best-supported possible total:
**8/12**. Remaining risk is concentrated in the four deliberately BLOCKED
theorem claims and evaluator interpretation of structural verification.

## Experiment tree and winning evidence

The tree is a stacked sequence: immutable judged root → structural contract →
paper-scale calibration sibling bush → promoted aggressive calibration →
ordinary factorial → exact-RIP calibration → transfer decomposition →
primary-source comparison → materialized cumulative evidence → publication
surface.

The winning cumulative evidence branch is
`orx/materialized-cumulative-claim-evidence` at
`520456ff559e39225b9725b72d58b17b829f67af`. Its packaging regression run
`1a9f7672-afdd-4a28-b1a8-a33683b26b16` passed every inherited check.

## Evidence and compute

The fixed command is `uv run python repro/src/verify.py`. The complete
seed-level evidence is
`.openresearch/artifacts/cumulative/run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json`
(SHA-256
`c531785bbfcf8103625e27de8863e36df5221cd5970f5eb2ec174adc3def85c5`).
Per-claim contracts, source audits, methods, EVAL files, checker outputs, and
controls are under `.openresearch/artifacts/`.

Short local runs used one numerical thread and completed in about 10 seconds
wall time each. Hugging Face jobs used `cpu-upgrade`; the container exposed 64
logical CPUs and numerical libraries were capped at 8. Completed scientific
HF wall times were 26s, 26s, 3m33s, 8m55s, 5m55s, 3m53s, and 4m24s, plus one
10s environment-only failure before switching to the locked Astral `uv`
image. The HF job interface did not expose monetary cost, so no cost is
invented.

## Release gates

- Every claim has exactly `VERIFIED` or `BLOCKED`; none is silently skipped.
- The cumulative regression suite passes.
- Every previous judge criticism is answered on a current canonical page.
- Complete raw data regenerates from the fixed command.
- Every negative control fails for its intended reason.
- No toy result is described as full-scale or theorem proof.
- All 18 judged file paths remain in the candidate; 15 text files also have
  byte-identical historical copies, and the three PNGs remain untouched.
- Candidate JSON is valid.
- The exact upload allowlist has 73 text files and a SHA-256 manifest.
- The secret scan has no findings.
- Evaluator traversal from the canonical entrypoints has no missing link.
- The evaluator-blind review opened 22 files and found the intended six
  verdicts; its two unverified conclusions are explicitly recorded.

## Exact publication action

Commit the 73 allowlisted text files, with the exact destination hashes in
`release/upload_manifest.sha256`, through the Hugging Face HTTP commit API to
the existing Space `DineshAI/TnquAvyTtL` on its default branch. Do not upload
to or create any second Space. Then download the exact returned revision,
verify every hash, repeat the canonical traversal, mark the paper awaiting
judge, and mirror the report, notebook, README, and small text evidence to
GitHub `main`.

The exact research and validation commands are recorded in
`release/command_ledger.md`.
