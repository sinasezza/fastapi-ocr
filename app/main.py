import pathlib
from typing import Annotated

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import config
from .config import templates

BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI()


setting_deps = Annotated[config.Settings, Depends(config.get_settings)]


@app.get("/", response_class=HTMLResponse)
def home_view(request: Request, settings: setting_deps):
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/")
def home_detail_view():
    return {"message": "Welcome to the FastAPI application! POST"}
