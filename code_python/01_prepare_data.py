"""Convert the pinned author linear-PGG MATLAB table to the replication CSV.

This decodes one known MCOS table layout using SciPy's private MATLAB reader.
It deliberately rejects other files; it is not a generic MATLAB table reader.
Source: https://doi.org/10.5281/zenodo.16918146 (Wang, Hilbe & Zhang, 2026).
The layout is adapted from this repository's abm_extension/prepare_data.py.
"""

import argparse
import hashlib
import io
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat
from scipy.io.matlab import _mio5

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = "dcdd23e709ce1c17fadddffb84d07b9cf2f37a0a206e4665317aed31fd4e790b"
FIELDS = [
    "Treatment", "Session", "GroupID", "PlayerID",
    "GlobalPlayerID", "Round", "Contribution",
]
ROWS = 12480


def decode_author_table(path):
    """Read and check the exact deposited MATLAB table before exposing its columns."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError("Source SHA-256 does not match the pinned author deposit.")
    data = loadmat(path)
    # SciPy releases expose MCOS tables either as MatlabOpaque or class metadata.
    if "all_data" in data:
        assert str(data["all_data"]["_Class"][0]) == "table", "Expected a MATLAB table."
    else:
        opaque = data.get("None")
        assert opaque is not None and opaque.dtype.names == ("s0", "s1", "s2", "arr")
        assert opaque["s0"][0] == b"all_data" and opaque["s2"][0] == b"table"
    raw = data["__function_workspace__"].tobytes()
    assert raw[:8] == b"\x00\x01IM\x00\x00\x00\x00", "Unexpected workspace header."
    stream = io.BytesIO(raw)
    reader = _mio5.MatFile5Reader(stream, byte_order="<")
    reader.initialize_read()
    stream.seek(8)
    header, _ = reader.read_var_header()
    decoded = reader.read_var_array(header, process=True)
    wrapper = decoded["MCOS"][0, 0]
    if "_ObjectMetadata" in wrapper.dtype.names:
        metadata = wrapper["_ObjectMetadata"][0]
    else:
        assert wrapper["s2"][0] == b"FileWrapper__", "Unexpected workspace wrapper."
        metadata = wrapper["arr"][0]
    assert metadata.shape == (11, 1), "Unexpected table metadata."
    assert metadata[4, 0].item() == ROWS and metadata[6, 0].item() == 7
    names = [str(x.item()) for x in metadata[7, 0].flat]
    assert names == FIELDS, "Unexpected field order."
    columns = metadata[2, 0]
    assert columns.shape == (1, 7)
    values = {}
    for name, column in zip(names, columns.flat):
        assert column.shape == (ROWS, 1), "Unexpected column dimensions."
        if name == "Treatment":
            values[name] = [str(x.item()) for x in column.flat]
        else:
            assert np.isfinite(column).all(), "Non-finite values."
            assert np.equal(column, np.floor(column)).all(), "Expected integers."
            values[name] = column.reshape(-1).astype(int)
    return pd.DataFrame(values)


def validate(data):
    """Check observation units and game constraints without dropping observations."""
    group = ["Treatment", "Session", "GroupID"]
    key = group + ["PlayerID", "Round"]
    assert data.shape == (ROWS, 7) and list(data.columns) == FIELDS
    assert not data.isna().any().any(), "Missing input values."
    assert not data.duplicated(key).any(), "Duplicate player-round keys."
    assert set(data["Treatment"]) == {"FE", "AI", "MI"}
    assert set(data["Session"]) == {1, 2}
    assert data[group].drop_duplicates().groupby("Treatment").size().to_dict() == {
        "AI": 52, "FE": 50, "MI": 54,
    }
    for _, player in data.groupby(group + ["PlayerID"]):
        assert len(player) == 20 and set(player["Round"]) == set(range(1, 21))
    for _, round_data in data.groupby(group + ["Round"]):
        assert len(round_data) == 4 and set(round_data["PlayerID"]) == {1, 2, 3, 4}
    endowment = np.where(
        data["Treatment"].eq("FE"), 24,
        np.where(data["PlayerID"].isin([1, 2]), 36, 12),
    )
    assert data["Contribution"].between(0, endowment).all(), "Invalid contribution."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mat", type=Path, required=True, help="Downloaded author MATLAB file.")
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / "data/LinearPGG_4P_ExperimentalData.csv",
    )
    args = parser.parse_args()
    data = decode_author_table(args.mat)
    validate(data)
    if args.output.exists():
        existing = pd.read_csv(args.output)
        pd.testing.assert_frame_equal(data, existing, check_dtype=False)
        print("Existing CSV is equivalent; its bytes were preserved.")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(args.output, index=False)
        print("Wrote CSV:", args.output)
    print(f"PASS: {len(data):,} rows, {len(data.columns)} columns; no exclusions.")
    print("Source SHA-256:", SOURCE_SHA256)


if __name__ == "__main__":
    main()
