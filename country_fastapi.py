"""Expose country database operations through FastAPI endpoints."""

import sqlite3

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from database_handling import CountryDatabaseManager


class CountryCreate(BaseModel):
    country_name: str
    capital: str
    population: int
    area: float


class CountryUpdate(BaseModel):
    capital: str
    population: int
    area: float


app = FastAPI()
country_database = CountryDatabaseManager()


@app.get("/countries")
def get_all_countries():
    return country_database.get_all_countries()


@app.get("/countries/{country_name}")
def get_country(country_name: str):
    country = country_database.get_country_by_name(country_name)
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@app.post("/countries", status_code=status.HTTP_201_CREATED)
def create_country(country: CountryCreate):
    try:
        country_database.create_country(country.model_dump())
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Country already exists")
    return {"message": "Country created successfully"}


@app.put("/countries/{country_name}")
def update_country(country_name: str, country: CountryUpdate):
    updated = country_database.update_country(country_name, country.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Country not found")
    return country_database.get_country_by_name(country_name)


@app.delete("/countries/{country_name}")
def delete_country(country_name: str):
    deleted = country_database.delete_country(country_name)
    if not deleted:
        raise HTTPException(status_code=404, detail="Country not found")
    return {"message": "Country deleted successfully"}
