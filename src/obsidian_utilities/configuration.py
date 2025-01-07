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


def initialize_configuration():
    home_config = CONFIGURATION_PATHS[0]
    if home_config.exists(): # found a .config home directory
        return home_config
    elif home_config.parent.exists():
        home_config.touch(exist_ok=True)
        return home_config
    elif home_config.parent.parent.exists():
        home_config.parent.mkdir()
        home_config.touch(exist_ok=True)
        return home_config
    
    local_config = CONFIGURATION_PATHS[1]
    if local_config.exists(): # found a .config local directory
        return local_config
    elif local_config.parent.exists():
        local_config.touch(exist_ok=True)
        return local_config
    elif local_config.parent.parent.exists():
        local_config.parent.mkdir()
        local_config.touch(exist_ok=True)
        return local_config


def get_configuration():
    found_configuration = initialize_configuration()
    configuration = configparser.ConfigParser()
    configuration.read(found_configuration)
    return configuration
    