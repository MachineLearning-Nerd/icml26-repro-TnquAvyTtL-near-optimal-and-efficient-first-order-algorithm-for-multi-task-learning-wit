"""Predeclared non-circular sample-threshold grid for Claim 5.

The N grid is fixed independently of the theorem expression.  The analysis
computes that expression only after all TPGD outcomes have been generated.
"""

CLAIM5_THRESHOLD_CONFIG = {
    "seeds": [8501, 8502, 8503, 8504, 8505],
    "N_grid": [32, 64, 128, 256, 512, 1024, 2048, 4096],
    "base": {
        "d": 128,
        "T": 32,
        "k": 4,
        "sigma": 0.4,
        "kappa": 1.0,
        "sigma_k": 1.0,
    },
    "factor_values": {
        "sigma_squared": [0.04, 0.16, 0.64],
        "d_plus_T": [96, 160, 288],
        "k": [2, 4, 8],
        "kappa": [1.0, 1.5, 2.0],
        "sigma_k": [0.5, 1.0, 2.0],
    },
    "K1": 1600,
    "alpha_tilde": 0.02,
    "phase1_step_multiplier": 0.05,
    "phase2_step_multiplier": 0.20,
    "absolute_stacked_distance_squared_target": 0.20,
    "normalized_stacked_distance_squared_target": 0.05,
    "successes_required_out_of_five": 4,
    "high_ratio_margin": 4.0,
    "low_ratio_margin": 0.25,
}
