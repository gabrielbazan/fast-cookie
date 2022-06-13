

VIRTUALENV_PATH="venv"

PROJECT_PACKAGE_NAME="{{ cookiecutter.project_package_name }}"
API_SERVICE_NAME="api"
REQUIREMENTS_FILE_NAME="requirements.frozen"
REQUIREMENTS_FILE_PATH="${PROJECT_PACKAGE_NAME}/${API_SERVICE_NAME}/${API_SERVICE_NAME}/${REQUIREMENTS_FILE_NAME}"


venv:
	echo "Creating virtualenv..."
	python3 -m venv "${VIRTUALENV_PATH}"

	echo "Installing requirements..."
	${VIRTUALENV_PATH}/bin/pip install -r "${REQUIREMENTS_FILE_PATH}"

	echo "Done!"


install_development_dependencies:
	echo "Installing development dependencies..."
	sudo apt install python3.10-venv
	echo "Done!"
