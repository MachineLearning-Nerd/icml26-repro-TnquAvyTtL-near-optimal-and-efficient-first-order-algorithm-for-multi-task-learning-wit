"""Predeclared factorial sweep; values were not selected from a theorem formula."""

FACTORIAL_CONFIG = {
    "seeds": [4101, 4102, 4103, 4104, 4105],
    "base": {"d": 100, "k": 10, "T": 100, "N": 200},
    "values": {
        "d": [50, 75, 100],
        "k": [5, 10, 15],
        "T": [50, 75, 100],
        "N": [100, 150, 200, 300, 400],
    },
    "sigma": 0.1,
    "K1": 650,
    "alpha_tilde": 0.05,
    "phase1_step_multiplier": 0.05,
    "phase2_step_multiplier": 0.20,
    "checkpoint_interval": 25,
    "relative_first_hit_fraction": 0.01,
    "absolute_first_hit_threshold": 0.01,
}
