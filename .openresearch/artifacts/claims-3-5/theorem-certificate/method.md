# Method

`repro/src/theorem_certificate.py` verifies the source anchors and reconstructs
the displayed rate, iteration, and sample-condition identities without fitting
the answer from generated data.

For Claim 4 it substitutes
`eta1=c1/(kappa^5 sigma1)` and `eta2=c2/sigma1`. This gives
`1/(eta1 sigma_k)=kappa^6/c1` and contraction
`1-c2/(4 kappa)`. The implementation uses the theorem's full `K1/2` exponent,
so the reported total count contains the required factor two. The initialization
condition contributes `log(max(d+T,k))`, which is precisely the logarithmic
dimension dependence suppressed by the tilde notation.

`repro/src/dimension_iteration_sweep.py` separately runs Algorithm 1 under an
exact-RIP, unit-spectrum construction across six values of `d` and five seeds.
It is corroboration, not the symbolic certificate itself.
