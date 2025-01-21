from configuration import configuration as cf
import platformdirs
import tomlkit
import pytest


class TestConfiguration:
    def test_create_platform_configuration(self):
        config = cf.Configuration()
        platform_paths = self.get_platform_paths()
        assert config.user_configuration_path.resolve() == platform_paths[0].resolve()
        assert config.user_configuration_file.resolve() == platform_paths[1].resolve()

    def test_create_supplied_configuration(self, tmp_path):
        with pytest.raises(ValueError):
            dne_path = tmp_path / "dne-path"
            cf.Configuration(supplied_path=dne_path)

        test_path, test_file = self.create_path_file(tmp_path, "tcpa", empty_file=True)
        config = cf.Configuration(supplied_path=test_file)
        assert config.user_configuration_path.resolve() == test_path.resolve()
        assert config.user_configuration_file.resolve() == test_file.resolve()
        assert config.user_configuration_file.stat().st_size == 0

        test_path, test_file = self.create_path_file(tmp_path, "tcpb")
        for create_element in [test_path, test_file]:
            config = cf.Configuration(supplied_path=create_element)
            assert config.user_configuration_path.resolve() == test_path.resolve()
            assert config.user_configuration_file.resolve() == test_file.resolve()
            assert config.create_default_toml() == config.get_configuration()

    def test_configuration_string(self, tmp_path):
        config = cf.Configuration()
        platform_paths = self.get_platform_paths()
        config_string = "Configuration Object\n"
        config_string += f"User Config Path: {platform_paths[0]}\n"
        config_string += f"User Config File: {platform_paths[1]}"
        assert str(config) == config_string

        test_path, test_file = self.create_path_file(tmp_path, "tcpa")
        for create_element in [test_path, test_file]:
            config = cf.Configuration(supplied_path=create_element)
            config_string = "Configuration Object\n"
            config_string += f"User Config Path: {test_path}\n"
            config_string += f"User Config File: {test_file}"
            assert str(config) == config_string

    def test_get_configuration(self, tmp_path):
        test_path, test_file = self.create_path_file(tmp_path, "tcpa", "cc.toml")
        config = cf.Configuration(supplied_path=test_path)
        assert config.create_default_toml() == config.get_configuration()
        assert isinstance(config.get_configuration(), tomlkit.TOMLDocument)

        test_file.touch()
        config = cf.Configuration(supplied_path=test_file)
        # an empty file is essentially just an empty tomlkit document
        assert tomlkit.document() == config.get_configuration()
        assert isinstance(config.get_configuration(), tomlkit.TOMLDocument)

        modified_toml = self.create_testing_toml()
        config.write_configuration(modified_toml)
        assert modified_toml == config.get_configuration()
        assert isinstance(config.get_configuration(), tomlkit.TOMLDocument)

    def test_write_configuration(self, tmp_path):
        test_path, test_file = self.create_path_file(tmp_path, "tcpa")
        config = cf.Configuration(supplied_path=test_path)

        with pytest.raises(ValueError):
            config.write_configuration(None)

        test_toml = self.create_testing_toml()
        assert config.create_default_toml() == config.get_configuration()
        config.write_configuration(test_toml)
        assert test_toml == config.get_configuration()

    def test_update_configuration(self, tmp_path):
        test_path, test_file = self.create_path_file(tmp_path, "tcpa")
        config = cf.Configuration(supplied_path=test_path)

        matching_toml = config.create_default_toml()
        runtime_table = tomlkit.table()
        runtime_table.add("purpose", "notes")
        matching_toml.add("RUNTIME", runtime_table)
        config.update_configuration("RUNTIME", "purpose", "notes")
        assert matching_toml == config.get_configuration()

        matching_toml["PATHS"]["templates"] = "testing"
        config.update_configuration("PATHS", "templates", "testing")
        assert matching_toml == config.get_configuration()

    def test_create_deafult_toml(self, tmp_path):
        config = cf.Configuration(supplied_path=tmp_path)
        configuration_contents = tomlkit.document()
        configuration_comment = tomlkit.comment("Application Configuration")
        configuration_contents.add(configuration_comment)
        paths = tomlkit.table()
        paths.add("templates", "")
        paths.add("dailys", "")
        configuration_contents.add("PATHS", paths)
        assert config.create_default_toml() == configuration_contents

    @staticmethod
    def get_platform_paths():
        path_platform = platformdirs.user_config_path(
            cf.PROJECT_NAMES[0], cf.PROJECT_NAMES[1], ensure_exists=False
        )
        user_path_platform = path_platform
        user_file_platform = path_platform / cf.PROJECT_NAMES[2]
        return (user_path_platform, user_file_platform)

    @staticmethod
    def create_path_file(
        input_path, path_name, file_name=cf.PROJECT_NAMES[2], empty_file=False
    ):
        configuration_path = input_path / path_name
        configuration_path.mkdir()
        configuration_file = configuration_path / file_name
        if empty_file:
            configuration_file.touch()
        return (configuration_path, configuration_file)

    @staticmethod
    def create_testing_toml():
        modified_toml = tomlkit.document()
        testing_table = tomlkit.table()
        testing_table.add("name", "test-name")
        testing_table.add("result", "test-result")
        modified_toml.add("TESTING", testing_table)
        return modified_toml
