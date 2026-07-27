"""Render the five evidence figures used by the reproduction report."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RAW = (
    ROOT
    / ".openresearch/artifacts/cumulative"
    / "run_6661bf06-a416-4eeb-a5be-b446970ca8ad.json"
)
DIMENSION_RAW = (
    ROOT
    / ".openresearch/artifacts/claims-3-5/source-certified"
    / "dimension_iteration_sweep.json"
)
OUT = ROOT / "reports/tpgd-reproduction/images"
COLORS = {
    "navy": "#183153",
    "blue": "#2878B5",
    "orange": "#F28E2B",
    "green": "#2A9D8F",
    "red": "#D1495B",
    "gray": "#7A7A7A",
}


def _style() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )


def headline_slopes(data: dict) -> None:
    summaries = data["current_research"]["exact_rip"]["factorial_summaries"]
    names = ["N", "k", "T", "d"]
    labels = ["samples N", "rank k", "tasks T", "dimension d"]
    target = np.asarray([-1.0, 1.0, -1.0, 1.0])
    observed = np.asarray([summaries[name]["log_log_slope"] for name in names])
    intervals = np.asarray(
        [summaries[name]["bootstrap_95pct_slope_interval"] for name in names]
    )
    errors = np.vstack((observed - intervals[:, 0], intervals[:, 1] - observed))
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.axhline(0, color="#C7C7C7", linewidth=1)
    ax.scatter(x - 0.12, target, marker="D", s=55, color=COLORS["navy"], label="paper exponent")
    ax.errorbar(
        x + 0.12,
        observed,
        yerr=errors,
        fmt="o",
        markersize=7,
        capsize=5,
        linewidth=2,
        color=COLORS["orange"],
        label="TPGD estimate (95% bootstrap CI)",
    )
    for index, value in enumerate(observed):
        ax.text(index + 0.12, value + (0.12 if value >= 0 else -0.17), f"{value:+.2f}", ha="center")
    ax.set_xticks(x, labels)
    ax.set_ylabel("log–log error exponent")
    ax.set_ylim(-1.45, 1.45)
    ax.set_title("Exact-RIP TPGD: two exponents align; two only match direction")
    ax.legend(frameon=False, ncol=2, loc="upper center")
    ax.grid(axis="y", alpha=0.22)
    fig.tight_layout()
    fig.savefig(OUT / "headline_slopes.png", dpi=180)
    plt.close(fig)


def tpgd_trajectory(data: dict) -> None:
    records = data["calibration"]["paper_scale_tpgd"]["records"]
    iterations = np.asarray([row["iteration"] for row in records])
    errors = np.asarray([row["parameter_error"] for row in records])
    imbalance = np.asarray([row["imbalance_frobenius"] for row in records])
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.semilogy(iterations, errors, "o-", color=COLORS["blue"], linewidth=2.2, label="parameter error")
    ax.semilogy(iterations, imbalance, "s--", color=COLORS["green"], linewidth=1.8, label="balance residual")
    ax.axvline(325, color=COLORS["gray"], linestyle=":", linewidth=1.8)
    ax.text(319, 2e-4, "phase switch", rotation=90, va="bottom", ha="right", color=COLORS["gray"])
    ax.text(135, 3e-3, "Phase I", color=COLORS["navy"])
    ax.text(475, 3e-3, "Phase II", color=COLORS["navy"])
    ax.set_xlabel("TPGD iteration")
    ax.set_ylabel("error (log scale)")
    ax.set_title("Paper-dimensional calibration: d=100, k=10, T=100, N=100")
    ax.grid(alpha=0.22, which="both")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "tpgd_trajectory.png", dpi=180)
    plt.close(fig)


def sample_threshold(data: dict) -> None:
    rows = data["current_research"]["exact_rip"]["threshold_summary"]
    sigma_sq = np.asarray([row["sigma_squared"] for row in rows])
    observed = np.asarray([row["first_grid_N_with_at_least_four_successes"] for row in rows])
    expression = np.asarray([row["theorem_sample_expression_without_hidden_constant"] for row in rows])
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(sigma_sq, observed, "o-", linewidth=2.2, markersize=7, color=COLORS["orange"], label="independent first-hit N")
    ax.plot(sigma_sq, expression, "D--", linewidth=1.8, markersize=6, color=COLORS["navy"], label="displayed expression, unit constant")
    for x, y in zip(sigma_sq, observed):
        ax.annotate(f"N={int(y)}", (x, y), xytext=(0, 9), textcoords="offset points", ha="center")
    ax.set_xlabel(r"noise variance $\sigma^2$")
    ax.set_ylabel("per-task sample count N")
    ax.set_title("Non-circular sample-threshold calibration (5 seeds per grid cell)")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "sample_threshold.png", dpi=180)
    plt.close(fig)


def transfer_decomposition(data: dict) -> None:
    transfer = data["current_research"]["transfer_decomposition"]
    representation = transfer["representation_scaling"]
    optimization = transfer["optimization_scaling"]
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.3))
    axes[0].loglog(
        representation["upstream_N_values"],
        representation["mean_components_at_K2_max"],
        "o-",
        color=COLORS["blue"],
        linewidth=2.2,
    )
    axes[0].set_title(f"representation slope {representation['log_log_slope']:.2f}")
    axes[0].set_xlabel("upstream N")
    axes[0].set_ylabel("population-risk component")
    axes[1].loglog(
        optimization["K2_values"],
        optimization["mean_components_at_upstream_N_max"],
        "o-",
        color=COLORS["green"],
        linewidth=2.2,
    )
    axes[1].set_title(f"optimization slope {optimization['log_log_slope']:.2f}")
    axes[1].set_xlabel("target iterations K2")
    for ax in axes:
        ax.grid(alpha=0.22, which="both")
    fig.suptitle("Theorem 5.4 components decrease with independently varied resources")
    fig.tight_layout()
    fig.savefig(OUT / "transfer_decomposition.png", dpi=180)
    plt.close(fig)


def dimension_iterations(data: dict) -> None:
    dimensions = np.asarray(data["configuration"]["d_values"], dtype=float)
    medians = np.asarray(
        [data["median_first_hit_by_d"][str(int(d))] for d in dimensions],
        dtype=float,
    )
    control_hits = [
        row["first_hit_iteration"] for row in data["negative_control"]["rows"]
    ]
    control = np.asarray(
        [
            value if value is not None else data["configuration"]["K1"] + 25
            for value in control_hits
        ],
        dtype=float,
    )
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.semilogx(
        dimensions,
        medians,
        "o-",
        base=2,
        linewidth=2.4,
        markersize=7,
        color=COLORS["blue"],
        label="TPGD, theorem-normalized steps",
    )
    ax.semilogx(
        dimensions,
        control,
        "s--",
        base=2,
        linewidth=2,
        markersize=6,
        color=COLORS["red"],
        label=r"negative control, steps $\propto1/d$",
    )
    for d, value in zip(dimensions, control_hits):
        if value is None:
            ax.annotate(
                "no hit",
                (d, data["configuration"]["K1"] + 25),
                xytext=(0, 7),
                textcoords="offset points",
                ha="center",
                color=COLORS["red"],
            )
    ax.axhline(
        data["configuration"]["K1"],
        color=COLORS["gray"],
        linestyle=":",
        linewidth=1.5,
        label="800-iteration horizon",
    )
    ax.set_xticks(dimensions, [str(int(d)) for d in dimensions])
    ax.set_xlabel("input dimension d (log₂ scale)")
    ax.set_ylabel("first-hit iteration")
    ax.set_title("TPGD iteration count stays stable across a 32× dimension sweep")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "dimension_iterations.png", dpi=180)
    plt.close(fig)


def main() -> None:
    _style()
    OUT.mkdir(parents=True, exist_ok=True)
    data = json.loads(RAW.read_text())
    headline_slopes(data)
    tpgd_trajectory(data)
    sample_threshold(data)
    transfer_decomposition(data)
    dimension_iterations(json.loads(DIMENSION_RAW.read_text()))
    print(f"rendered_figures=5 output={OUT}")


if __name__ == "__main__":
    main()
