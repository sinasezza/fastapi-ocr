import io
import pathlib
import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse, HTMLResponse
from PIL import Image

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



@app.post("/img-echo/", response_class=FileResponse)
async def image_echo_view(
    file: Annotated[UploadFile, File(...)],
    settings: Annotated[config.Settings, Depends(config.get_settings)],
):
    if not settings.echo_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Echo feature is not active"
        )

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded"
        )

    try:
        file_content = await file.read()
        if not file_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty"
            )

        if len(file_content) > config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds the limit of {config.MAX_FILE_SIZE // (1024 * 1024)} MB",
            )

        bytes_str = io.BytesIO(file_content)

        try:
            img = Image.open(bytes_str)
            img.verify()
            bytes_str.seek(0)
            img = Image.open(bytes_str)
        except (IOError, SyntaxError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid image file: {str(e)}",
            )

        filename = pathlib.Path(file.filename)
        suffix = filename.suffix.lower()
        if suffix not in [".jpg", ".jpeg", ".png", ".gif"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type. Only JPG, PNG, and GIF are allowed.",
            )

        config.UPLOAD_DIR.mkdir(exist_ok=True)
        dest = config.UPLOAD_DIR / f"{uuid.uuid1()}{suffix}"
        img.save(dest, format=img.format, quality=95)

        return FileResponse(dest, filename=file.filename, media_type=file.content_type)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the file: {str(e)}",
        )
