

API_SERVICE_NAME="api"


MESSAGE="${1}"


is_container_running=true

if [ -z `docker compose ps -q ${API_SERVICE_NAME} 2>/dev/null` ] || [ -z `docker ps -q --no-trunc | grep $(docker compose ps -q ${API_SERVICE_NAME})` ]; then
  is_container_running=false
fi


if [ ${is_container_running} = false ]; then
  echo "Containers are not running. Running them..."
  docker compose up -d
fi


echo "Generating migrations..."
docker compose exec ${API_SERVICE_NAME} bash -c "./wait-service.sh \${DATABASE_HOST} \${DATABASE_PORT} && alembic revision --autogenerate -m '${MESSAGE}'"


if [ ${is_container_running} = false ]; then
  echo "Containers were not running before generating the migrations. Stopping them..."
	docker compose stop
fi
