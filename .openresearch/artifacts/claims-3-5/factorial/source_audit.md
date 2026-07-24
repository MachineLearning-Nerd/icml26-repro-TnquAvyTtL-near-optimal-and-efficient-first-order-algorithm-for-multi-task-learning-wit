# Claims 3–5 source audit: factorial route

Theorem 5.1 (`#S5.Thmtheorem1`) assumes every realized task design satisfies
Definition 3.1 RIP with a common
\(\delta\lesssim\min\{k^{-1/2}\kappa^{-7/2},\kappa^{-6}\}\), as well as the
printed hyperparameter and per-task sample conditions. Its conclusion is a
high-probability factor-distance upper bound with an optimization term plus a
noise term.

Corollary 5.3 (`#S5.Thmtheorem3`) inherits every Theorem 5.1 condition and
states population estimation error
\(T^{-1}\sum_t\|\widehat v_t-v_t^*\|^2\lesssim\sigma^2dk/(NT)\). The following
prose compares this upper bound with prior likelihood-based upper bounds of
order \(dk^2/(NT)\); it is not an instancewise promise of an exact factor-k
numerical gap.

Claim 4's \(\widetilde O(1)\) treats condition number as constant and suppresses
logarithmic dependence. A finite sweep can measure first-hit iteration
distributions but cannot prove a uniform complexity upper bound.

Claim 5's displayed sample expression contains an unspecified comparison
constant and is additional to the RIP assumption. This route computes the
expression only after collecting observations and separately reports the exact
realized RIP constant. It does not infer theorem validity from monotonicity.

Source retrieval details and hashes are in the Claims 1–2 source audit. The
same ar5iv HTML and arXiv source archive are used here.
