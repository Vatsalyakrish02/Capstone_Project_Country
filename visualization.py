"""Plot population against area using the CSV exported by the client."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import LogFormatterMathtext, LogLocator


PROJECT_FOLDER = Path(__file__).resolve().parent
CSV_FILE = PROJECT_FOLDER / "exported_countries.csv"
PLOT_FILE = PROJECT_FOLDER / "population_vs_area.png"
LABEL_OFFSETS = {
    "Andorra": (10, 14),
    "United Arab Emirates": (-12, 20),
    "Afghanistan": (8, 8),
    "Antigua and Barbuda": (8, -18),
    "Anguilla": (8, 7),
    "Albania": (-8, 16),
    "Armenia": (8, -18),
    "Angola": (-8, -7),
    "Antarctica": (8, -12),
    "Argentina": (8, 8),
    "American Samoa": (-10, 22),
    "Austria": (12, 22),
    "Australia": (8, 8),
    "Aruba": (12, -20),
    "Åland": (8, 8),
    "Azerbaijan": (12, -22),
    "Bosnia and Herzegovina": (-12, -26),
    "Barbados": (8, 8),
    "Bangladesh": (-8, 8),
    "Belgium": (8, -8),
}


def create_scatter_plot():
    country_dataframe = pd.read_csv(CSV_FILE)

    figure, axis = plt.subplots(figsize=(11, 7))
    axis.scatter(
        country_dataframe["population"],
        country_dataframe["area"],
        s=65,
        alpha=0.8,
        edgecolors="white",
        linewidth=0.6,
    )

    # Label each point with its country name; offsets separate nearby records.
    for _, country in country_dataframe.iterrows():
        country_name = country["country_name"]
        offset_x, offset_y = LABEL_OFFSETS.get(country_name, (7, 7))
        horizontal_alignment = "left" if offset_x > 0 else "right"
        vertical_alignment = "bottom" if offset_y > 0 else "top"
        axis.annotate(
            country_name,
            (country["population"], country["area"]),
            xytext=(offset_x, offset_y),
            textcoords="offset points",
            ha=horizontal_alignment,
            va=vertical_alignment,
            fontsize=7.5,
        )

    # Symmetric-log keeps a zero population visible while compressing large values.
    axis.set_xscale("symlog", linthresh=10_000)
    axis.set_yscale("log")
    axis.yaxis.set_major_locator(LogLocator(base=10))
    axis.yaxis.set_major_formatter(LogFormatterMathtext(base=10))
    axis.set_title("Country Population vs Area")
    axis.set_xlabel("Population (symmetric log scale)")
    axis.set_ylabel("Area (sq. km, log scale)")
    axis.grid(True, which="major", alpha=0.55)
    axis.grid(True, which="minor", linestyle=":", alpha=0.3)
    figure.tight_layout()
    figure.savefig(PLOT_FILE, dpi=160)
    print(f"Saved {PLOT_FILE.name}")
    if "agg" not in plt.get_backend().lower():
        plt.show()


if __name__ == "__main__":
    create_scatter_plot()