# Claims 1–2 source audit

Source: arXiv 2605.00473, retrieved from
`https://ar5iv.labs.arxiv.org/html/2605.00473` with an explicit browser
User-Agent on 2026-07-24. HTML SHA-256:
`ed1f5ebbab55beda1e583b3f896e180d14a29b5920ce2910986b222a12c60a77`.
The arXiv source archive SHA-256 is
`1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f`.

## Exact anchors and quantifiers

- Algorithm 1 (`#alg1`) initializes
  \(B_0=\widetilde\alpha\widetilde B_0\) and
  \(W_0=(\widetilde\alpha/3)\widetilde W_0\), with Gaussian entries scaled by
  \(1/\sqrt d\).
- For integer iterations \(0\leq\tau<K_1/2\), Phase I updates both matrices by
  gradients of Equation (1), the unregularized empirical loss.
- For \(K_1/2\leq\tau<K_1\), Phase II updates both matrices by gradients of
  Equation (5), whose penalty is
  \(\|B^\top B-WW^\top\|_F^2/8\).
- The exact derivative of that penalty is
  \(\frac12B(B^\top B-WW^\top)\) for \(B\) and
  \(-\frac12(B^\top B-WW^\top)W\) for \(W\).

The experiment binds `K1` to a positive even integer so the printed half-step
boundary is unambiguous. Claim 1 and Claim 2 are algorithm-description claims,
not convergence theorems; Assumptions 3.2 and 3.3 therefore govern later
statistical claims rather than the algebraic identity checked here.

## Source discrepancies

Two inconsistencies are preserved rather than resolved opportunistically:

1. Section 4 prose says Phase I “performs \(K_1\) iterations” but immediately
   names the \(K_1/2\)-th iterate, while Algorithm 1 explicitly uses half of the
   total horizon for each phase. This contract follows Algorithm 1.
2. Equation (5)'s coefficient \(1/8\) implies half correction gradients. An
   older commented algorithm block in the arXiv source subtracts the full
   correction. The finite-difference checker follows the current displayed
   Equation (5), and treats the full correction as a negative control.
