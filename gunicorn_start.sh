#!/bin/bash

gunicorn learn.wsgi:application --workers=2 --bind 0.0.0.0:$PORT

