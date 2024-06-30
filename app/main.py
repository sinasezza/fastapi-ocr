import pathlib
from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


BASE_DIR = pathlib.Path(__file__).parent

app = FastAPI()


templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

@app.get("/", response_class=HTMLResponse)
def home_view(request: Request):
    # return {"message": "Welcome to the FastAPI application!"}
    return templates.TemplateResponse("home.html", context={"request": request})


@app.post("/")
def home_detail_view():
    return {"message": "Welcome to the FastAPI application! POST"}