# To run the file 'uvicorn main:app --reload'

from fastapi import FastAPI
from databases import Database
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String
from fastapi.middleware.cors import CORSMiddleware


class Item(BaseModel):
    porcentaje_contenedor: Optional[str]
    fecha: Optional[str]
    morning: Optional[str]
    morning_porcion: Optional[str]
    lunch: Optional[str]
    lunch_porcion: Optional[str]
    dinner: Optional[str]
    dinner_porcion: Optional[str]
    porcion: Optional[str]
    ultima_comida: Optional[str]

DATABASE_URL = "mysql://root:password@localhost:3306/alimentador"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Retrieves all data form the database
@app.get("/datos/")
async def read_items():
    query = "SELECT * FROM datos;"
    results = await database.fetch_all(query)
    return results

# 
@app.get("/contenedor/")
async def read_latest_porcentaje_contenedor():
    query = "SELECT porcentaje_contenedor FROM datos ORDER BY fecha DESC LIMIT 1;"
    results = await database.fetch_all(query)
    return results

@app.get("/porcion/")
async def read_latest_porcion():
    query = "SELECT porcion FROM datos ORDER BY fecha DESC LIMIT 1;"
    results = await database.fetch_all(query)
    return results


@app.get("/schedule/")
async def read_latest_schedule():
    query = "SELECT morning, lunch, dinner FROM datos ORDER BY fecha DESC LIMIT 1;"
    results = await database.fetch_all(query)
    return results

@app.get("/latest/")
async def read_latest_entry():
    query = "SELECT * FROM datos ORDER BY fecha DESC LIMIT 1;"
    results = await database.fetch_all(query)
    return results

@app.put("/updateItem/")
async def update_item(item: Item):
    data = await read_latest_entry()
    fecha = data[0]['fecha']
    query = """
    UPDATE datos 
    SET 
        porcentaje_contenedor = :porcentaje_contenedor,
        fecha = :fecha,
        morning = :morning,
        morning_porcion = :morning_porcion,
        lunch = :lunch,
        lunch_porcion = :lunch_porcion,
        dinner = :dinner,
        dinner_porcion = :dinner_porcion,
        porcion = :porcion,
        ultima_comida = :ultima_comida
    WHERE fecha = :fecha
    """
    values = item.dict()
    values.update({"fecha": fecha})
    if await database.execute(query, values):
        return {"message": "Item has been updated successfully"}
    else:
        print('** Something happened, couldnt update item! **')


@app.put("/updatePropertyItem/")
async def update_property_item(item: Item):
    # Retrieve the latest data
    data = await read_latest_entry()
    fecha = data[0]['fecha']

    query = """
    UPDATE datos 
    SET 
        porcentaje_contenedor = :porcentaje_contenedor,
        fecha = :fecha,
        morning = :morning,
        morning_porcion = :morning_porcion,
        lunch = :lunch,
        lunch_porcion = :lunch_porcion,
        dinner = :dinner,
        dinner_porcion = :dinner_porcion,
        porcion = :porcion,
        ultima_comida = :ultima_comida
    WHERE fecha = :fecha
    """
    values = {
        "porcentaje_contenedor": item.porcentaje_contenedor if item.porcentaje_contenedor is not None else data[0]['porcentaje_contenedor'],
        "fecha": fecha,
        "morning": item.morning if item.morning != "" else data[0]['morning'],
        "morning_porcion": item.morning_porcion if item.morning_porcion != "" else data[0]['morning_porcion'],
        "lunch": item.lunch if item.lunch != "" else data[0]['lunch'],
        "lunch_porcion": item.lunch_porcion if item.lunch_porcion != "" else data[0]['lunch_porcion'],
        "dinner": item.dinner if item.dinner != "" else data[0]['dinner'],
        "dinner_porcion": item.dinner_porcion if item.dinner_porcion != "" else data[0]['dinner_porcion'],
        "porcion": item.porcion if item.porcion != "" else data[0]['porcion'],
        "ultima_comida": item.ultima_comida if item.ultima_comida != "" else data[0]['ultima_comida'], 
    }

    if await database.execute(query, values):
        return {"message": "Item has been updated successfully"}
    else:
        print("** Something happened, couldn't update item! **")
