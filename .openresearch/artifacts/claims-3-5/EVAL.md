# Claims 3–5 evaluation

Verdict: **BLOCKED** for each claim. Confidence: **MEDIUM**.

The cumulative fixed-command run is
`6661bf06-a416-4eeb-a5be-b446970ca8ad` at Git SHA
`e582fbea5cbce995dcd084eced463e142890721d`. Download the complete
seed-level output from
`../cumulative/run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json`; its SHA-256 is
`c531785bbfcf8103625e27de8863e36df5221cd5970f5eb2ec174adc3def85c5`.

- Claim 3: faithful TPGD shows the full four-variable directional trend,
  exact \(1/N\) scaling on a \(\delta=0,\kappa=1\) design, and the cited
  factor-\(k\) rate quotient checks exactly. It remains BLOCKED because finite
  sweeps do not certify the universal high-probability theorem.
- Claim 4: every predeclared group reaches the relative first-hit target in
  175–200 iterations on the exact-RIP route. It remains BLOCKED because
  \(\widetilde O(1)\) hides logarithmic and comparison constants and no
  machine-checkable proof certificate is available.
- Claim 5: an independently selected first-hit sweep moves from \(N=100\) to
  300 to 600 as noise standard deviation moves from 0.5 to 1.0 to 1.5. It
  remains BLOCKED because the theorem contains unspecified constants and
  finite calibration cannot verify its universal sufficient condition.

All independent numerical checkers pass and all three negative controls fail
for their intended reasons. Passing diagnostics are not converted into
theorem verification.
