import shutil
import time

import pytest
from fastapi import Request, Response, status
from fastapi.testclient import TestClient
from PIL import Image, ImageChops

from ..config import BASE_DIR, UPLOAD_DIR, get_settings
from ..main import app

client = TestClient(app)


def test_get_home():
    response: Response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["Content-Type"]


valid_image_extensions = ("jpg", "jpeg", "png", "gif")


def images_are_equal(img1, img2, tolerance=10):
    diff = ImageChops.difference(img1, img2)
    diff_data = diff.getdata()
    for pixel in diff_data:
        if any(channel > tolerance for channel in pixel):
            return False
    return True


def test_img_echo():
    img_saved_path = BASE_DIR / "test_images"
    for path in img_saved_path.glob("*"):
        if path.suffix[1:].lower() not in valid_image_extensions:
            continue  # Skip non-image files

        with open(path, "rb") as file:
            response = client.post(
                "/img-echo/",
                files={"file": (path.name, file, f"image/{path.suffix[1:].lower()}")},
            )

        if response.status_code == status.HTTP_200_OK:
            # Save the received image temporarily
            received_image_path = BASE_DIR / "temp" / path.name
            received_image_path.parent.mkdir(exist_ok=True)
            with open(received_image_path, "wb") as out_file:
                out_file.write(response.content)

            # Compare the images
            with Image.open(path) as original_img, Image.open(
                received_image_path
            ) as received_img:
                original_img = original_img.convert("RGB")
                received_img = received_img.convert("RGB")
                assert images_are_equal(
                    original_img, received_img
                ), f"Image mismatch for file: {path}"

        else:
            pytest.fail(
                f"Failed to upload file {path}, status code: {response.status_code}"
            )

    time.sleep(3)
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)


@pytest.mark.xfail(reason="no Authentication Mechanism")
def test_prediction_view_without_auth_token_should_fail():
    img_saved_path = BASE_DIR / "test_images"

    # Ensure the image directory exists
    assert img_saved_path.exists(), "Image directory does not exist"

    for path in img_saved_path.glob("*"):
        if path.suffix[1:].lower() not in valid_image_extensions:
            continue  # Skip non-image files

        with open(path, "rb") as file:
            response = client.post(
                "/",
                files={"file": (path.name, file, f"image/{path.suffix[1:].lower()}")},
            )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Authentication" in response.json()["detail"]


def test_prediction_view():
    img_saved_path = BASE_DIR / "test_images"

    settings = get_settings()

    # Ensure the image directory exists
    assert img_saved_path.exists(), "Image directory does not exist"

    for path in img_saved_path.glob("*"):
        if path.suffix[1:].lower() not in valid_image_extensions:
            continue  # Skip non-image files

        with open(path, "rb") as file:
            response = client.post(
                "/",
                files={"file": (path.name, file, f"image/{path.suffix[1:].lower()}")},
                headers={"Authorization": f"Bearer {settings.app_auth_token}"},
            )

        if response.status_code == status.HTTP_200_OK:
            response_data = response.json()
            assert (
                "text" in response_data
            ), f"Response data missing 'text' key for file: {path}"
            assert isinstance(
                response_data["text"], list
            ), f"Response 'text' is not a list for file: {path}"
        else:
            pytest.fail(
                f"Failed to upload file {path}, status code: {response.status_code}"
            )
