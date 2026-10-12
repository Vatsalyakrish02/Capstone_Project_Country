"""Dashboard page and workflow launcher for the separate capstone modules."""

import threading
import time
import webbrowser
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import uvicorn
from fastapi import HTTPException
from fastapi.responses import FileResponse, HTMLResponse

from client import export_countries
from country_fastapi import app, country_database
from database_handling import load_scraped_countries
from visualization import create_scatter_plot


PROJECT_FOLDER = Path(__file__).resolve().parent
CSV_FILE = PROJECT_FOLDER / "exported_countries.csv"
PLOT_FILE = PROJECT_FOLDER / "population_vs_area.png"


HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Country Field Notes</title>
  <style>
    :root {
      --paper: #f6f4ee;
      --card: #fffefa;
      --ink: #26382f;
      --muted: #758078;
      --line: #e5e5d9;
      --forest: #365c49;
      --forest-dark: #294636;
      --sage: #e9eee5;
      --ochre: #c48645;
      --red: #a8523f;
      --shadow: 0 8px 28px rgba(49, 64, 48, .055);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "Segoe UI", Arial, sans-serif;
    }
    .masthead {
      background: rgba(255, 254, 250, .94);
      border-bottom: 1px solid var(--line);
    }
    .masthead-inner, main, .footer {
      width: min(1180px, calc(100% - 44px));
      margin: 0 auto;
    }
    .masthead-inner {
      min-height: 68px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .identity { display: flex; align-items: center; gap: 12px; }
    .mark {
      width: 37px; height: 37px; border-radius: 50%;
      display: grid; place-items: center;
      color: var(--forest); background: var(--sage);
      font-family: Georgia, serif; font-size: 22px;
    }
    .identity-name { font: 600 15px Georgia, "Times New Roman", serif; letter-spacing: .01em; }
    .docs-link { color: var(--forest); text-decoration: none; font-size: 13px; }
    .docs-link:hover { text-decoration: underline; }
    main { padding: 36px 0 56px; }
    .intro {
      display: grid; grid-template-columns: 1.35fr .65fr; gap: 28px;
      align-items: center; padding: 28px 32px;
      background: #e9eee5; border: 1px solid #dce4d8; border-radius: 17px;
    }
    h1 { margin: 0; font-size: clamp(26px, 3vw, 32px); font-weight: 600; letter-spacing: 0; }
    h2 { font-family: Georgia, "Times New Roman", serif; font-weight: 600; }
    .intro-copy { max-width: 670px; margin: 12px 0 0; color: #59685d; line-height: 1.65; font-size: 15px; }
    .source-note {
      border-left: 2px solid var(--ochre); padding: 5px 0 5px 15px;
      color: #637067; font-size: 13px; line-height: 1.65;
    }
    .source-note strong { display: block; color: var(--ink); font-size: 12px; margin-bottom: 3px; }
    .workflow {
      margin: 21px 0 13px; display: flex; align-items: center; gap: 9px;
      overflow-x: auto; padding-bottom: 3px;
    }
    .step {
      flex: 1 0 128px; min-height: 58px; padding: 10px 12px;
      background: var(--card); border: 1px solid var(--line); border-radius: 10px;
    }
    .step-top { color: var(--forest); font-size: 10px; font-weight: 800; letter-spacing: .08em; }
    .step-name { margin-top: 5px; font-size: 12px; color: #526057; font-weight: 600; }
    .step-arrow { color: #b2b8ae; flex: 0 0 auto; }
    .toolbar {
      display: flex; align-items: center; justify-content: space-between; gap: 18px;
      padding: 15px 2px 17px;
    }
    .status-wrap { min-height: 24px; display: flex; align-items: center; gap: 9px; }
    .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #9da69e; }
    #status { color: var(--muted); font-size: 13px; }
    #status.success { color: var(--forest); }
    #status.error { color: var(--red); }
    #runButton, .download {
      border: 0; border-radius: 9px; font: inherit; font-size: 13px;
      font-weight: 700; text-decoration: none; cursor: pointer;
    }
    #runButton {
      padding: 12px 17px; color: #fff; background: var(--forest);
      box-shadow: 0 4px 10px rgba(54, 92, 73, .15);
    }
    #runButton:hover { background: var(--forest-dark); }
    #runButton:disabled { opacity: .7; cursor: progress; }
    .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 13px; margin-bottom: 15px; }
    .metric {
      padding: 15px 18px; border: 1px solid var(--line); border-radius: 12px;
      background: var(--card);
    }
    .metric-label { color: var(--muted); font-size: 10px; letter-spacing: .08em; text-transform: uppercase; }
    .metric-value { margin-top: 6px; font: 600 19px Georgia, "Times New Roman", serif; }
    .content { display: grid; grid-template-columns: 1.12fr .88fr; gap: 15px; align-items: start; }
    .panel {
      background: var(--card); border: 1px solid var(--line);
      border-radius: 13px; overflow: hidden; box-shadow: var(--shadow);
    }
    .panel-head {
      min-height: 66px; padding: 14px 17px; display: flex;
      align-items: center; justify-content: space-between; gap: 12px;
      border-bottom: 1px solid var(--line);
    }
    h2 { margin: 0; font-size: 18px; }
    .panel-subtitle { margin-top: 4px; color: var(--muted); font-size: 12px; }
    .download { display: inline-block; padding: 9px 11px; color: var(--forest); background: var(--sage); }
    .download.disabled { color: #98a097; background: #f0f0eb; cursor: default; pointer-events: none; }
    .table-scroll { max-height: 480px; overflow: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 12px; }
    th, td { padding: 11px 12px; border-bottom: 1px solid #eeeee7; text-align: left; white-space: nowrap; }
    th { position: sticky; top: 0; z-index: 1; background: #f7f7f1; color: #6e796f; font-size: 10px; letter-spacing: .07em; text-transform: uppercase; }
    tbody tr:hover { background: #fafaf5; }
    tbody tr:last-child td { border-bottom: 0; }
    .empty { padding: 27px 14px; text-align: center; color: #8a948b; line-height: 1.6; }
    .chart-wrap { padding: 15px; }
    .chart-wrap img { display: block; width: 100%; height: auto; border-radius: 7px; }
    .chart-empty {
      min-height: 250px; padding: 22px; display: grid; place-items: center;
      text-align: center; color: #879188; background: #f6f6f0; border-radius: 8px;
      font: 14px/1.6 Georgia, "Times New Roman", serif;
    }
    .footer { padding: 17px 0 0; color: #899188; font-size: 11px; }
    @media (max-width: 820px) {
      .intro { grid-template-columns: 1fr; gap: 18px; }
      .content { grid-template-columns: 1fr; }
    }
    @media (max-width: 560px) {
      .masthead-inner, main, .footer { width: min(100% - 28px, 1180px); }
      main { padding-top: 20px; }
      .intro { padding: 22px 19px; }
      .toolbar { align-items: flex-start; flex-direction: column; }
      .metrics { grid-template-columns: 1fr; gap: 8px; }
      .metric { padding: 12px 15px; }
      .metric-value { font-size: 16px; }
    }
  </style>
</head>
<body>
  <header class="masthead">
    <div class="masthead-inner">
      <div class="identity"><span class="mark">✳</span><span class="identity-name">A small country data study</span></div>
      <a class="docs-link" href="/docs" target="_blank">API reference ↗</a>
    </div>
  </header>
  <main>
    <section class="intro">
      <div>
        <h1>Country Data Dashboard</h1>
        <p class="intro-copy">A simple look at the first 20 country records from the project source. Run the workflow to collect the data, save it to the database, and prepare the table, CSV, and population-to-area chart.</p>
      </div>
      <div class="source-note"><strong>Data source</strong>Simple Countries · scrapethissite.com<br>Fields: country, capital, population, area</div>
    </section>
    <section class="workflow" aria-label="Project workflow">
      <div class="step"><div class="step-top">01 · READY</div><div class="step-name">Virtual environment</div></div>
      <span class="step-arrow">›</span>
      <div class="step"><div class="step-top">02</div><div class="step-name">Collect records</div></div>
      <span class="step-arrow">›</span>
      <div class="step"><div class="step-top">03</div><div class="step-name">Save in SQLite</div></div>
      <span class="step-arrow">›</span>
      <div class="step"><div class="step-top">04</div><div class="step-name">Read through API</div></div>
      <span class="step-arrow">›</span>
      <div class="step"><div class="step-top">05–06</div><div class="step-name">CSV and chart</div></div>
    </section>
    <section class="toolbar">
      <div class="status-wrap"><span class="status-dot" id="statusDot"></span><span id="status" role="status">Ready when you are. Run the workflow to refresh the country data.</span></div>
      <button id="runButton" onclick="runPipeline()">Run the workflow</button>
    </section>
    <section class="metrics">
      <div class="metric"><div class="metric-label">Records in database</div><div class="metric-value" id="countryCount">—</div></div>
      <div class="metric"><div class="metric-label">Database file</div><div class="metric-value">countries.db</div></div>
      <div class="metric"><div class="metric-label">Project outputs</div><div class="metric-value">CSV · Scatter plot</div></div>
    </section>
    <section class="content">
      <article class="panel">
        <div class="panel-head">
          <div><h2>Country records</h2><div class="panel-subtitle">Population and area are shown as numeric values</div></div>
          <a class="download disabled" id="downloadLink" href="#" aria-disabled="true">Download CSV</a>
        </div>
        <div class="table-scroll">
          <table>
            <thead><tr><th>Country</th><th>Capital</th><th>Population</th><th>Area (sq. km)</th></tr></thead>
            <tbody id="countryRows"><tr><td class="empty" colspan="4">Country records will appear here after the first run.</td></tr></tbody>
          </table>
        </div>
      </article>
      <article class="panel">
        <div class="panel-head"><div><h2>Population and area</h2><div class="panel-subtitle">Each point represents one country</div></div></div>
        <div class="chart-wrap" id="chartWrap"><div class="chart-empty">The scatter plot will appear here<br>after the workflow completes.</div></div>
      </article>
    </section>
    <div class="footer">Country data capstone · local dashboard</div>
  </main>
  <script>
    const statusBox = document.getElementById("status");
    const statusDot = document.getElementById("statusDot");
    const runButton = document.getElementById("runButton");

    function setStatus(message, kind) {
      statusBox.textContent = message;
      statusBox.className = kind || "";
      statusDot.style.background = kind === "success" ? "#477a5e" :
                                  kind === "error" ? "#a8523f" : "#c48645";
    }

    function showCountries(countries) {
      const rows = document.getElementById("countryRows");
      rows.replaceChildren();
      for (const country of countries) {
        const row = document.createElement("tr");
        const values = [country.country_name, country.capital,
                        Number(country.population).toLocaleString("en-IN"),
                        Number(country.area).toLocaleString("en-IN", { maximumFractionDigits: 2 })];
        for (const value of values) {
          const cell = document.createElement("td");
          cell.textContent = value;
          row.appendChild(cell);
        }
        rows.appendChild(row);
      }
      document.getElementById("countryCount").textContent = countries.length;
    }

    async function showExistingData() {
      try {
        const [countriesResponse, outputsResponse] = await Promise.all([
          fetch("/countries"), fetch("/dashboard-outputs")
        ]);
        if (countriesResponse.ok) {
          const countries = await countriesResponse.json();
          if (countries.length) showCountries(countries);
        }
        if (outputsResponse.ok) {
          const outputs = await outputsResponse.json();
          if (outputs.csv_ready) enableDownload();
          if (outputs.plot_ready) showPlot();
        }
      } catch (_) {
        // The workflow button remains available if saved data cannot be loaded.
      }
    }

    function enableDownload() {
      const link = document.getElementById("downloadLink");
      link.href = "/dashboard-download-csv";
      link.classList.remove("disabled");
      link.removeAttribute("aria-disabled");
      link.setAttribute("download", "exported_countries.csv");
    }

    function showPlot() {
      document.getElementById("chartWrap").innerHTML =
        '<img alt="Scatter plot comparing country population and area" src="/dashboard-chart?v=' + Date.now() + '">';
    }

    async function runPipeline() {
      runButton.disabled = true;
      runButton.textContent = "Working…";
      setStatus("Collecting the country records and preparing the files…", "");
      try {
        const response = await fetch("/dashboard-run", { method: "POST" });
        const result = await response.json();
        if (!response.ok) throw new Error(result.detail || "The workflow could not finish.");
        showCountries(result.countries);
        enableDownload();
        showPlot();
        setStatus("Finished. " + result.count + " records are ready in the table, CSV, and chart.", "success");
      } catch (error) {
        setStatus("The workflow stopped: " + error.message, "error");
      } finally {
        runButton.disabled = false;
        runButton.textContent = "Run the workflow";
      }
    }

    showExistingData();
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def country_dashboard():
    return HTML_PAGE


@app.get("/dashboard-outputs")
def dashboard_outputs():
    return {"csv_ready": CSV_FILE.exists(), "plot_ready": PLOT_FILE.exists()}


@app.get("/dashboard-download-csv")
def dashboard_download_csv():
    if not CSV_FILE.exists():
        raise HTTPException(status_code=404, detail="Run the workflow before downloading the CSV")
    return FileResponse(CSV_FILE, filename="exported_countries.csv", media_type="text/csv")


@app.get("/dashboard-chart")
def dashboard_chart():
    if not PLOT_FILE.exists():
        raise HTTPException(status_code=404, detail="Run the workflow before viewing the chart")
    return FileResponse(PLOT_FILE, media_type="image/png")


@app.post("/dashboard-run")
def dashboard_run():
    try:
        # This calls the separate scraper and database modules.
        load_scraped_countries(country_database)

        # This calls the separate client, which fetches GET /countries and writes the CSV.
        export_countries()

        # This calls the separate visualization module, which reads the CSV and saves the chart.
        create_scatter_plot()

        countries = country_database.get_all_countries()
        return {"count": len(countries), "countries": countries}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


def open_dashboard():
    time.sleep(1.5)
    webbrowser.open_new_tab("http://127.0.0.1:8000/")


if __name__ == "__main__":
    threading.Thread(target=open_dashboard, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
