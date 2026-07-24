"""Predeclared exact-RIP route; grids were chosen before formula evaluation."""

EXACT_RIP_CONFIG = {
    "seeds": [6101, 6102, 6103, 6104, 6105],
    "base": {"d": 100, "k": 10, "T": 100, "N": 200},
    "factor_values": {
        "d": [50, 75, 100],
        "k": [5, 10, 15],
        "T": [50, 75, 100],
        "N": [100, 150, 200, 300, 400]
    },
    "noise_values": [0.5, 1.0, 1.5],
    "sample_grid": [100, 150, 200, 300, 400, 600],
    "operational_error_target": 0.1,
    "K1": 650,
    "alpha_tilde": 0.05,
    "phase1_step_multiplier": 0.05,
    "phase2_step_multiplier": 0.20,
    "relative_first_hit_fraction": 0.01,
    "checkpoint_interval": 25
}
