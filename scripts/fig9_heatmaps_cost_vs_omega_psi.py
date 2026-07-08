# -*- coding: utf-8 -*-
"""
Figure 9: Heatmaps of optimal total relief cost for different |T| values

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# ===== 1. Set figure style =====
mpl.rcParams.update({
    "font.family": "Times New Roman",
    "font.serif": ["Times New Roman"],
    "font.size": 14,
    "axes.labelsize": 16,
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

# ===== 2. Read data =====
file_path = "EJOR_Data for numerical analysis.xlsx"
sheet_name = "Section 6.1.2-2"

df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Rename columns for easier use
df = df.rename(columns={
    "|T|": "T",
    "Optimal total relief cost (×10^8 CNY)": "cost"
})

# Keep the baseline case rho = 6
df = df[df["rho"] == 6].copy()

# Convert data types
df["T"] = pd.to_numeric(df["T"]).astype(int)
df["Omega"] = pd.to_numeric(df["Omega"])
df["Psi"] = pd.to_numeric(df["Psi"])
df["cost"] = pd.to_numeric(df["cost"])

# Use a common color scale across panels
vmax = df[df["T"] == 2]["cost"].max()
vmin = df[df["T"] == 6]["cost"].min()

# Selected |T| values and panel labels
T_list = [2, 4, 6]
panel_labels = ["(a) |T| = 2", "(b) |T| = 4", "(c) |T| = 6"]

# ===== 3. Create subplots =====
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)

for ax, T_val, panel_label in zip(axes, T_list, panel_labels):
    sub = df[df["T"] == T_val].copy()

    pivot = sub.pivot_table(index="Psi", columns="Omega", values="cost")
    pivot = pivot.sort_index().sort_index(axis=1)

    omega_vals = pivot.columns.values
    psi_vals = pivot.index.values

    im = ax.imshow(
        pivot.values,
        origin="lower",
        vmin=vmin,
        vmax=vmax,
        aspect="auto",
        cmap="viridis"
    )

    ax.set_xticks(np.arange(len(omega_vals)))
    ax.set_xticklabels([str(x) for x in omega_vals])

    ax.set_yticks(np.arange(len(psi_vals)))
    ax.set_yticklabels([str(x) for x in psi_vals])

    # Add panel label below each subplot
    ax.text(
        0.5, -0.20,
        panel_label,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=16,
        fontfamily="Times New Roman"
    )

# ===== 4. Set shared axis labels =====
axes[1].set_xlabel("Ω (unit emergency cost multiplier)")
axes[0].set_ylabel("Ψ (shortage allowance multiplier)")

# ===== 5. Add colorbar =====
fig.subplots_adjust(right=0.88, bottom=0.25, wspace=0.25)

cbar_ax = fig.add_axes([0.90, 0.25, 0.02, 0.60])
cbar = fig.colorbar(im, cax=cbar_ax)
cbar.set_label("Optimal total relief cost (unit: 10⁸ CNY)")

# ===== 6. Save figure =====
fig.savefig("Figure_9_heatmaps_T2_T4_T6.pdf", dpi=300, bbox_inches="tight")
plt.show()