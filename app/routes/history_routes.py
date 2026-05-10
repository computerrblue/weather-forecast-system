from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.file_service import FileService


router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

history_service = FileService("data/history.json")


@router.get("/history")
def history_page(request: Request):

    history = history_service.load_json()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "history": history
        }
    )