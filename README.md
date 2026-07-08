# Computational Materials

This repository provides the computational-supporting materials for the manuscript:

**Adaptive relief logistics for predictable disasters: Integrating professional vehicles with flexible crowdshipping**

submitted to the **European Journal of Operational Research**.

## Repository structure

```text
├── README.md
├── data/
│   └── EJOR\_Data for numerical analysis.xlsx
├── scripts/
│   ├── fig6\_trc\_vs\_T\_rho.py
│   ├── fig7\_cost\_components\_vs\_T\_rho6.py
│   ├── fig8\_relative\_cost\_increase\_vs\_T.py
│   ├── fig9\_heatmaps\_cost\_vs\_omega\_psi.py
│   ├── fig10\_Tstar\_vs\_crowdparams.py
│   ├── fig11\_total\_cost\_vs\_crowdparams.py
│   ├── figD1\_TRC\_vs\_T\_rho.py
│   └── random\_network\_generation.py
├── generated\_instances/
│   ├── instance\_rep\_1\_seed\_5000/
│   ├── instance\_rep\_2\_seed\_6000/
│   ├── instance\_rep\_3\_seed\_7000/
│   ├── instance\_rep\_4\_seed\_8000/
│   └── instance\_rep\_5\_seed\_9000/
```

## Data file

The file `data/EJOR\_Data for numerical analysis.xlsx` contains the detailed numerical results used in the revised manuscript and Supplementary Material.

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

Please run the scripts from the root directory of this repository.

```bash
python scripts/fig6\_trc\_vs\_T\_rho.py
python scripts/fig7\_cost\_components\_vs\_T\_rho6.py
python scripts/fig8\_relative\_cost\_increase\_vs\_T.py
python scripts/fig9\_heatmaps\_cost\_vs\_omega\_psi.py
python scripts/fig10\_Tstar\_vs\_crowdparams.py
python scripts/fig11\_total\_cost\_vs\_crowdparams.py
python scripts/figD1\_TRC\_vs\_T\_rho.py
```

The scripts read the corresponding worksheets in `data/EJOR\_Data for numerical analysis.xlsx` and generate the figures reported in the revised manuscript and Supplementary Material.

## Random instance generation

The script `scripts/random\_network\_generation.py` generates random spatial instances used in the algorithmic experiments.

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
python scripts/random\_network\_generation.py
```

By default, the script uses the following random seeds:

```text
5000, 6000, 7000, 8000, 9000
```

The generated files are stored in:

```text
generated\_instances/
├── instance\_rep\_1\_seed\_5000/
├── instance\_rep\_2\_seed\_6000/
├── instance\_rep\_3\_seed\_7000/
├── instance\_rep\_4\_seed\_8000/
└── instance\_rep\_5\_seed\_9000/
```

Each folder contains the generated data for one random replicate, including files such as:

```text
node\_coordinates.csv
trajectory\_scenarios.csv
affected\_demand\_points\_tau\_\*.csv
demand\_point\_population.csv
nominal\_demand.csv
generation\_settings.csv
network\_rep\_\*\_seed\_\*.png
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

These parameters can be modified in the `NetworkConfig` settings in `random\_network\_generation.py`.

## Notes

The optimization results reported in the manuscript are provided in `data/EJOR\_Data for numerical analysis.xlsx`. The scripts and generated files in this repository are intended to help readers trace the numerical results, reproduce the reported figures from the provided data, and verify the random instance-generation and data-processing procedures.

