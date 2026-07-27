# Source audit

Paper: arXiv `2605.00473v1`. The source archive was retrieved on 2026-07-24
with an explicit browser User-Agent and has SHA-256
`1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f`.
Verbatim anchors are preserved in `repro/source/main_result_anchors.tex`.

- Claim 3: Corollary 5.3, source lines 55–65, quantifies over tasks \(t\in[T]\)
  under all Theorem 5.1 assumptions and states a probability of at least
  \(1-\widetilde\delta-C_2e^{-C_3k}\). The displayed population loss is
  \(\sigma^2dk/(NT)\). The following paragraph states the likelihood-method
  comparison \(dk^2/(NT)\).
- Claim 4: the discussion following Theorem 5.1 states
  \(\widetilde O(1)\) iterations. The actual theorem conditions are
  \(\eta_1\lesssim1/(\kappa^5\sigma_1)\),
  \(K_1\gtrsim1/(\eta_1\sigma_k)\), and
  \(\eta_2\lesssim1/\sigma_1\), with a \(K_1/2\) contraction exponent.
  Dimension independence is therefore assessed at fixed \(\kappa\) and
  normalized steps, not across changing condition number.
- Claim 5: Equation (6) assumes
  \(N\gtrsim\sigma^2(d+T)k\kappa^4/\sigma_k^2(\Sigma^*)\).
  The hidden constant and logarithmic suppression are not numerically stated.

The exact-RIP construction has \(\delta=0\), every cell has \(T>k\), and the
realized spectrum, balance residual, and condition number are audited in the
raw outputs. Finite experiments do not replace the universal proof.
