#!/bin/bash
echo "Activating staging environment..."
source tracku-env/bin/activate
export ENV="stage"
echo "Runnning the application..."
python3 -m gunicorn main:app --worker-class gevent --bind 127.0.0.1:8000


