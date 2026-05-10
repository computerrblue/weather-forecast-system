from fastapi import APIRouter,Request,Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form
from app.services import file_service
from app.services.weather_service import WeatherService
from app.services.file_service import FileService
from dotenv import load_dotenv
import os
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

load_dotenv()
api_key = os.getenv("API_KEY")
weather_service = WeatherService(api_key=api_key)
history_service = FileService("data/history.json")




@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.post("/weather")
def get_weather(request: Request, city: str = Form(...)):

    weather = weather_service.get_current_weather(city=city)
    weather["searched_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    history_service.append_history(weather)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "weather": weather
        }
    )


