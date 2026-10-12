"""Fetch countries from the API, display them, and export them to CSV."""

import pandas as pd
import requests


API_URL = "http://127.0.0.1:8000/countries"


def export_countries():
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()

    country_data = response.json()
    country_dataframe = pd.DataFrame(country_data)

    print(country_dataframe)
    country_dataframe.to_csv("exported_countries.csv", index=False)
    print("Saved exported_countries.csv")


if __name__ == "__main__":
    export_countries()
