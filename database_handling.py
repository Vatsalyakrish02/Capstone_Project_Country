"""Store scraped country records in SQLite using a database manager class."""

import sqlite3
from pathlib import Path

from web_scraping import scrape_countries


class CountryDatabaseManager:
    def __init__(self, db_name=None):
        if db_name is None:
            db_name = Path(__file__).with_name("countries.db")
        self.db_name = str(db_name)
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS countries (
                    country_name TEXT PRIMARY KEY,
                    capital TEXT NOT NULL,
                    population INTEGER NOT NULL,
                    area REAL NOT NULL
                )
                """
            )

    def create_country(self, country):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO countries (country_name, capital, population, area)
                VALUES (?, ?, ?, ?)
                """,
                (
                    country["country_name"],
                    country["capital"],
                    country["population"],
                    country["area"],
                ),
            )

    def get_all_countries(self):
        with sqlite3.connect(self.db_name) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT country_name, capital, population, area FROM countries")
            return [dict(row) for row in cursor.fetchall()]

    def get_country_by_name(self, country_name):
        with sqlite3.connect(self.db_name) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                "SELECT country_name, capital, population, area FROM countries WHERE country_name = ?",
                (country_name,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_country(self, country_name, country):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE countries
                SET capital = ?, population = ?, area = ?
                WHERE country_name = ?
                """,
                (
                    country["capital"],
                    country["population"],
                    country["area"],
                    country_name,
                ),
            )
            return cursor.rowcount > 0

    def delete_country(self, country_name):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM countries WHERE country_name = ?",
                (country_name,),
            )
            return cursor.rowcount > 0


def load_scraped_countries(database):
    countries = scrape_countries()

    for country in countries:
        old_country = database.get_country_by_name(country["country_name"])
        if old_country:
            database.update_country(country["country_name"], country)
        else:
            database.create_country(country)

    print(f"Stored {len(countries)} country records in countries.db")


if __name__ == "__main__":
    country_database = CountryDatabaseManager()
    load_scraped_countries(country_database)

    for country in country_database.get_all_countries():
        print(country)
