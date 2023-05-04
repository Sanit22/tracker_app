#!/bin/bash
echo "Activating local development environment..."
source tracku-env/bin/activate
echo "Runnning the application..."
python3 -m celery -A main.celery worker --loglevel=info
