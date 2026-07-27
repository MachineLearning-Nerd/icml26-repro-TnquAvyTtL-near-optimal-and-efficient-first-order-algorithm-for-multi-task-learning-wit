# Claim 6 evaluation

Verdict: **VERIFIED**. Confidence: **HIGH**.

The direct Algorithm 2 experiment uses an exact-RIP, balanced upstream model
and Gaussian target covariates satisfying Assumption 3.3 with \(\alpha=3\).
Across 128 rows, the analytic population-risk decomposition closes to at most
\(1.96\times10^{-16}\). Representation and optimization components decrease
with separately varied \(N\) and \(K_2\), respectively. The zero-anchor
negative control leaves a gap of 2.90413 and is rejected.

The exact two-term identity and both independently varied resource
dependences are therefore verified. Theorem 5.4 does not specify Algorithm
2's required input `h`, and the prose and pseudocode differ at a step-size
boundary; the registered implementation discloses `h=0` and follows the
pseudocode. This is retained as a limitation rather than hidden.

The complete raw output is
`../cumulative/run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json`.
