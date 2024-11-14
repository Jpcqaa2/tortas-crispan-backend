#!/usr/bin/env bash

# Exit on error
set -o errexit

# Build
./build_production.sh

if [ $? -eq 0 ]; then
    # run server
    python -m gunicorn tortas-crispan-backend.asgi:application -k uvicorn.workers.UvicornWorker
else
    echo "The script ./build_production finished with error. The backend will not run."
fi