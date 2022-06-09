from os import getenv


STAGING_LEVEL_ENVIRONMENT_VARIABLE = "ENV"
DEFAULT_STAGING_LEVEL = "dev"


STAGING_LEVEL_FILENAME_TEMPLATE_PARAMETER = "staging_level"
STAGING_LEVEL_FILENAME_TEMPLATE = f"{{{STAGING_LEVEL_FILENAME_TEMPLATE_PARAMETER}}}.env"


def get_staging_level():
    return getenv(STAGING_LEVEL_ENVIRONMENT_VARIABLE, DEFAULT_STAGING_LEVEL)


def get_environment_file():
    staging_level = get_staging_level()
    filename = STAGING_LEVEL_FILENAME_TEMPLATE.format(
        **{STAGING_LEVEL_FILENAME_TEMPLATE_PARAMETER: staging_level}
    )
    return filename
