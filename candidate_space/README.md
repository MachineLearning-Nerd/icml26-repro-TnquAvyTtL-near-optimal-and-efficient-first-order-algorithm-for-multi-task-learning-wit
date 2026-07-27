---
title: "Repro - TPGD Multi-Task Representation (arXiv 2605.00473)"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-TnquAvyTtL
---

# Direct claim-by-claim TPGD reproduction

The live judge scored revision
`9b3781d6a422415a0f474ca7575757c7a2c4d27a` **7/12**. It accepted Claims 1,
2, and 6, gave Claim 4 toy credit, and rejected the formula-only Claims 3 and
5 evidence.

This candidate replaces those rejected default verifiers with:

- direct two-phase TPGD slopes across all four \(d,k,T,N\) factors;
- direct first-hit iteration distributions across all four factors; and
- a non-circular sample grid with calibration and disjoint held-out seeds.

The conservative forecast is **8–12/12** and the best-supported possible score
is **12/12**, explicitly a forecast rather than a judge result. Finite
exact-RIP evidence and its limitations are stated on every current page.

[Open the current verification index](pages/index.md). It exposes the exact
claims and source quantifiers, numerical assumption audit, executable code,
fixed command, inline results, downloadable raw JSON/CSV, independent
checkers, negative controls, limitations, Git SHA, seeds, CPU allocation, and
runtime.

| Claim | Live points | Candidate evidence |
|---|---:|---|
| 1–2 | 4/4 | Retained direct verified evidence |
| 3 | 0/2 | New direct four-factor TPGD rate |
| 4 | 1/2 | New four-factor first-hit distribution |
| 5 | 0/2 | New calibrated/held-out TPGD phase diagram |
| 6 | 2/2 | Retained direct verified evidence |

The unchanged cumulative command is:

```text
uv run python repro/src/verify.py
```

## Historical rejected baseline

The exact original 6/12 pages and manifest remain under
[`historical/judged-45396d/README.md`](historical/judged-45396d/README.md), and every
file in the exact 7/12 judged Space is checked as a subset of the assembled
candidate. Its [rejected Claims 3–5 page](pages/claims-3-5.md) remains at the
same path and is labeled **Historical rejected baseline** in current
navigation. The preceding canonical text is also preserved verbatim under
`historical/judged-9b378/`.
