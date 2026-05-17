from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os

from requests import api
from app.services.weather_service import WeatherService


router = APIRouter()
load_dotenv()
api_key = os.getenv("API_KEY")
templates = Jinja2Templates(directory="app/templates")

weather_service = WeatherService(api_key=api_key)

@router.get("/forecast/{city}")
def forecast_page(request: Request, city: str):

    if "user" not in request.session:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    forecasts = weather_service.get_forecast(city)

    return templates.TemplateResponse(
        request=request,
        name="forecast.html",
        context={
            "username": request.session["user"],
            "city": city,
            "forecasts": forecasts
        }
    )