"""Predeclared Theorem 5.4 transfer-risk decomposition route."""

TRANSFER_CONFIG = {
    "seeds": [8101, 8102, 8103, 8104, 8105, 8106, 8107, 8108],
    "d": 100,
    "k": 10,
    "T": 100,
    "upstream_N_values": [100, 200, 400, 800],
    "K2_values": [1000, 2000, 4000, 8000],
    "sigma": 1.0,
    "K1": 650,
    "alpha_tilde": 0.05,
    "phase1_step_multiplier": 0.05,
    "phase2_step_multiplier": 0.20,
    "target_h": 0,
    "eta0_fraction_of_alpha_trace_bound": 0.25
}
