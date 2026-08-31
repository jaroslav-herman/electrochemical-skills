"""Reference template for comparing IV/SV performance evolution across samples."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / ".matplotlib"))
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams["text.usetex"] = False

import wepy.basics as we
import wepy.iv_curve as weiv
from measurement_paths import candidate_measurement_roots


YEAR = 2026
FILE_EXTENSION = os.environ.get("ELECTROCHEMICAL_FILE_EXTENSION", ".mpr").lower()
SAMPLE_IDS = ("453", "455", "457")  # Replace with IDs selected from the live sheet.
# Populate from the live sheet. Missing/blank values search both year locations.
SAMPLE_TYPES: dict[str, str] = {}
CELL_VOLTAGES = (1.6, 1.8, 2.0)
OUTPUT_DIR = Path("results")


def sample_folders() -> dict[str, Path]:
    result = {}
    for sample_id in SAMPLE_IDS:
        matches = []
        for root in candidate_measurement_roots(YEAR, SAMPLE_TYPES.get(sample_id)):
            folders = we.load_folders(
                str(root), contains_string=sample_id, natural_sort=True, mode="any"
            )
            if not isinstance(folders, str):
                matches.extend(
                    Path(folder)
                    for folder in folders
                    if Path(folder).name.startswith(f"{sample_id}_")
                    or Path(folder).name == sample_id
                )
        if len(matches) != 1:
            raise FileNotFoundError(f"Expected one folder for {sample_id}, found {matches}")
        result[sample_id] = matches[0]
    return result


def evolution(folder: Path) -> dict[float, list[float]]:
    files = we.load_files(
        str(folder), contains_string="SV", extension=FILE_EXTENSION, natural_sort=True
    )
    values = {voltage: [] for voltage in CELL_VOLTAGES}
    for file in files:
        data = we.read_file_safe(file)
        if data is None:
            continue
        voltages, currents = weiv.IV_curves_data(data)
        for voltage_curve, current_curve in zip(voltages, currents):
            for target in CELL_VOLTAGES:
                index = int(np.abs(voltage_curve - target).argmin())
                values[target].append(float(current_curve[index]))
    return values


def main() -> None:
    folders = sample_folders()
    colors = we.get_colors(len(SAMPLE_IDS))
    data = {sample_id: evolution(folder) for sample_id, folder in folders.items()}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for target in CELL_VOLTAGES:
        figure, axis = plt.subplots(figsize=(12, 4.8))
        for sample_id, color in zip(SAMPLE_IDS, colors):
            values = data[sample_id][target]
            if values:
                axis.plot(
                    range(1, len(values) + 1),
                    values,
                    "o-",
                    color=color,
                    label=sample_id,
                )
        axis.set_xlabel("Measurement sequence")
        axis.set_ylabel("Current (mA)")
        axis.set_title(f"Performance evolution at {target:g} V")
        axis.legend(
            frameon=False,
            loc="upper left",
            bbox_to_anchor=(1.02, 1.0),
            borderaxespad=0.0,
        )
        figure.subplots_adjust(right=0.56)
        figure.savefig(OUTPUT_DIR / f"performance_evolution_{target:g}V.png", dpi=300)
        plt.close(figure)


if __name__ == "__main__":
    main()
