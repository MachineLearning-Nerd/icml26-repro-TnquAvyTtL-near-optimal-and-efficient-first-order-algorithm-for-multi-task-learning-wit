# Claim 3 primary-source comparison audit

Retrieved 2026-07-24 with the explicit User-Agent
`OpenResearch-Reproduction/1.0 (paper audit)`.

## Proposed paper

- Source: `https://arxiv.org/src/2605.00473`
- SHA-256: `1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f`
- Anchor: `Main_Latex/main_result.tex`, Corollary 5.3 and the paragraph
  immediately following it.
- Relevant rate: population loss \(\widetilde O(dk/(NT))\).

## Tripuraneni, Jin, and Jordan (2021)

- Source: `https://arxiv.org/pdf/2002.11684`
- SHA-256: `4d2167b0f63ac72dc72deed79ed0041eefd38acc3bbbd7b4d9782967f02a46ac`
- Anchor: informal Theorem 1, Eq. (2), with formal statement in Theorem 6.
- Relevant source-representation term: \(\widetilde O(dr^2/n_1)\), where
  \(n_1\) is the total number of source-task samples.
- Mapping: \(r=k\), \(n_1=NT\), giving \(\widetilde O(dk^2/(NT))\).

## Thekumparampil et al. (2021)

- Source:
  `https://proceedings.neurips.cc/paper_files/paper/2021/file/99e7e6ce097324aceb45f98299ceb621-Paper.pdf`
- SHA-256: `55cc2ba9bec7e478fc7c23744e5840da7826de032eb35b4859b986ec2424ec34`
- Anchor: simplified Theorem 1, Eq. (5), and prediction-error Remark 2.
- Relevant source-representation prediction term is proportional to
  \(dr^2/(mt)\).
- Mapping: \(r=k\), \(m=N\), \(t=T\), giving \(dk^2/(NT)\).

The monomial quotient \([dk^2/(NT)]/[dk/(NT)]\) is exactly \(k\). This is a
source-bound algebra audit, not a proof that either upper bound is tight on
every instance and not an independent proof of the proposed theorem.
