# Replication code

**Start here: [Python replication notebook](python/00_replication.ipynb)** — data validation, treatment comparisons, and Figures 4A–4C.

| Language | Entry point | Supporting scripts |
| --- | --- | --- |
| Python | [00_replication.ipynb](python/00_replication.ipynb) | Self-contained notebook |
| R | [00_run_all.R](r/00_run_all.R) | [01_import.R](r/01_import.R), [02_derive_variables.R](r/02_derive_variables.R), [03_replication.R](r/03_replication.R) |

Names use lowercase snake_case with two-digit execution-order prefixes; R scripts retain the conventional `.R` extension. The Python notebook can run from the repository root or its own directory. Run the R entry point from the repository root with `Rscript code/r/00_run_all.R`.

Inputs remain in the root `data/` directory; figures remain in `figures/` (R) and `figures/python/` (Python). See the [repository overview](../README.md) for dependencies, data preparation, and research limitations.

The independent [ABM extension](../abm_extension/README.md) retains its own Python package, tests, R comparison, and run instructions.
