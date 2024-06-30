#!/bin/bash
set -e

RUN_PORT=${RUN_PORT:-8000}
exec gunicorn --worker-tmp-dir /dev/shm \
              --bind 0.0.0.0:$RUN_PORT \
              --workers 2 \
              --worker-class uvicorn.workers.UvicornWorker \
              app.main:app
