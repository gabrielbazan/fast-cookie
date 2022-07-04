import re
from os import remove
from os.path import join
from shutil import rmtree


class BooleanOptions:
    YES = "Yes"
    NO = "No"


PROJECT_PACKAGE_NAME = "{{ cookiecutter.project_package_name }}"


ADD_DATABASE_ANSWER = "{{ cookiecutter.add_database }}"
ADD_DATABASE = ADD_DATABASE_ANSWER == BooleanOptions.YES


API_SERVICE_NAME = "api"

DATABASE_ENV_FILENAME = "database.env"
ALEMBIC_FOLDER_NAME = "alembic"
ALEMBIC_INI_FILENAME = "alembic.ini"
DATABASE_PACKAGE_NAME = "database"
SERIALIZATION_PACKAGE_NAME = "serialization"
MODEL_SERIALIZATION_MODULE_NAME = "model_serialization.py"
SCRIPTS_FOLDER_NAME = "scripts"
GENERATE_DATABASE_MIGRATION_SCRIPT_FILENAME = "generate_database_migration.sh"
MIGRATE_DATABASE_SCRIPT_FILENAME = "migrate_database.sh"
SETTINGS_PY_FILENAME = "settings.py"


DATABASE_FILES = (
    join(
        PROJECT_PACKAGE_NAME,
        DATABASE_ENV_FILENAME,
    ),
    join(
        PROJECT_PACKAGE_NAME,
        API_SERVICE_NAME,
        API_SERVICE_NAME,
        ALEMBIC_INI_FILENAME,
    ),
    join(
        PROJECT_PACKAGE_NAME,
        API_SERVICE_NAME,
        API_SERVICE_NAME,
        SERIALIZATION_PACKAGE_NAME,
        MODEL_SERIALIZATION_MODULE_NAME,
    ),
    join(
        PROJECT_PACKAGE_NAME,
        API_SERVICE_NAME,
        API_SERVICE_NAME,
        SCRIPTS_FOLDER_NAME,
        GENERATE_DATABASE_MIGRATION_SCRIPT_FILENAME,
    ),
    join(
        PROJECT_PACKAGE_NAME,
        API_SERVICE_NAME,
        API_SERVICE_NAME,
        SCRIPTS_FOLDER_NAME,
        MIGRATE_DATABASE_SCRIPT_FILENAME,
    ),
)


DATABASE_FOLDERS = (
    join(
        PROJECT_PACKAGE_NAME,
        API_SERVICE_NAME,
        API_SERVICE_NAME,
        ALEMBIC_FOLDER_NAME,
    ),
    join(
        PROJECT_PACKAGE_NAME,
        API_SERVICE_NAME,
        API_SERVICE_NAME,
        DATABASE_PACKAGE_NAME,
    ),
)


PYTHON_FILES_WITH_TEMPLATING = (
    join(
        PROJECT_PACKAGE_NAME,
        API_SERVICE_NAME,
        API_SERVICE_NAME,
        SETTINGS_PY_FILENAME,
    ),
)


if not ADD_DATABASE:
    for file_path in DATABASE_FILES:
        print(f"Removing '{file_path}' file")
        remove(file_path)

    for folder_path in DATABASE_FOLDERS:
        print(f"Removing '{folder_path}' folder")
        rmtree(folder_path)


for file_path in PYTHON_FILES_WITH_TEMPLATING:
    with open(file_path, "r") as opened_file:
        file_contents = opened_file.read()

    reg = "    #[\n]*"
    rep = ""

    replaced = re.sub(reg, rep, file_contents)

    with open(file_path, "w") as opened_file:
        opened_file.write(replaced)
