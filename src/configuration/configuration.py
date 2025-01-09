import configparser
import tomllib
import pathlib

with open("pyproject.toml", "rb") as f:
    PROJECT_CONFIGURATION = tomllib.load(f)

NAMES = (
    PROJECT_CONFIGURATION["tool"]["poetry"]["name"],
    PROJECT_CONFIGURATION["tool"]["poetry"]["config"],
)

CONFIGURATION_PATHS = (
    pathlib.Path.home() / ".config" / NAMES[0] / NAMES[1],
    pathlib.Path.cwd() / ".config" / NAMES[0] / NAMES[1],
)


def get_configuration_path():
    home_config = initialize_configuration_path(CONFIGURATION_PATHS[0])
    if home_config is not None:
        return home_config
    
    local_config = initialize_configuration_path(CONFIGURATION_PATHS[1])
    if local_config is not None:
        return local_config
    
def initialize_configuration_path(configuration_path):
    if configuration_path.exists():
        return configuration_path
    elif configuration_path.parent.exists():
        configuration_path.touch(exist_ok=True)
        create_default_configuration(configuration_path)
        return configuration_path
    elif configuration_path.parent.parent.exists():
        configuration_path.parent.mkdir()
        configuration_path.touch(exist_ok=True)
        create_default_configuration(configuration_path)
        return configuration_path
    return None

def create_default_configuration(configuration_path):
    configuration_contents = [
        "[DEFAULT]\n",
        "\n",
        "[TEMPLATE]\n",
        "directory =\n",
        "\n",
        "[DAILY]\n",
        "directory =\n",
    ]
    with open(configuration_path, "w") as f:
        f.writelines(configuration_contents)

def get_configuration():
    found_configuration = get_configuration_path()
    configuration = configparser.ConfigParser()
    configuration.read(found_configuration)
    return configuration
    