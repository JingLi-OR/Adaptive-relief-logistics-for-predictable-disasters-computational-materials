# -*- coding: utf-8 -*-
"""
Figure 8: Relative cost increase versus |T|

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# ===== 1. Read data =====
file_path = "EJOR_Data for numerical analysis.xlsx"
sheet_name = "Section 6.1.2-1"

df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Rename columns for easier use
df = df.rename(columns={
    "|T|": "T",
    "Relative cost increase": "regret"
})

# Keep required columns
df = df[["OMEGA", "PSI", "T", "total_cost_obj", "best_cost", "regret"]].dropna(
    subset=["OMEGA", "PSI", "T", "regret"]
)

# Convert data types
df["OMEGA"] = pd.to_numeric(df["OMEGA"])
df["PSI"] = pd.to_numeric(df["PSI"])
df["T"] = pd.to_numeric(df["T"]).astype(int)
df["regret"] = pd.to_numeric(df["regret"])

df = df.sort_values(["T", "OMEGA", "PSI"]).reset_index(drop=True)

# ===== 2. Set figure style =====
mpl.rcParams.update({
    "font.family": "Times New Roman",
    "font.serif": ["Times New Roman"],
    "font.size": 15,
    "axes.labelsize": 17,
    "xtick.labelsize": 15,
    "ytick.labelsize": 15,
    "legend.fontsize": 15,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    "mathtext.it": "Times New Roman:italic",
    "mathtext.bf": "Times New Roman:bold",
})

# ===== 3. Prepare boxplot data =====
T_values = sorted(df["T"].unique())
box_data = [df.loc[df["T"] == t, "regret"].values for t in T_values]

# ===== 4. Plot boxplot =====
fig, ax = plt.subplots(figsize=(9, 4.5))

ax.boxplot(
    box_data,
    positions=T_values,
    showfliers=False
)

# ===== 5. Set axes =====
ax.set_xlabel("|T|")
ax.set_ylabel("Relative cost increase")

ax.axhline(0, linestyle="--", linewidth=1.0)
ax.grid(True, linestyle=":", linewidth=0.6, alpha=0.7)

# Use integer ticks on the x-axis
ax.set_xticks(T_values)
ax.set_xticklabels([str(int(t)) for t in T_values])

# ===== 6. Save figure =====
fig.tight_layout()
fig.savefig("Figure_8_relative_cost_increase_vs_T.pdf", dpi=300, bbox_inches="tight")
plt.show()