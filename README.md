# Asymmetric Public-Goods Experiment Replication

This repository contains an ongoing replication and extension of Wang, Hilbe, and Zhang (2026), *The dynamics of cooperation in asymmetric public goods games*, using R and Python.

The experimental replication focuses on the four-player linear public-goods game and compares three treatments: full equality (FE), aligned inequality (AI), and misaligned inequality (MI).

## Current Progress

- Imported a dataset with 12,480 player-round observations.
- Checked missing values, duplicate records, group size, player roster, round completeness, and contribution bounds.
- Constructed contribution, payoff, and surplus measures.
- Produced Figures 4A–4D in R.
- Produced Figures 4A–4C in Python. Figure 4D is not included in Python yet.

The project is still in progress. Producing the figures does not mean that every detail of the original analysis has been verified.

## Repository Structure

- `R/00_run_all.R`: runs the R scripts in order.
- `R/01_import.R`: imports and checks the data.
- `R/02_derive_variables.R`: constructs analysis variables.
- `R/03_replication.R`: runs comparisons and produces figures.
- `replication_python.ipynb`: Python replication notebook.
- `figures/`: R replication figures.
- `figures/python/`: Python replication figures.
- `data/`: local data and data source notes.
- `abm_extension/`: a separate agent-based modeling extension.

## Data

Original data and code are available on [Zenodo](https://doi.org/10.5281/zenodo.16918146).

Raw experimental data are not included in this repository. Put `LinearPGG_4P_ExperimentalData.csv` in `data/` before running the replication. See `data/README.md` for the data source.

The CSV should contain:

`Treatment`, `Session`, `GroupID`, `PlayerID`, `GlobalPlayerID`, `Round`, and `Contribution`.

The replication scripts read the prepared CSV. They do not convert the authors' original MATLAB file to CSV.

## Running the Replication

### R

The R replication uses `ggplot2`.

Run the scripts from the repository root, starting with `R/00_run_all.R`. Data paths should be relative to the repository root.

### Python

The notebook uses pandas, NumPy, Matplotlib, and SciPy.

Open `replication_python.ipynb` in a Jupyter-compatible environment with the repository root as the current working directory. Restart the kernel and run all cells in order.

The notebook saves:

- `figures/python/figure_4a.png`: average group relative contribution.
- `figures/python/figure_4b.png`: group relative contribution across rounds.
- `figures/python/figure_4c.png`: overall surplus.

## Python Replication Notes

Treatment comparisons use group-session averages over the first 20 rounds. The main outcomes are group relative contribution and overall surplus. Average payoff comparisons are extra checks.

The reported p-values are unadjusted. The paper uses Bonferroni correction, but the number of comparisons is unclear in the supplement. Unadjusted p-values below 0.05 should therefore not automatically be described as significant.

For Figures 4A and 4C, error bars use mean ± 1.96 × SE, based on group-session averages. The authors' exact confidence interval method has not been confirmed. These intervals do not adjust for participants taking part in both sessions.

## Agent-Based Modeling Extension

A separate Python model and R comparison are available in [abm_extension/](abm_extension/README.md).

The extension covers FE, AI, and MI treatments in both linear and threshold games. It uses published two-player learning parameters without fitting them to the four-player outcomes.

The model does not reproduce all experimental patterns. It underpredicts contributions in the linear MI treatment, overpredicts threshold success under inequality, and remains sensitive to initialization. Behavioral validation and my review of the implementation are ongoing.

See [results and limitations](abm_extension/RESULTS.md) for details.