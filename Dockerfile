FROM python:3.12-slim-bullseye

WORKDIR /home

# Copy requirements first for better caching
COPY ./requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    python3-setuptools \
    tesseract-ocr \
    make \
    gcc && \
    python3 -m pip install -r requirements.txt && \
    apt-get remove -y --purge make gcc build-essential && \
    apt-get clean && \
    apt-get autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000


COPY ./entrypoint.sh .
COPY ./app ./app

# Set permissions for entrypoint
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
