"""Verify the team environment without requiring access to measurement data."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / ".matplotlib"))

import matplotlib
import numpy
import pandas
import scipy

import wepy
from wepy import basics

matplotlib.rcParams["text.usetex"] = False


def main() -> None:
    mpt = "\n".join(
        [
            "EC-Lab ASCII FILE",
            "Nb header lines : 3",
            "cycle number\tcontrol/V\t<I>/mA",
            "1\t1.5\t100",
            "1\t1.6\t200",
            "1\t1.7\t300",
        ]
    )
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "fixture.mpt"
        path.write_text(mpt, encoding="latin1")
        data = basics.read_file(path)
    if data.empty or "control/V" not in data or "<I>/mA" not in data:
        raise RuntimeError("The .mpt fixture did not load correctly")

    root = os.environ.get("ELECTROCHEMICAL_DATA_ROOT", "not configured")
    print(f"wepy={wepy.__version__}")
    print(f"numpy={numpy.__version__}, pandas={pandas.__version__}, scipy={scipy.__version__}")
    print(f"matplotlib={matplotlib.__version__}, text.usetex={matplotlib.rcParams['text.usetex']}")
    print(f"data_root={root}")


if __name__ == "__main__":
    main()
