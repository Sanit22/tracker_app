#!/bin/bash
echo "Activating local development environment..."
export ENV="development"
source tracku-env/bin/activate
echo "Runnning the application..."
python3 main.py

