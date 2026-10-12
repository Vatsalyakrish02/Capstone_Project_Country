# Country Data Explorer

This project collects information about the first 20 countries on [Scrape This Site](https://www.scrapethissite.com/pages/simple/), stores the records in SQLite, serves them through a FastAPI API, and exports a CSV and chart. The dashboard is the quickest way to run the full workflow. The individual commands are included below as well, so each capstone phase can be run and reviewed on its own.

## Set up the project

Open PowerShell in the project folder. Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the packages used by the project:

```powershell
python -m pip install fastapi uvicorn requests beautifulsoup4 pandas matplotlib
```

The scraper needs an internet connection to reach its source page.

## Option 1: Run the dashboard

This is the simplest way to run the full workflow. From the project folder, start the dashboard:

```powershell
python dashboard.py
```

It should open in your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000). If it does not, open that address yourself and use the page's workflow button. The dashboard runs the scraper, saves the records to SQLite, fetches them through the API, exports the CSV, and creates the chart.

Keep the PowerShell window open while using the dashboard. Press `Ctrl+C` in that window when you are finished.

## Option 2: Run the capstone phases separately

Use this option to follow the project modules one at a time. Run these commands from the project folder, with the virtual environment activated.

First, scrape and display the country records:

```powershell
python web_scraping.py
```

Then save the records to the SQLite database:

```powershell
python database_handling.py
```

Start the API in a separate PowerShell window. In that window, change to the project folder and activate `.venv` before running:

```powershell
uvicorn country_fastapi:app --reload
```

Leave the API running. In the first PowerShell window, fetch the records from the API and create the CSV:

```powershell
python client.py
```

Then create the chart from the CSV:

```powershell
python visualization.py
```

The chart uses logarithmic scales on both axes so countries with smaller populations and areas remain visible alongside the largest values.

## API routes

The API is available while its server is running. The interactive API page is at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/countries` | List all countries |
| `GET` | `/countries/{country_name}` | Look up one country by name |
| `POST` | `/countries` | Add a country |
| `PUT` | `/countries/{country_name}` | Update a country's capital, population, and area |
| `DELETE` | `/countries/{country_name}` | Delete a country |

## Project files

- `web_scraping.py` collects the country information.
- `database_handling.py` creates and manages the SQLite database.
- `country_fastapi.py` defines the API and its routes.
- `client.py` fetches API data and exports it to CSV.
- `visualization.py` creates the population-versus-area chart.
- `dashboard.py` brings the modules together in a browser page.

## Output files

- `countries.db` — the SQLite database, with the country name as its primary key.
- `exported_countries.csv` — country records fetched from the API.
- `population_vs_area.png` — the scatter plot.

The `.gitignore` file excludes the virtual environment and Python cache files from Git.