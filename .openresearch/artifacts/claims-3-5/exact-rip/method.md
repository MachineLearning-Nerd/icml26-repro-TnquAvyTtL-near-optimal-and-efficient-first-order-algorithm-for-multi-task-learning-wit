# Exact-RIP theorem calibration

For every task, choose a signed permutation matrix \(P_t\) and define
\(X_t=\sqrt N[P_t;0]\). Then \(X_t^\top X_t/N=I_d\) exactly, giving a compact
machine-checkable \(\delta=0\) certificate. With Gaussian response noise,
\(X_t^\top y_t/N=\theta_t^*+\epsilon_t\) where
\(\epsilon_t\sim N(0,\sigma^2 I/N)\). TPGD gradients depend only on this
sufficient statistic, so the implementation is distributionally identical to
running Algorithm 1 on the explicit designs. A separate small explicit-matrix
checker compares both gradient routes entrywise.

The ground-truth task matrix is balanced so every nonzero singular value of
\(B^*W^*\) is \(\sqrt{T/k}\), hence \(\kappa=1\). This removes the previous
route's RIP failure and condition-number confounding.

The same factorial grid is rerun with five new seeds. A second grid independently
varies noise standard deviation and sample count, then reports the first
predeclared sample count at which at least four of five seeds reach error 0.1.
Only after observations does the verifier compute the theorem's sample
expression and compare their log scaling.

The negative control deletes one design direction, producing \(\delta=1\);
the certificate checker must reject it. Hidden constants in the theorem's
initialization bound remain a declared blocker, not a fitted knob.
