"""
    Utilize a configuration file for loading and saving common configuration 
    settings used by the application. This module utilizes Python's configparser 
    to utilize a .ini style configuration file.

    Author: Jason Boyd
    Date: January 6, 2025
    Modified: January 14, 2025
"""

import configparser
import tomllib
import pathlib

# load the projects toml configuration for application items
with open("pyproject.toml", "rb") as f:
    PROJECT_CONFIGURATION = tomllib.load(f)

# get the name of the application and name of configuration file
NAMES = (
    PROJECT_CONFIGURATION["tool"]["poetry"]["name"],
    PROJECT_CONFIGURATION["application"]["config"]["config"],
)

# create the possible configuration file paths to search for
CONFIGURATION_PATHS = (
    pathlib.Path.home() / ".config" / NAMES[0] / NAMES[1],
    pathlib.Path.cwd() / ".config" / NAMES[0] / NAMES[1],
)


def get_configuration_path():
    """Find and return the currently existing configuration file path, in 
        order of priority starting with the users home directory, to the 
        project working directory.

    Returns:
        pathlib.Path: the newly created or already-existing configuration 
            file path that the application will use for configuration.
    """
    home_config = initialize_configuration_path(CONFIGURATION_PATHS[0])
    if home_config is not None:
        return home_config
    
    local_config = initialize_configuration_path(CONFIGURATION_PATHS[1])
    if local_config is not None:
        return local_config
    
def initialize_configuration_path(configuration_path):
    """Given a supposed configuration path, return if it exists, otherwise 
        step up through the parent directories to create the configuration 
        file and return the newly created, usable configuration file path.

    Args:
        configuration_path (pathlib.Path): the path to the configuration 
            file in question that will be used to identify.

    Returns:
        pathlib.Path: the already-existing or newly created by the function 
            configuration file path to use.
    """

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
    """Given a configuration file path, create a default configuration file 
        with the default sections and keys that the application will use.

    Args:
        configuration_path (pathlib.Path): the path to the configuration file 
            that will be created and updated with default values.
    """

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
    """Get the parsed configuration object from the configuration file 
        for the application.

    Returns:
        configParser.ConfigParser: the parsed configuration object that 
            the application uses.
    """
    found_configuration = get_configuration_path()
    configuration = configparser.ConfigParser()
    configuration.read(found_configuration)
    return configuration

def update_configuration(section, key, value):
    """Given a section, key, and value, update the configuration file with 
        the new values supplied by the caller.

    Args:
        section (str): the section header the key and value belong to.
        key (str): the key that will be updated with the new value.
        value (str): the value that will be updated in the configuration file.
    """
    
    config = get_configuration()
    config.set(section, key, value)
    with open(get_configuration_path(), "w") as f:
        config.write(f)
    