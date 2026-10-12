"""Plot population against area using the CSV exported by the client."""

import pandas as pd
import matplotlib.pyplot as plt


def create_scatter_plot():
    country_dataframe = pd.read_csv("exported_countries.csv")

    plt.scatter(country_dataframe["population"], country_dataframe["area"])
    plt.title("Country Population vs Area")
    plt.xlabel("Population")
    plt.ylabel("Area (sq. km)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("population_vs_area.png")
    print("Saved population_vs_area.png")
    plt.show()


if __name__ == "__main__":
    create_scatter_plot()
