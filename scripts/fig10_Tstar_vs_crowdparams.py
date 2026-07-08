# -*- coding: utf-8 -*-
"""
Figure 10: Optimal number of periods under crowd-related parameters

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mticker

# ===== 1. Set line styles =====
colors = ["#d95f02", "#7570b3", "#e7298a", "#66a61e"]
markers = ["s", "^", "D", "v"]
linestyles = ["--", "-.", ":", (0, (5, 1))]

# ===== 2. Set figure style =====
mpl.rcParams.update({
    "font.family": "Times New Roman",
    "font.serif": ["Times New Roman"],
    "font.size": 14,
    "axes.labelsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    "mathtext.it": "Times New Roman:italic",
    "mathtext.bf": "Times New Roman:bold",
})

# ===== 3. Read data =====
file_path = "EJOR_Data for numerical analysis.xlsx"
sheet_name = "Section 6.1.4"

df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Rename columns for easier use
df = df.rename(columns={
    "Optimal number of periods |T|*": "T_star"
})

# Keep required columns
df = df[["Panel", "Parameter", "Phi", "x_value", "T_star"]].dropna(
    subset=["Panel", "Phi", "x_value", "T_star"]
)

# Convert data types
df["Panel"] = df["Panel"].astype(str).str.strip()
df["Phi"] = pd.to_numeric(df["Phi"])
df["x_value"] = pd.to_numeric(df["x_value"])
df["T_star"] = pd.to_numeric(df["T_star"]).astype(int)

# ===== 4. Define helper functions =====
def set_log2_ticks_subset(ax, anchor=0.8, exponents=(-3, -1, 1, 3)):
    """Set selected ticks on a log2 axis."""
    ticks = [anchor * (2 ** k) for k in exponents]
    labels = [f"2^{k}" for k in exponents]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    ax.xaxis.set_minor_locator(mticker.NullLocator())


def plot_panel(ax, data, panel_label, xlabel, use_log_scale=False):
    """Plot one panel."""
    phi_values = sorted(data["Phi"].unique())

    for i, phi in enumerate(phi_values):
        sub = data[data["Phi"] == phi].sort_values("x_value")

        ax.plot(
            sub["x_value"],
            sub["T_star"],
            color=colors[i % len(colors)],
            marker=markers[i % len(markers)],
            linestyle=linestyles[i % len(linestyles)],
            linewidth=1.6,
            markersize=6,
            label=f"Φ = {phi:g}"
        )

    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.6)
    ax.set_xlabel(xlabel)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    if use_log_scale:
        ax.set_xscale("log", base=2)
        set_log2_ticks_subset(ax, anchor=0.8, exponents=(-3, -1, 1, 3))
    else:
        ax.set_xticks(sorted(data["x_value"].unique()))

    ax.text(
        0.5,
        -0.23,
        panel_label,
        ha="center",
        va="top",
        transform=ax.transAxes,
        fontsize=14,
        fontfamily="Times New Roman"
    )


# ===== 5. Create subplots =====
fig, axes = plt.subplots(1, 3, figsize=(15, 4.7), sharey=True)

panel_settings = [
    {
        "panel": "(a)",
        "xlabel": "ϒ (road capacity consumption multiplier)",
        "use_log_scale": True,
        "legend_loc": "upper right"
    },
    {
        "panel": "(b)",
        "xlabel": "ϒ (participation ratio multiplier)",
        "use_log_scale": True,
        "legend_loc": "upper right"
    },
    {
        "panel": "(c)",
        "xlabel": "L (periods)",
        "use_log_scale": False,
        "legend_loc": "upper left"
    }
]

for ax, setting in zip(axes, panel_settings):
    panel_data = df[df["Panel"] == setting["panel"]].copy()

    plot_panel(
        ax=ax,
        data=panel_data,
        panel_label=setting["panel"],
        xlabel=setting["xlabel"],
        use_log_scale=setting["use_log_scale"]
    )

    ax.legend(
        loc=setting["legend_loc"],
        frameon=False,
        prop={"family": "Times New Roman", "size": 14}
    )

# ===== 6. Set shared y-axis label =====
axes[0].set_ylabel("Optimal number of periods |T|*")

# ===== 7. Save figure =====
fig.subplots_adjust(left=0.05, right=0.98, bottom=0.30, top=0.97, wspace=0.25)
fig.savefig("Figure_10_Tstar_vs_crowdparams_three_panels.pdf", dpi=400, bbox_inches="tight")
plt.show()