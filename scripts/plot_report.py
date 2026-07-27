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
    / ".openresearch/artifacts/claims-3-5/direct-current"
    / "direct_multidim_tpgd.json"
)
THRESHOLD_RAW = (
    ROOT
    / ".openresearch/artifacts/claims-3-5/direct-current"
    / "claim5_threshold_phase_diagram.json"
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
    summaries = data["rate_summaries"]
    names = ["d", "k", "T", "N"]
    labels = ["dimension d", "rank k", "tasks T", "samples N"]
    target = np.asarray([1.0, 1.0, -1.0, -1.0])
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
    ax.set_title("Direct TPGD recovers every exponent in the full dk/(NT) rate")
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
    grouped = {}
    for row in data["rows"]:
        key = (row["factor"], row["factor_value"], row["N"])
        grouped.setdefault(key, []).append(row)
    ratios = []
    success_fractions = []
    for rows in grouped.values():
        ratios.append(rows[0]["N_over_sample_expression"])
        success_fractions.append(np.mean([row["success"] for row in rows]))
    ratios = np.asarray(ratios)
    success_fractions = np.asarray(success_fractions)
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    scatter = ax.scatter(
        ratios,
        success_fractions,
        c=success_fractions,
        cmap="RdYlGn",
        vmin=0,
        vmax=1,
        s=42,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.4,
    )
    ax.axvline(0.25, color=COLORS["red"], linestyle=":", label="registered low ratio")
    ax.axvline(10, color=COLORS["navy"], linestyle="--", label="frozen sufficient margin")
    ax.set_xscale("log")
    ax.set_xlabel(r"$N\,/\,\{\sigma^2(d+T)k\kappa^4/\sigma_k^2\}$")
    ax.set_ylabel("held-out success fraction (five seeds)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("Held-out Claim 5 phase diagram across five factor families")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    fig.colorbar(scatter, ax=ax, label="success fraction")
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
    summaries = data["iteration_summaries"]
    factors = ["d", "k", "T", "N"]
    markers = ["o", "s", "^", "D"]
    colors = [COLORS["blue"], COLORS["orange"], COLORS["green"], COLORS["navy"]]
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    for factor, marker, color in zip(factors, markers, colors):
        summary = summaries[factor]
        x = np.arange(4)
        medians = summary["median_first_hit_iterations"]
        ax.plot(
            x,
            medians,
            marker=marker,
            linewidth=2,
            markersize=6,
            color=color,
            label=f"{factor}: slope {summary['log_log_median_iteration_slope']:+.3f}",
        )
    ax.set_xticks(np.arange(4), ["level 1", "level 2", "level 3", "level 4"])
    ax.set_xlabel("increasing factor value (see legend and report table)")
    ax.set_ylabel("first-hit iteration")
    ax.set_title("TPGD first-hit counts stay stable across d, k, T, and N")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(OUT / "dimension_iterations.png", dpi=180)
    plt.close(fig)


def main() -> None:
    _style()
    OUT.mkdir(parents=True, exist_ok=True)
    data = json.loads(RAW.read_text())
    direct = json.loads(DIMENSION_RAW.read_text())
    threshold = json.loads(THRESHOLD_RAW.read_text())
    headline_slopes(direct)
    tpgd_trajectory(data)
    sample_threshold(threshold)
    transfer_decomposition(data)
    dimension_iterations(direct)
    print(f"rendered_figures=5 output={OUT}")


if __name__ == "__main__":
    main()
