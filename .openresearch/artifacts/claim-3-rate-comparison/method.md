# Method

The verifier represents each asymptotic rate as an integer exponent map over
`d`, `k`, `N`, and `T`. It performs the notation substitutions recorded in the
claim contract and subtracts proposed-rate exponents from prior-rate exponents.
The only surviving exponent must be `k: 1`.

An independent numerical cross-check evaluates both monomials at five
predeclared values of \(k\). A negative control changes the cited rate to
\(dk/(NT)\); this must eliminate the factor-\(k\) quotient and be rejected.

No experiment-derived slope or selected sample size enters this check. Hidden
constants and polylogarithmic factors are not compared.
