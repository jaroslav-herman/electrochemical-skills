"""Reference template for comparing IV/SV performance evolution across samples."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import wepy.basics as we
import wepy.iv_curve as weiv


DATA_ROOT = Path(r"\\ELECTROLYZER\PEM-WE_measurements\2026")
SAMPLE_IDS = ("453", "455", "457")  # Replace with IDs selected from the live sheet.
CELL_VOLTAGES = (1.6, 1.8, 2.0)
OUTPUT_DIR = Path("results")


def sample_folders() -> dict[str, Path]:
    folders = we.load_folders(
        str(DATA_ROOT), contains_string=list(SAMPLE_IDS), natural_sort=True, mode="any"
    )
    if isinstance(folders, str):
        raise FileNotFoundError(folders)
    result = {}
    for sample_id in SAMPLE_IDS:
        matches = [
            Path(folder)
            for folder in folders
            if Path(folder).name.startswith(f"{sample_id}_")
            or Path(folder).name == sample_id
        ]
        if len(matches) != 1:
            raise FileNotFoundError(f"Expected one folder for {sample_id}, found {matches}")
        result[sample_id] = matches[0]
    return result


def evolution(folder: Path) -> dict[float, list[float]]:
    files = we.load_files(
        str(folder), contains_string="SV", extension=".mpr", natural_sort=True
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
        figure, axis = plt.subplots(figsize=(6.5, 4.5))
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
        axis.legend(frameon=False)
        figure.tight_layout()
        figure.savefig(OUTPUT_DIR / f"performance_evolution_{target:g}V.png", dpi=300)
        plt.close(figure)


if __name__ == "__main__":
    main()
