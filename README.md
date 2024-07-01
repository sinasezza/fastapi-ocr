# fastapi-ocr

fastapi microservice app for text extraction from images

## overview

this is a simple implementation of the fastapi micro service that provides text extraction from images using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
Tesseract is an optical character recognition engine for various operating systems.

## Get Started

first, Let's Get The Application's Repository

```bash
git clone https://github.com/sinasezza/fastapi-ocr.git
cd fastapi-ocr
```

## How to use

to run the fastapi microservice app there is two ways:

- run on os
- run on docker engine

## first of all you mush have a .env file in your app directory

dotenv files is a list of environment variables that are sensitive to store in code.

you can rename the .env.sample file in app directory and configure it as you wish and use it.

## Run On OS

### first install Tesseract App/Package

for example if you want to install it on linux based systems like debian/ubuntu you can install using the following command:

```bash
sudo apt-get install tesseract-ocr
```

### second install fastapi requirements

make sure you have installed python (at least version 3.9)

#### create and use a virtualenv (optional)

##### MacOs/Linux Users

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install uv
uv pip install -r requirements.txt --upgrade
```

##### Windows Users

```bash
python -m venv venv
venv\Scripts\activate
pip install uv
uv pip install -r requirements.txt --upgrade
```

#### Run The project

```bash
uvicorn app.main:app --reload
```

#### for test the project

```bash
pytest .
```

## Run On Docker Engine

first make sure you have installed docker-engine and docker-ce

### run the docker compose

```bash
docker compose up -d --build
```

## check the endpoints

check and test endpoints in the address:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
