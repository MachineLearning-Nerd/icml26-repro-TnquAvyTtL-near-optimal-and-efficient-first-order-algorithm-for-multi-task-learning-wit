"""Predeclared configuration for direct Claims 3 and 4 TPGD evidence.

The grids are ordinary powers-of-two ranges selected independently of observed
outcomes.  The base has d/T=32 so the paper's leading dk/(NT) term is separated
from the lower-order task-coordinate term in this finite diagnostic.
"""

DIRECT_MULTIDIM_CONFIG = {
    "seeds": [8301, 8302, 8303, 8304, 8305, 8306],
    "base": {"d": 512, "k": 4, "T": 16, "N": 800},
    "factor_values": {
        "d": [128, 256, 512, 1024],
        "k": [2, 4, 6, 8],
        "T": [8, 16, 32, 64],
        "N": [200, 400, 800, 1600],
    },
    "rate": {
        "sigma": 0.2,
        "K1": 600,
        "alpha_tilde": 0.05,
        "phase1_step_multiplier": 0.05,
        "phase2_step_multiplier": 0.20,
        "relative_first_hit_fraction": 0.20,
        "maximum_slope_deviation": 0.25,
    },
    "iteration": {
        "sigma": 0.02,
        "K1": 600,
        "alpha_tilde": 0.05,
        "phase1_step_multiplier": 0.05,
        "phase2_step_multiplier": 0.20,
        "relative_squared_error_target": 0.05,
        "maximum_absolute_loglog_slope": 0.25,
        "maximum_median_ratio": 2.0,
    },
}
