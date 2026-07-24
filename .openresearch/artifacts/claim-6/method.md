# Direct transfer-risk decomposition method

Upstream TPGD uses the exact-RIP sufficient-statistic construction and a
balanced \(\kappa=1\) truth. On a new task, \(x\sim N(0,I)\) and Gaussian
response noise satisfy Assumption 3.3 with \(\alpha=3\). Algorithm 2 is run
exactly as printed for four `K2` horizons and four upstream sample sizes.

Population excess risk is evaluated analytically, not with a test-set proxy.
The orthogonal projection onto `span(Bhat)` yields the exact Pythagorean split:

1. representation approximation:
   \(0.5\|(I-P_{\widehat B})\theta^*\|^2\);
2. task optimization:
   \(0.5\|\widehat B(w_{K_2}-w_{\mathrm{opt}})\|^2\).

The sum must equal the direct excess risk within `1e-10`. Scaling of the first
component is measured over upstream `N`; scaling of the second is measured over
`K2`, without mixing factors. A zero-anchor negative control must break the
identity.

The experiment is scoped corroboration. Hidden comparison constants,
unspecified `h`, the pseudocode/prose boundary mismatch, and universal
high-probability quantifiers remain explicit blockers.
