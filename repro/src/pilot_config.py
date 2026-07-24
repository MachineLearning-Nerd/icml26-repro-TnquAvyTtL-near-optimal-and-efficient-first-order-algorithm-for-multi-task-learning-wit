"""Committed configuration for the conservative paper-scale calibration node."""

PILOT_CONFIG = {
    "seed": 3101,
    "d": 100,
    "k": 10,
    "T": 100,
    "N": 100,
    "sigma": 0.1,
    "K1": 650,
    "phase1_step_multiplier": 0.02,
    "phase2_step_multiplier": 0.10,
    "alpha_tilde": 0.05,
    "checkpoints": [0, 25, 50, 100, 200, 325, 400, 500, 650],
    "first_hit_thresholds": [1.0, 0.3, 0.1, 0.03, 0.01],
}
