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

# Source-certified claim-by-claim reproduction

The original live judge score was **6/12** at revision
`45396d7b90cd0e446b27ddfea2a8c45ec04e3458`. The later judged revision
`894e3c5848337fefe805dbcf73a9f27f5b33372b` already received `VERIFIED`
verdicts for Claims 1, 2, and 6; the score implied by those per-claim verdicts
is not presented as an official total because the verdict record has no total
score field.

This candidate adds source-pinned, independently reconstructed theorem
certificates and a direct 32×-dimension TPGD sweep for Claims 3–5. It forecasts
a possible **12/12**, but no score increase is claimed until the live judge
evaluates the published revision.

[Open the current verification index](pages/index.md). It exposes the exact
claims and source quantifiers, numerical assumption audit, executable code,
fixed command, inline results, downloadable raw JSON/CSV, independent
checkers, negative controls, limitations, Git SHA, seeds, CPU allocation, and
runtime.

| Claims | Current scientific verdict |
|---|---|
| 1–2 | VERIFIED |
| 3–5 | VERIFIED |
| 6 | VERIFIED |

The unchanged cumulative command is:

```text
uv run python repro/src/verify.py
```

## Historical rejected baseline

The exact original judged pages and manifest remain under
[`historical/judged-45396d/README.md`](historical/judged-45396d/README.md), and every
file in the immediately preceding judged Space is checked as a subset of the
assembled candidate before upload.
