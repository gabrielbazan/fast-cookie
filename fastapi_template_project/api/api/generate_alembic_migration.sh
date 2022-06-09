

MESSAGE=${1}
CONTAINER_NAME=fastapi_template_project-api-1


docker exec ${CONTAINER_NAME} alembic revision --autogenerate -m "${MESSAGE}"
