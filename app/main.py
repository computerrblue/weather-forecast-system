from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import weather_routes
from app.routes import history_routes


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


app.include_router(weather_routes.router)

app.include_router(history_routes.router)