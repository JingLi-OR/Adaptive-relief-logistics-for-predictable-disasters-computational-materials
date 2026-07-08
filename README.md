# Computational Materials

This repository provides the computational-supporting materials for the manuscript:

**Adaptive relief logistics for predictable disasters: Integrating professional vehicles with flexible crowdshipping**

submitted to the **European Journal of Operational Research**.

## Repository structure

```text
├── README.md
├── data/
│   └── EJOR_Data for numerical analysis.xlsx
├── scripts/
│   ├── fig6_trc_vs_T_rho.py
│   ├── fig7_cost_components_vs_T_rho6.py
│   ├── fig8_relative_cost_increase_vs_T.py
│   ├── fig9_heatmaps_cost_vs_omega_psi.py
│   ├── fig10_Tstar_vs_crowdparams.py
│   ├── fig11_total_cost_vs_crowdparams.py
│   ├── figD1_TRC_vs_T_rho.py
│   └── random_network_generation.py
├── generated_instances/
│   ├── instance_rep_1_seed_5000/
│   ├── instance_rep_2_seed_6000/
│   ├── instance_rep_3_seed_7000/
│   ├── instance_rep_4_seed_8000/
│   └── instance_rep_5_seed_9000/
```

## Data file

The file `data/EJOR_Data for numerical analysis.xlsx` contains the detailed numerical results used in the revised manuscript and Supplementary Material.

The workbook includes separate worksheets corresponding to the numerical experiments, including:

* case-study experiments;
* planning-horizon analysis;
* cost-decomposition analysis;
* sensitivity analyses;
* randomly generated instances;
* fixed-information experiment in Appendix D.

These worksheets provide the data used to generate the reported tables and figures, including objective values, cost components, parameter settings, optimal numbers of periods, relative cost increases, optimality gaps, and computational times where applicable.

## Python requirements

The scripts were prepared using Python 3. The following packages are required:

```text
pandas
openpyxl
numpy
matplotlib
shapely
```

They can be installed with:

```bash
pip install pandas openpyxl numpy matplotlib shapely
```

## Reproducing the numerical figures

The scripts in the `scripts/` folder can be used to reproduce the main numerical figures from the provided Excel workbook.

```bash
python scripts/fig6_trc_vs_T_rho.py
python scripts/fig7_cost_components_vs_T_rho6.py
python scripts/fig8_relative_cost_increase_vs_T.py
python scripts/fig9_heatmaps_cost_vs_omega_psi.py
python scripts/fig10_Tstar_vs_crowdparams.py
python scripts/fig11_total_cost_vs_crowdparams.py
python scripts/figD1_TRC_vs_T_rho.py
```


## Random instance generation

The script `scripts/random_network_generation.py` generates random spatial instances used in the algorithmic experiments.

It generates:

* node coordinates;
* typhoon trajectory scenarios;
* affected demand points;
* demand point population data;
* nominal demand records;
* generation-setting files;
* representative network figures.

To run the script:

```bash
python scripts/random_network_generation.py
```

By default, the script uses the following random seeds:

```text
5000, 6000, 7000, 8000, 9000
```

The generated files are stored in:

```text
generated_instances/
├── instance_rep_1_seed_5000/
├── instance_rep_2_seed_6000/
├── instance_rep_3_seed_7000/
├── instance_rep_4_seed_8000/
└── instance_rep_5_seed_9000/
```

Each folder contains the generated data for one random replicate, including files such as:

```text
node_coordinates.csv
trajectory_scenarios.csv
affected_demand_points_tau_*.csv
demand_point_population.csv
nominal_demand.csv
generation_settings.csv
network_rep_*_seed_*.png
```

## Adjustable parameters

The random instance-generation script allows users to adjust the instance size and configuration, including:

* number of MDCs;
* number of SAs;
* number of commodity suppliers;
* number of carrier suppliers;
* number of demand points;
* number of trajectory path points;
* number of planning periods;
* period length;
* random seed.

These parameters can be modified in the `NetworkConfig` settings in `random_network_generation.py`.

## Notes

The optimization results reported in the manuscript are provided in `data/EJOR_Data for numerical analysis.xlsx`. The scripts and generated files in this repository are intended to help readers trace the numerical results, reproduce the reported figures from the provided data, and verify the random instance-generation and data-processing procedures.

