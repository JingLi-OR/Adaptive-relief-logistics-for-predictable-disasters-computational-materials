# -*- coding: utf-8 -*-
"""
Figure 7: Cost components versus |T| for the baseline case (rho = 6 h)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MaxNLocator

# ===== 1. Read data =====
file_path = "EJOR_Data for numerical analysis.xlsx"
sheet_name = "Section 6.1.1-2"

df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Rename columns for easier use
df = df.rename(columns={
    "|T|": "T",
    "Facility and contract costs": "cost_fac_contract",
    "Procurement costs": "cost_proc",
    "Transportation costs": "cost_trans",
    "Total emergency procurement costs": "cost_epc",
    "TRC_1e8_CNY": "TRC"
})

# ===== 2. Keep the baseline case rho = 6 =====
rho_baseline = 6
sub = df[df["rho"] == rho_baseline].copy()

# Convert data types
sub["rho"] = pd.to_numeric(sub["rho"])
sub["T"] = pd.to_numeric(sub["T"])
sub["cost_fac_contract"] = pd.to_numeric(sub["cost_fac_contract"])
sub["cost_proc"] = pd.to_numeric(sub["cost_proc"])
sub["cost_trans"] = pd.to_numeric(sub["cost_trans"])
sub["cost_epc"] = pd.to_numeric(sub["cost_epc"])

sub = sub.sort_values("T").reset_index(drop=True)

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
    "mathtext.fontset": "custom",
    "mathtext.rm": "Times New Roman",
    "mathtext.it": "Times New Roman:italic",
    "mathtext.bf": "Times New Roman:bold",
})

# ===== 4. Prepare plot settings =====
colors = ["#d95f02", "#7570b3", "#e7298a", "#66a61e"]
markers = ["s", "^", "D", "v"]
linestyles = ["--", "-.", ":", (0, (5, 1))]

series = [
    ("cost_fac_contract", "Facility and contract costs"),
    ("cost_proc", "Procurement costs"),
    ("cost_trans", "Transportation costs"),
    ("cost_epc", "Total emergency procurement costs"),
]

fig, ax = plt.subplots(figsize=(9, 6))

# ===== 5. Plot the cost components =====
for idx, (col, label) in enumerate(series):
    ax.plot(
        sub["T"],
        sub[col],
        marker=markers[idx],
        linestyle=linestyles[idx],
        color=colors[idx],
        linewidth=1.8,
        markersize=6,
        label=label
    )

# ===== 6. Set axes and legend =====
ax.set_xlabel(r"$|\mathcal{T}|$")
ax.set_ylabel("Cost (unit: 10⁸ CNY)")

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.grid(True, linestyle=":", linewidth=0.6, alpha=0.7)

leg = ax.legend(
    loc="best",
    frameon=False,
    prop={"family": "Times New Roman", "size": 16}
)
leg.get_title().set_fontfamily("Times New Roman")

# ===== 7. Save figure =====
fig.tight_layout()
fig.savefig("Figure_7_cost_components_vs_T_rho6.pdf", dpi=300, bbox_inches="tight")
plt.show()