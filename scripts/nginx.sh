#!/usr/bin/bash

# Nombre del directorio de la aplicacion
PROJECT_MAIN_DIR_NAME="social"

# Replace {FOLDER_NAME_WHERE_SETTINGS_FILE_EXISTS} with the folder name where your nginx configuration file exists
FOLDER_NAME_WHERE_SETTINGS_FILE_EXISTS="core"

# Recarga systemd daemon
sudo systemctl daemon-reload

# Elimina el archivo default Nginx site si existe
sudo rm -f /etc/nginx/sites-enabled/default

# Copia el archivo de configuration para Nginx 
sudo cp "/home/ubuntu/$PROJECT_MAIN_DIR_NAME/nginx/nginx.conf" "/etc/nginx/sites-available/$FOLDER_NAME_WHERE_SETTINGS_FILE_EXISTS"

# Crea el vinculo simbolico para habilitar Nginx site
sudo ln -s "/etc/nginx/sites-available/$FOLDER_NAME_WHERE_SETTINGS_FILE_EXISTS" "/etc/nginx/sites-enabled/"

# Añade el usuario www-data al gropo ubuntu
sudo gpasswd -a www-data ubuntu

# Reinicia el Nginx service
sudo systemctl restart nginx