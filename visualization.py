"""Plot population against area using the CSV exported by the client."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_FOLDER = Path(__file__).resolve().parent
CSV_FILE = PROJECT_FOLDER / "exported_countries.csv"
PLOT_FILE = PROJECT_FOLDER / "population_vs_area.png"


def create_scatter_plot():
    country_dataframe = pd.read_csv(CSV_FILE)

    figure, axis = plt.subplots(figsize=(9, 6))
    axis.scatter(
        country_dataframe["population"],
        country_dataframe["area"],
        s=65,
        alpha=0.8,
        edgecolors="white",
        linewidth=0.6,
    )

    # Log scales keep smaller countries visible alongside the largest outliers.
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_title("Country Population vs Area")
    axis.set_xlabel("Population (log scale)")
    axis.set_ylabel("Area (sq. km, log scale)")
    axis.grid(True, which="major", alpha=0.55)
    axis.grid(True, which="minor", linestyle=":", alpha=0.3)
    figure.tight_layout()
    figure.savefig(PLOT_FILE, dpi=160)
    print(f"Saved {PLOT_FILE.name}")
    plt.show()


if __name__ == "__main__":
    create_scatter_plot()