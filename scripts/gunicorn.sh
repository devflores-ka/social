#!/usr/bin/bash

# Nombre del directorio de la aplicacion
PROJECT_MAIN_DIR_NAME="social"

# Copia los archivos socket y service de gunicorn  
sudo cp "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/gunicorn/gunicorn.socket" "/etc/systemd/system/gunicorn.socket"
sudo cp "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/gunicorn/gunicorn.service" "/etc/systemd/system/gunicorn.service"

# Inicia y habilita Gunicorn service
sudo systemctl start gunicorn.service
sudo systemctl enable gunicorn.service