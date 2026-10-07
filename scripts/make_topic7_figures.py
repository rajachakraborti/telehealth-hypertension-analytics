"""Figures for the Topic 7 audit report and deck, built from the notebook's saved metrics.

Run from the repository root after the notebook has been executed:
    python scripts/make_topic7_figures.py
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

SRC = "artifacts/topic6/topic6_metrics.json"
OUT = "artifacts/topic7"
os.makedirs(OUT, exist_ok=True)
m = json.load(open(SRC, encoding="utf-8"))
plt.rcParams.update({"font.family": "sans-serif", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 200, "savefig.bbox": "tight"})
INK, MUTED, BLUE, ORANGE, RED, GREEN = "#1f2933", "#52606d", "#2a78d6", "#eb6834", "#c53030", "#2f855a"


# ---------- Figure A: cross-validated selection (z-scores against the pre-set rule) ----------
def fig_selection():
    cmp_, dec = m["selection"]["comparisons"], m["selection"]["decisions"]
    steps = [("feature_engineering", "Feature engineering\n(vs raw features)"),
             ("hyperparameter_search", "Hyperparameter search\n(vs default settings)"),
             ("isotonic_calibration", "Isotonic calibration\n(vs uncalibrated)"),
             ("morning_surge_features", "Morning-surge features\n(vs current features)")]
    z = [cmp_[k]["logloss"]["z"] for k, _ in steps]
    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    ax.axvspan(-8, -2, color="#fde8e8", lw=0); ax.axvspan(-2, 2, color="#f1f3f5", lw=0); ax.axvspan(2, 15, color="#e3f4ea", lw=0)
    colors = [BLUE if "RETAIN" in dec[k] else GREEN if dec[k] == "ADOPT" else RED if dec[k] == "REJECT" else "#7b8794"
              for k, _ in steps]
    y = np.arange(len(steps))[::-1]
    ax.barh(y, z, color=colors, height=0.55)
    for yi, zi, (k, _) in zip(y, z, steps):
        ax.text(zi + (0.3 if zi >= 0 else -0.3), yi, f"z = {zi:+.1f}  {dec[k].split(' (')[0].title()}",
                va="center", ha="left" if zi >= 0 else "right", fontsize=9, color=INK)
    ax.axvline(0, color=INK, lw=0.8)
    for v in (-2, 2):
        ax.axvline(v, color=MUTED, ls="--", lw=0.9)
    ax.set_ylim(-0.6, len(steps) - 0.05)
    ax.set_yticks(y, [s for _, s in steps]); ax.set_xlim(-8, 15)
    ax.set_xlabel("Cross-validated log-loss gain, in standard errors (positive = step helps)")
    top = len(steps) - 0.3
    ax.text(-5, top, "Reject", ha="center", color=RED, fontsize=9, fontweight="bold")
    ax.text(0, top + 0.12, "No supported\ndifference", ha="center", va="center", color=MUTED, fontsize=8.5, fontweight="bold")
    ax.text(8.5, top, "Adopt", ha="center", color=GREEN, fontsize=9, fontweight="bold")
    n = m["selection"]["nested_cv"]
    ax.set_title(f"Selection used training-set cross-validation only. Nested check on tuning: gain {n['gain']:.3f} (SE {n['se']:.3f})",
                 fontsize=9.5, loc="left", color=INK, pad=10)
    plt.tight_layout(); plt.savefig(f"{OUT}/topic7_cv_selection.png"); plt.close()


# ---------- Figure B: accuracy by subgroup ----------
def fig_subgroups():
    sub = m["eda"]["subgroups"]
    keys = list(sub)
    acc = np.array([sub[k][0] for k in keys]) * 100; n = np.array([sub[k][1] for k in keys])
    err = 1.96 * np.sqrt((acc / 100) * (1 - acc / 100) / n) * 100
    labels = [k.replace("sex=", "Sex ").replace("age=", "Age ") for k in keys]
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    cols = [ORANGE if a < 88 else BLUE for a in acc]
    ax.bar(labels, acc, yerr=err, color=cols, capsize=3, width=0.6)
    overall = m["results"]["xgb_tuned"]["accuracy"] * 100
    ax.axhline(overall, color=MUTED, ls="--", lw=1, label=f"Overall {overall:.1f}%")
    for i, (a, nn, e) in enumerate(zip(acc, n, err)):
        ax.text(i, 79.2, f"n={nn}", ha="center", fontsize=8, color="white")
        ax.text(i + 0.12, a + e + 0.6, f"{a:.1f}%", ha="left", fontsize=8.5, color=INK, fontweight="bold")
    ax.set_ylim(78, 106); ax.set_ylabel("Holdout accuracy (%)")
    ax.set_yticks(range(80, 101, 5))
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.set_title("Accuracy by subgroup (95% CI); under-45 is lowest", fontsize=10, loc="left")
    plt.tight_layout(); plt.savefig(f"{OUT}/topic7_subgroups.png"); plt.close()


# ---------- Figure C: architecture as built ----------
def fig_architecture():
    fig, ax = plt.subplots(figsize=(10, 5.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 56); ax.axis("off")

    def box(x, y, w, h, text, fc="#eef2ff", ec="#5b6cc9", dashed=False, fs=9, bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc=fc, ec=ec, lw=1.3,
                                    ls="--" if dashed else "-"))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK,
                fontweight="bold" if bold else None)

    def arrow(p, q, label=None, dashed=False, dx=0, dy=1.2):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, lw=1.2, color=MUTED, ls="--" if dashed else "-"))
        if label:
            ax.text((p[0] + q[0]) / 2 + dx, (p[1] + q[1]) / 2 + dy, label, ha="center", fontsize=8, color=MUTED)

    box(2, 42, 16, 9, "Clinician\nbrowser", fc="#fff7e6", ec="#d69e2e")
    box(27, 42, 20, 9, "React dashboard\n(Vercel)\nABPM Staging page")
    ax.add_patch(FancyBboxPatch((24, 3), 74, 34, boxstyle="round,pad=0.3,rounding_size=1.5", fc="#fffff0", ec="#b7a53a", lw=1.2))
    ax.text(26, 34.2, "FastAPI backend (Render)", fontsize=9.5, fontweight="bold", color="#6b5f12")
    box(27, 24, 17, 7, "JWT login + RBAC\n(bcrypt passwords)", fs=8.5)
    box(47, 24, 17, 7, "slowapi rate limit\n(SHA-256 fingerprint)", fs=8.5)
    box(67, 24, 28, 7, "/api/abpm/classify\n24-hour record in, stage out", fs=8.5, bold=True)
    box(67, 11, 13, 8, "Feature\nextraction", fs=8.5)
    box(82, 11, 13, 8, "XGBoost +\nTreeSHAP", fs=8.5, fc="#e6f4ea", ec="#2f855a")
    box(27, 14.5, 17, 6.5, "Patient registry\n(/api/clinical)", fs=8.5)
    box(27, 4.5, 22, 7, "PostgreSQL\n(pgcrypto column encryption)", fc="#f1f5f9", ec="#64748b", fs=8.5)
    box(52, 5.5, 11, 8, "/api/metrics\n(Prometheus)", fc="#f1f5f9", ec="#64748b", fs=8)
    box(60, 46, 18, 7, "GitHub Actions\nCI (pytest, build)", fc="#f1f5f9", ec="#64748b", fs=8.5)
    box(81, 46, 17, 7, "Override log + Jira\nretraining (planned)", fc="#ffffff", ec="#a0aec0", dashed=True, fs=8)
    arrow((18, 46.5), (27, 46.5))
    arrow((37, 42), (37, 31.4), "HTTPS + JWT", dx=6)
    arrow((44, 27.5), (47, 27.5)); arrow((64, 27.5), (67, 27.5))
    arrow((81, 24), (81, 19.4)); arrow((74, 24), (74, 19.4))
    arrow((35.5, 24), (35.5, 21.4)); arrow((35.5, 14.5), (35.5, 11.7), "encrypted PHI", dx=7, dy=-0.4)
    arrow((69, 46), (69, 37.4), "tests on push", dx=7, dy=-0.5)
    arrow((89, 31.4), (89, 46), None, dashed=True)
    ax.set_title("System architecture as built (dashed = planned, not implemented)", fontsize=11, loc="left", color=INK)
    plt.tight_layout(); plt.savefig(f"{OUT}/topic7_architecture.png"); plt.close()


# ---------- Figure D: benchmark accuracy with bootstrap intervals ----------
def fig_benchmarks():
    r, ci = m["results"], m["ci"]
    rows = [("office_rule", "Office rule\n(1 reading)"), ("abpm_rule", "ABPM rule\n(daytime mean)"), ("logreg", "Logistic\nregression"),
            ("xgb_default", "Default\nXGBoost"), ("xgb_tuned", "Refined\nXGBoost")]
    acc = np.array([r[k]["accuracy"] for k, _ in rows]) * 100
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    cols = ["#9aa5b1", "#9aa5b1", BLUE, BLUE, ORANGE]
    ax.bar(range(len(rows)), acc, color=cols, width=0.62)
    for i, (k, _) in enumerate(rows):
        if k in ci:
            lo, hi = np.array(ci[k]["accuracy"]) * 100
            ax.plot([i, i], [lo, hi], color=INK, lw=1.4)
            ax.plot([i - .08, i + .08], [lo, lo], color=INK, lw=1.4)
            ax.plot([i - .08, i + .08], [hi, hi], color=INK, lw=1.4)
        ax.text(i + 0.36, acc[i] - 1.5, f"{acc[i]:.1f}", ha="left", va="top", fontsize=9.5, color=INK, fontweight="bold")
    ax.set_xticks(range(len(rows)), [l for _, l in rows], fontsize=9); ax.set_ylim(40, 100); ax.set_ylabel("Holdout accuracy (%)")
    ax.set_title("Holdout accuracy with 95% bootstrap intervals (n = 540)", fontsize=10, loc="left")
    plt.tight_layout(); plt.savefig(f"{OUT}/topic7_benchmarks.png"); plt.close()


if __name__ == "__main__":
    fig_selection(); fig_subgroups(); fig_architecture(); fig_benchmarks()
    print("figures written to", OUT)
