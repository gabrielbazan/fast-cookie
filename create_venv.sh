

VIRTUALENV_PATH="venv"
REQUIREMENTS_FILE_PATH=fastapi_template_project/api/api/requirements.frozen


echo "Creating virtualenv..."
python3 -m venv ${VIRTUALENV_PATH}

echo "Installing requirements..."
${VIRTUALENV_PATH}/bin/pip install -r ${REQUIREMENTS_FILE_PATH}


echo "Done!"
