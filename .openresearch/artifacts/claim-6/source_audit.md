# Claim 6 source audit

Theorem 5.4 inherits Assumptions 3.2 and 3.3 and Equation (6)'s upstream
hyperparameters. It adds
\(\eta_0\lesssim[\alpha\,\mathrm{tr}(\widehat B^\top H\widehat B)]^{-1}\)
and a lower bound on \(K_2\). Its displayed excess-risk upper bound is the sum
of a representation term proportional to \(1/N\) and an optimization term
\(\sigma^2k/K_2\).

Algorithm 2 performs last-iterate online SGD and defines
\(K_2'=\lfloor(K_2-h)/\log(K_2-h)\rfloor\). The theorem does not instantiate
the required input `h`. There is also an off-by-one discrepancy: pseudocode
halves the step before sampling update \(K_2'\) when `h=0`, while the prose
says the initial step remains constant through \(K_2'+h\) iterations.

This route binds to the pseudocode and commits `h=0` as one defensible
interpretation. It cannot convert the exact theorem to VERIFIED while that
input remains unspecified.
