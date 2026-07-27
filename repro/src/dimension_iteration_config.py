"""Predeclared dimension sweep for the Claim 4 TPGD iteration audit."""

DIMENSION_ITERATION_CONFIG = {
    "d_values": [32, 64, 128, 256, 512, 1024],
    "k": 4,
    "T": 32,
    "seeds": [9201, 9202, 9203, 9204, 9205],
    "K1": 800,
    "alpha_tilde": 0.05,
    "eta1_times_sigma1": 0.1,
    "eta2_times_sigma1": 0.1,
    "relative_squared_error_target": 1e-4,
    "maximum_median_iteration_ratio": 1.50,
    "maximum_absolute_loglog_slope": 0.15,
}
