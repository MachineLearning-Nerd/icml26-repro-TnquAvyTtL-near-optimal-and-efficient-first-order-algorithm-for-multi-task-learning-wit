# Factorial TPGD scaling and first-hit method

The sweep varies one of `d`, `k`, `T`, or `N` while holding the other base
values fixed at `d=100,k=10,T=100,N=200`. Each point uses five deterministic
seeds and the promoted paper-scale TPGD calibration. The 650-iteration horizon
and 25-iteration checkpoint grid are fixed across all points.

For each run the verifier records mean task-parameter error, an independently
recomputed task loop, the first checkpoint reaching 1% of initialization
error, and the exact worst-task RIP delta. Factor summaries report standard
errors and a deterministic 2,000-resample bootstrap interval for the log-log
slope.

The negative control cyclically permutes response task labels while leaving
each design and the audited ground truth fixed. Its final parameter error must
exceed ten times the unpermuted base mean.

This route is deliberately incapable of returning `VERIFIED` for Claims 3–5.
The exact theorem is universal/high-probability and contains hidden constants;
finite experiments provide scoped corroboration or identify assumption
failures, never a proof certificate.
