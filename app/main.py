from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.routes import weather_routes
from app.routes import history_routes
from app.routes import forecast_routes
from app.routes import auth_routes
app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


app.include_router(weather_routes.router)
app.include_router(auth_routes.router)
app.include_router(forecast_routes.router)
app.include_router(history_routes.router)
