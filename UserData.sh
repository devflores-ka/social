# !/bin/bash
set -e

# Repositorio publico de GitHub
GIT_REPO_URL="https://github.com/devflores-ka/social"

# Nombre del directorio de la aplicacion
PROJECT_MAIN_DIR_NAME="social"

# Clonar repositorio
git clone "$GIT_REPO_URL" "/home/ubuntu/$PROJECT_MAIN_DIR_NAME"

# Cambiar de directorio
cd "/home/ubuntu/$PROJECT_MAIN_DIR_NAME"

# Dar permiso a los archivos .sh
chmod +x scripts/*.sh

# Instalar dependencias
./scripts/instance_os_dependencies.sh
./scripts/python_dependencies.sh
./scripts/gunicorn.sh
./scripts/nginx.sh
./scripts/after_install.sh
./scripts/start_app.sh