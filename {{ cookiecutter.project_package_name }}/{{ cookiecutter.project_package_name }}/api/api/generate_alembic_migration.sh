

PROJECT_NAME="{{ cookiecutter.project_package_name }}"
API_SERVICE_NAME="api"
CONTAINER_NAME="${PROJECT_NAME}-${API_SERVICE_NAME}-1"

MESSAGE="${1}"


docker exec "${CONTAINER_NAME}" alembic revision --autogenerate -m "${MESSAGE}"
