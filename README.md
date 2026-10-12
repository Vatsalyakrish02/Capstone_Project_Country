# Country Data Explorer

This project is a small Python capstone that collects information about 20 countries, saves it in a database, and turns it into a CSV file and a chart. The dashboard brings the results together in one browser page.

## What the project does

When you run the workflow from the dashboard, it:

1. Collects the first 20 country records from [Scrape This Site](https://www.scrapethissite.com/pages/simple/).
2. Saves the country name, capital, population, and area in a SQLite database.
3. Makes the records available through a FastAPI service.
4. Fetches the API data and writes `exported_countries.csv`.
5. Creates `population_vs_area.png`, a scatter plot of population and area.

The country name is used as the database key. If a country is already in the database, the workflow updates its record instead of adding a duplicate.

## Run it on Windows

Open PowerShell in this project folder, then create and activate the virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the packages used by the project:

```powershell
python -m pip install fastapi uvicorn requests beautifulsoup4 pandas matplotlib
```

Start the dashboard:

```powershell
python dashboard.py
```

The dashboard should open in your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000). If it does not, open that address yourself. Select the button to run the workflow. Keep the PowerShell window open while using the dashboard; press `Ctrl+C` there when you are finished.

The scraper needs an internet connection to reach the source page.

## API routes

The API is part of the dashboard server. You can view and try the routes at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/countries` | List all countries |
| `GET` | `/countries/{country_name}` | Look up one country by name |
| `POST` | `/countries` | Add a country |
| `PUT` | `/countries/{country_name}` | Update a country's capital, population, and area |
| `DELETE` | `/countries/{country_name}` | Delete a country |

## Project files

- `web_scraping.py` collects the country information.
- `database_handling.py` creates and works with the SQLite database.
- `country_fastapi.py` defines the API and its routes.
- `client.py` reads country data from the API and exports the CSV.
- `visualization.py` builds the scatter plot from the CSV.
- `dashboard.py` connects the modules and serves the browser page.

## Files created by the workflow

- `countries.db` — the SQLite database.
- `exported_countries.csv` — the country data exported by the client.
- `population_vs_area.png` — the population-versus-area chart.

The `.gitignore` file keeps the virtual environment and Python cache files out of Git.