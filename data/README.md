# Preparing the experimental data

Source: Wang, Hilbe, and Zhang (2026), *The dynamics of cooperation in asymmetric public goods games*.
Original data and code: [Zenodo record 16918146](https://doi.org/10.5281/zenodo.16918146).
The supplied project source manifest records the deposit as CC BY 4.0.
The authors' raw data are not bundled with this repository.

## One-time setup

1. Download **LinearPGG_4P_ExperimentalData.mat** from the Zenodo record above.
2. From the repository root, install the Python dependencies:

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Convert the downloaded file (replace the example path with its actual location):

   ```sh
   python code_python/01_prepare_data.py --mat "path/to/LinearPGG_4P_ExperimentalData.mat"
   ```

4. Open `code_python/00_replication.ipynb`, restart the kernel, and run all cells.
   The same generated CSV is also the input to `Rscript code_R/00_run_all.R`.

The converter writes `data/LinearPGG_4P_ExperimentalData.csv` with seven columns:
`Treatment`, `Session`, `GroupID`, `PlayerID`, `GlobalPlayerID`, `Round`, `Contribution`.
It verifies the source SHA-256, field names, shape, integer values, unique observation keys,
treatment counts, complete four-player groups, twenty rounds, and contribution bounds.
It stops rather than silently overwriting a CSV with different content. An existing equivalent
CSV is accepted without changing its bytes.

## Scope and verification

This is a file-specific converter for the checksum-pinned author MATLAB table, using SciPy's
private MATLAB reader. It is **not** a general-purpose MATLAB table importer. Python 3.12.14,
SciPy 1.17.0, pandas 2.2.3 and NumPy 2.3.5 were used for release verification.
During preparation, all **12,480 rows × 7 fields** were compared with the pre-existing project
CSV and matched, ignoring storage dtype. No observations were dropped or values imputed.
The converter reports the input checksum and output dimensions when run.

The generated CSV and downloaded MATLAB file are local inputs excluded from version control.
Preserve the source attribution when using or sharing author data.
