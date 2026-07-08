# -*- coding: utf-8 -*-
"""
Figure 11: Total relief cost under crowd-related parameters

"""

import pandas as pd
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
})

# ===== 3. Read data =====
file_path = "EJOR_Data for numerical analysis.xlsx"

sheet_candidates = ["Section Section 6.1.4", "Section 6.1.4"]
for sheet_name in sheet_candidates:
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
        break
    except ValueError:
        continue

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Rename columns for easier use
df = df.rename(columns={
    "min_total_cost_1e8_CNY": "cost"
})

# Keep required columns
df = df[["Panel", "Parameter", "Phi", "x_value", "cost"]].dropna(
    subset=["Panel", "Phi", "x_value", "cost"]
)

# Convert data types
df["Panel"] = df["Panel"].astype(str).str.strip()
df["Phi"] = pd.to_numeric(df["Phi"])
df["x_value"] = pd.to_numeric(df["x_value"])
df["cost"] = pd.to_numeric(df["cost"])

# ===== 4. Define helper functions =====
def set_log2_ticks_subset(ax, anchor=0.8, exponents=(-3, -1, 1, 3)):
    """Set selected ticks on a log2 axis."""
    ticks = [anchor * (2 ** k) for k in exponents]
    labels = ["2⁻³", "2⁻¹", "2¹", "2³"]

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
            sub["cost"],
            color=colors[i % len(colors)],
            marker=markers[i % len(markers)],
            linestyle=linestyles[i % len(linestyles)],
            linewidth=1.6,
            markersize=6,
            label=f"Φ = {phi:g}"
        )

    ax.grid(True, linestyle=":", linewidth=0.5, alpha=0.6)
    ax.set_xlabel(xlabel)

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
        "legend_loc": "upper left"
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

# ===== 6. Set shared y-axis =====
axes[0].set_ylabel("Total relief cost (unit: 10⁸ CNY)")

for ax in axes:
    ax.set_ylim(0.7, 1.6)
    ax.yaxis.set_major_locator(mticker.MultipleLocator(0.2))

# ===== 7. Save figure =====
fig.subplots_adjust(left=0.05, right=0.98, bottom=0.30, top=0.97, wspace=0.25)
fig.savefig("Figure_11_total_cost_vs_crowdparams_three_panels.pdf", dpi=400, bbox_inches="tight")
plt.show()