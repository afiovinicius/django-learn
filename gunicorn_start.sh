#!/bin/bash

# Certifique-se de ajustar os caminhos conforme necessário
PROJECT_DIR="django-learn"
APP_DIR="learn"
GUNICORN_CONFIG="gunicorn_config.py"

# Inicie o Gunicorn apontando para o arquivo wsgi.py
gunicorn ${APP_DIR}.wsgi:application -c ${PROJECT_DIR}/${GUNICORN_CONFIG}
