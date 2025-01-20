"""
    Utilize a configuration file for loading and saving common configuration 
    settings used by the application. This module utilizes the tomlkit package 
    for parsing and writing to a TOML configuration file.

    Author: Jason Boyd
    Date: January 6, 2025
    Modified: January 18, 2025
"""

import pathlib
import tomlkit
import platformdirs


# load the projects toml configuration for application items
module_parent = pathlib.Path(__file__).parent.parent.parent
configuration_toml = module_parent / "pyproject.toml"

try: # attempt to get the project config from package structure
    with open(configuration_toml, "r") as f:
        PROJECT_TOML = tomlkit.load(f)

    # get the name of the application and name of configuration file
    PROJECT_NAMES = (
        PROJECT_TOML["project"]["name"],
        PROJECT_TOML["project"]["authors"],
        PROJECT_TOML["application"]["config"],
    )
except FileNotFoundError as fnfe:
    print(f"{fnfe}\nProject configuration does not exist: {configuration_toml.resolve()}")
    PROJECT_NAMES = ("obsidian-utilities", "obsidian-utilities.toml")


class Configuration:
    """The Configuration class is used to load and save configuration settings 
        for the application. The configuration file is a TOML file that is loaded
        and saved using the tomlkit package. This class utlizes the platformdirs 
        package for a usable user configuration directory.

    Returns:
        Configuration: the Configuration object that is used to load and save 
            configuration settings for the application.
    """

    def __init__(self):
        """Find a suitable configuration path with platformdirs suggestion and 
            then create a default configuration file if one doesn't already 
            exist at the found confguration path.
        """

        self.user_configuration_path = platformdirs.user_config_path(
            PROJECT_NAMES[0],
            PROJECT_NAMES[1],
            ensure_exists=True
        )
        self.user_configuration_file = self.user_configuration_path / PROJECT_NAMES[2]
        if not self.user_configuration_file.is_file():
            self.user_configuration_file.touch()
            default_configuration = self.create_default_toml()
            self.write_configuration(default_configuration)


    def __str__(self):
        """Return a stringified version of the Configuration instance.

        Returns:
            str: the Configuration instance's config path and file.
        """

        self_string = "Configuration Object\n"
        self_string += f"User Config Path: {self.user_configuration_path}\n"
        self_string += f"User Config File: {self.user_configuration_file}"
        return self_string
    

    def get_configuration(self):
        """Read the configuration file saved in the Configuration object and 
            return its contents as a tomlkit TOMLDocument object.

        Returns:
            tomlkit.TOMLDocument: the loaded TOMLDocument found at the 
                configuration file location.
        """

        with open(self.user_configuration_file, "r") as cf:
            current_configuration = tomlkit.load(cf)
        return current_configuration
    

    def write_configuration(self, new_toml):
        """Write the new_toml TOMLDocument object to the saved configuration 
            file location, overwriting any previous configuration with the 
            new_toml object.

        Args:
            new_toml (tomlkit.TOMLDocument): the new TOMLDocument object to 
                write at the configuration file location.

        Raises:
            ValueError: if the supplied new_toml argument is not of 
                TOMLDocument type.
        """

        if not isinstance(new_toml, tomlkit.toml_document.TOMLDocument):
            raise ValueError("The configuration object must be of TOMLDocument type.")

        with open(self.user_configuration_file, "w") as cf:
            tomlkit.dump(new_toml, cf)


    def update_configuration(self, section, key, value):
        """Update the current configuration file with value that is found 
            under a secion and key, creating a new section and key if they 
            don't already exist.

        Args:
            section (str): the section header that the key and value belong to.
            key (str): the key that the value will be assigned to.
            value (str): the value that will be assigned to the key under section.
        """

        current_configuration = self.get_configuration()
        if section not in current_configuration:
            current_configuration.add(section, {})
        current_configuration[section][key] = value
        self.write_configuration(current_configuration)


    @staticmethod
    def create_default_toml():
        """Create a default tomlkit.TOMLDocument object structure that the 
            application will utilize during runtime.

        Returns:
            tomlkit.TOMLDocument: the final default TOMLDocument that the 
                application will utilize.
        """

        configuration_contents = tomlkit.document()
        configuration_comment = tomlkit.comment("Application Configuration")
        configuration_contents.add(configuration_comment)
        paths = tomlkit.table()
        paths.add("templates", "")
        paths.add("dailys", "")
        configuration_contents.add("PATHS", paths)
        print(type(configuration_contents))
        return configuration_contents