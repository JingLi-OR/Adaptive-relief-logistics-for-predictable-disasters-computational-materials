# -*- coding: utf-8 -*-
"""
Figure 6: TRC versus |T| under different rho values

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

# ===== 1. Read data =====
file_path = "EJOR_Data for numerical analysis.xlsx"
sheet_name = "Section 6.1.1-1"

df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Rename columns for easier use
df = df.rename(columns={
    "|T|": "T",
    "TRC_1e8_CNY": "TRC"
})

# Keep required columns
df = df[["rho", "T", "TRC", "is_lowest_TRC"]].dropna(subset=["rho", "T", "TRC"])

df["rho"] = df["rho"].astype(int)
df["T"] = df["T"].astype(int)
df["TRC"] = df["TRC"].astype(float)

df = df.sort_values(["rho", "T"]).reset_index(drop=True)

# ===== 2. Identify the lowest TRC =====
lowest_flag = df["is_lowest_TRC"].astype(str).str.upper().eq("TRUE")

if lowest_flag.any():
    best = df.loc[lowest_flag].iloc[0]
else:
    best = df.loc[df["TRC"].idxmin()]

print(
    "Best (rho, |T|):",
    int(best["rho"]),
    int(best["T"]),
    "TRC =",
    best["TRC"],
    "(10^8 CNY)"
)

# ===== 3. Set figure style =====
mpl.rcParams.update({
    "font.family": "Times New Roman",
    "font.serif": ["Times New Roman"],
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.fontsize": 16,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,

    # Use Times New Roman for math text where possible
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    "mathtext.it": "Times New Roman:italic",
    "mathtext.bf": "Times New Roman:bold",
})

fig, ax = plt.subplots(figsize=(9, 6))

colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e"]
markers = ["o", "s", "^", "D", "v"]
linestyles = ["-", "--", "-.", ":", (0, (5, 1))]

# ===== 4. Plot TRC curves =====
for (rho_value, g), c, m, ls in zip(df.groupby("rho"), colors, markers, linestyles):
    g = g.sort_values("T")

    ax.plot(
        g["T"],
        g["TRC"],
        marker=m,
        markersize=5.5,
        linewidth=1.8,
        linestyle=ls,
        color=c,
        label=f"ρ = {rho_value} h"
    )

# ===== 5. Mark the lowest TRC =====
ax.scatter(
    best["T"],
    best["TRC"],
    marker="*",
    color="black",
    s=100,
    zorder=5
)

ax.annotate(
    "lowest TRC",
    xy=(best["T"], best["TRC"]),
    xytext=(5, 8),
    textcoords="offset points",
    fontsize=14,
    fontfamily="Times New Roman"
)

# ===== 6. Set axes =====
ax.set_xlabel(r"$|\mathcal{T}|$")
ax.set_ylabel("Total relief cost (TRC, unit: 10⁸ CNY)")

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.grid(True, linestyle=":", linewidth=0.7, alpha=0.6)

# ===== 7. Set legend =====
leg = ax.legend(
    title="Period length",
    frameon=False,
    loc="upper right",
    prop={"family": "Times New Roman", "size": 16}
)

leg.get_title().set_fontfamily("Times New Roman")
leg.get_title().set_fontsize(16)

# ===== 8. Save figure =====
fig.tight_layout()
fig.savefig("Figure_6_TRC_vs_T_rho.pdf", dpi=300, bbox_inches="tight")
plt.show()
