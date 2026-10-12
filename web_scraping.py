"""Scrape the first 20 country records from the project page."""

import requests
from bs4 import BeautifulSoup


COUNTRIES_URL = "https://www.scrapethissite.com/pages/simple/"


def scrape_countries():
    response = requests.get(COUNTRIES_URL, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    country_divs = soup.select(".country")[:20]

    countries = []
    for country_div in country_divs:
        country_name = country_div.select_one(".country-name").get_text(strip=True)
        capital = country_div.select_one(".country-capital").get_text(strip=True)
        population = int(country_div.select_one(".country-population").get_text(strip=True))
        area = float(country_div.select_one(".country-area").get_text(strip=True))

        country = {
            "country_name": country_name,
            "capital": capital,
            "population": population,
            "area": area,
        }
        countries.append(country)

    return countries


if __name__ == "__main__":
    country_list = scrape_countries()
    for country in country_list:
        print(country)
