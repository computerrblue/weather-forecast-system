from fastapi import (
    APIRouter,
    Request,
    Form
)

from fastapi.templating import (
    Jinja2Templates
)

from fastapi.responses import RedirectResponse

from app.services.auth_service import AuthService


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)

auth_service = AuthService()


@router.get("/register")
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )

@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    result = auth_service.register_user(username, password)

    if "success" in result:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"result": result}
    )



@router.get("/login")
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    result = auth_service.login_user(username, password)

    if "success" in result:

        request.session["user"] = username

        return RedirectResponse(
            url="/",
            status_code=302
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"result": result}
    )




@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=302
    )