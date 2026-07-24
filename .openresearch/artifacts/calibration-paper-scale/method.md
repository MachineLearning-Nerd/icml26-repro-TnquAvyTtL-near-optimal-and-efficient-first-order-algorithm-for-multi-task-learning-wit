# Paper-scale optimization calibration

This node runs faithful TPGD at `d=100,k=10,T=100,N=100` for 650 iterations,
matching Figure 1(a)'s dimensions and horizon. It is explicitly
**CALIBRATION_ONLY**: one seed and one configuration cannot verify Claims 3–5.

The checkpoint grid `[0,25,50,100,200,325,400,500,650]`, absolute first-hit
thresholds `[1,0.3,0.1,0.03,0.01]`, and five-fold improvement criterion are
committed before the run. None is computed from the theorem rate. The
independent checker recomputes taskwise parameter error with a Python loop; a
frozen-initialization control must fail the improvement criterion.

Step sizes are `0.02/sigma_1(M*)` in Phase I and `0.10/sigma_1(M*)` in Phase
II. This is the conservative member of a small sibling calibration round.
The selected member will be determined by observed convergence, stability, and
runtime—not by whichever result best matches the theorem formula.
