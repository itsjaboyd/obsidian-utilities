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
        
        good_path_one = tmp_path / "test-config-path-one"
        good_path_one.mkdir()
        good_file_one = good_path_one / cf.PROJECT_NAMES[2]
        good_file_one.touch() # create a config file so a default isn't created
        config = cf.Configuration(supplied_path=good_file_one)
        assert config.user_configuration_path.resolve() == good_path_one.resolve()
        assert config.user_configuration_file.resolve() == good_file_one.resolve()
        assert config.user_configuration_file.stat().st_size == 0
        
        good_path_two = tmp_path / "test-config-path-two"
        good_path_two.mkdir()
        good_file_two = good_path_two / cf.PROJECT_NAMES[2]
        for create_element in [good_path_two, good_file_two]:
            config = cf.Configuration(supplied_path=create_element)
            assert config.user_configuration_path.resolve() == good_path_two.resolve()
            assert config.user_configuration_file.resolve() == good_file_two.resolve()
            assert config.create_default_toml() == config.get_configuration()


    def test_configuration_string(self, tmp_path):
        config = cf.Configuration()
        platform_paths = self.get_platform_paths()
        config_string = "Configuration Object\n"
        config_string += f"User Config Path: {platform_paths[0]}\n"
        config_string += f"User Config File: {platform_paths[1]}"
        assert str(config) == config_string

        good_path = tmp_path / "test-config-path-one"
        good_path.mkdir()
        good_file = good_path / cf.PROJECT_NAMES[2]
        for create_element in [good_path, good_file]:
            config = cf.Configuration(supplied_path=create_element)
            config_string = "Configuration Object\n"
            config_string += f"User Config Path: {good_path}\n"
            config_string += f"User Config File: {good_file}"
            assert str(config) == config_string
        

    def test_get_configuration(self, tmp_path):
        good_path = tmp_path / "test-config-path-one"
        good_path.mkdir()
        config = cf.Configuration(supplied_path=good_path)
        assert config.create_default_toml() == config.get_configuration()
        assert isinstance(config.get_configuration(), tomlkit.TOMLDocument)

        modified_toml = tomlkit.document()
        testing_table = tomlkit.table()
        testing_table.add("name", "test-name")
        testing_table.add("result", "test-result")
        modified_toml.add("TESTING", testing_table)
        config.write_configuration(modified_toml)
        assert modified_toml == config.get_configuration()
        assert isinstance(config.get_configuration(), tomlkit.TOMLDocument)
        



    def test_write_configuration(self):
        pass

    def test_update_configuration(self):
        pass

    def test_create_deafult_toml(self):
        pass


    @staticmethod
    def get_platform_paths():
        path_platform = platformdirs.user_config_path(
            cf.PROJECT_NAMES[0],
            cf.PROJECT_NAMES[1],
            ensure_exists=False
        )
        user_path_platform = path_platform
        user_file_platform = path_platform / cf.PROJECT_NAMES[2] 
        return (user_path_platform, user_file_platform)
    
