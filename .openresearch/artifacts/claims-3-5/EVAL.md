# Claims 3–5 evaluation

Verdict: **VERIFIED** for each claim. Confidence: **HIGH**.

The accepted source-certificate run is
`28927bbd-6573-4dc2-ad4c-f76d34fcccfe` at Git SHA
`eeb5b4b4fde7dcbda75d00158288ae122fa79431`, using the unchanged command
`uv run python repro/src/verify.py`.

- Claim 3: the hash-pinned Corollary 5.3 expression is reconstructed with
  exponent vector `(d=1,k=1,N=-1,T=-1)` across 24 cells, and the cited
  likelihood/proposed-rate quotient equals `k` with zero error. The mutation
  that removes one factor of `k` is rejected.
- Claim 4: substituting the theorem-normalized step sizes reconstructs the
  dimension-free polynomial dependence of `K1`, including the factor two from
  the `K1/2` exponent. A separate 30-run faithful TPGD sweep has median first
  hits `82,96,97,102,101,114` over `d=32..1024`, absolute log slope `0.0763`,
  and a discriminating `1/d`-step control that degrades to no hit.
- Claim 5: the displayed
  `sigma^2(d+T)k kappa^4/sigma_k^2` expression is independently reconstructed
  in 24 cells with zero error. Replacing `kappa^4` by `kappa^2` is rejected.

The source archive SHA-256 is
`1f9b28d527bc30de0dd327a8ad86466e1ffce415b04a6a78158ed2ca02c9556f`.
The certificate verifies the exact registered theorem identities and
asymptotic dependences; it does not claim a formalization of every appendix
lemma or identify hidden constants.

Raw evidence is under `source-certified/`; the claim contract, method, source
audit, and limitations are under `theorem-certificate/`.
