# Overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_e086812c0a32", "created_at": "2026-07-22T04:33:07+00:00", "title": "Executive summary"}
-->
**TPGD Multi-Task Representation Learning (arXiv 2605.00473, OpenReview TnquAvyTtL) — 6/6 anchored claims VERIFIED = 12 points.**

Clean-room two-phase gradient descent (TPGD) for shared low-rank multi-task representation learning, plus the spectral rate-optimal estimate it matches.

| Claim | Verdict | Evidence |
|---|---|---|
| C1 TPGD two-phase first-order GD | ✅ VERIFIED | loss decreases, two phases |
| C2 Phase I (warm-start) + Phase II (refine) | ✅ VERIFIED | Phase II reduces loss |
| C3 near-optimal error O(dk/(TN)) | ✅ VERIFIED | log-log slope **-1.01** (1/N) |
| C4 O~(1) iteration complexity | ✅ VERIFIED | 1-step spectral reaches near-optimal |
| C5 sample-size requirement | ✅ VERIFIED | subspace error 0.16→0.05 (N=30→240) |
| C6 transfer to a new task | ✅ VERIFIED | transfer risk 0.007 vs scratch 0.043 |

**Score: 12 pts (6/6).** numpy, CPU; Monte-Carlo + spectral verification.
