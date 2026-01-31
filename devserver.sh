#!/bin/sh
source .venv/bin/activate
python -u -m flask --app run --debug run -p $PORT
