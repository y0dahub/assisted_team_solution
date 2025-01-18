from fastapi import FastAPI

from data.data import parse_stats, parse_flights, compare_xml_files

app = FastAPI()

@app.get("/")
async def get_root():
    return {"Hello": "World"}


@app.post("/flights")
async def get_flights():
    flights = parse_flights()

    return flights

@app.post("/stats")
async def get_stats():
    stats = parse_stats()

    return stats

@app.post("/flights/difference")
async def get_difference():
    xml = compare_xml_files()
    diffs = []

    for tag, value1, value2 in xml:
        diffs.append({"Element": tag, "File 1": value1, "File 2": value2})

    return diffs