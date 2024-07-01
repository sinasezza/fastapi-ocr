import pathlib

import pytesseract
from PIL import Image

BASE_DIR = pathlib.Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "test_images"
img_path = IMG_DIR / "img2.png"


img = Image.open(img_path)

preds = pytesseract.image_to_string(img)

predictions = [x for x in preds.split("\n")]


print(predictions)
