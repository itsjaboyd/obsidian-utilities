from templates import copy_template as ct
import pytest
import datetime


class TestCopyTemplate:

    def test_compute_spread(self):
        zero_spread = ["one", "two", "six"]
        one_spread = ["one", "two", "four"]
        ten_spread = ["one", "twenty-sevens"]

        assert ct.compute_spread(zero_spread) == 0
        assert ct.compute_spread(one_spread) == 1
        assert ct.compute_spread(ten_spread) == 10

    def test_find_common_position_characters(self):
        common_one = ["app", "apple", "apricot"]
        common_two = ["jason", "lakom", "casom"]
        common_none = ["jimmy", "alpha", "corona"]

        assert ct.find_common_position_characters(common_one) == ["a", "p"]
        assert ct.find_common_position_characters(common_two) == ["a", "o"]
        assert ct.find_common_position_characters(common_none) == []

    def test_iso_proper_length_parts(self):
        good_parts_one = ["2025", "01", "01"]
        good_parts_two = ["1999", "W03", "1"]
        bad_parts_one = ["2025", "01"]
        bad_parts_two = ["20501", "01", "01"]
        bad_parts_three = ["2025", "W03", "12"]
        bad_parts_four = ["2025", "01", "1"]

        assert ct.iso_proper_length_parts(good_parts_one)
        assert ct.iso_proper_length_parts(good_parts_two)
        assert not ct.iso_proper_length_parts(bad_parts_one)
        assert not ct.iso_proper_length_parts(bad_parts_two)
        assert not ct.iso_proper_length_parts(bad_parts_three)
        assert not ct.iso_proper_length_parts(bad_parts_four)

    def test_process_template_location(self, tmp_path):
        non_path = tmp_path / "non_path"
        with pytest.raises(FileNotFoundError):
            ct.process_template_location(non_path)
        non_path.mkdir()
        with pytest.raises(IsADirectoryError):
            ct.process_template_location(non_path)
        non_file = non_path / "non_file.txt"
        with pytest.raises(FileNotFoundError):
            ct.process_template_location(non_file)
        non_file.touch()
        assert ct.process_template_location(non_file) == non_file

    def test_process_directory_location(self, tmp_path):
        non_path = tmp_path / "non_path"
        with pytest.raises(FileNotFoundError):
            ct.process_directory_location(non_path)
        non_file = tmp_path / "non_file.txt"
        non_file.touch()
        with pytest.raises(NotADirectoryError):
            ct.process_directory_location(non_file)
        non_path.mkdir()
        assert ct.process_directory_location(non_path) == non_path

    def test_iso_formatted_string(self):
        good_iso_one, good_chars_one = "2025-01-01", ["-"]
        good_iso_two, good_chars_two = "2025_W03_1", ["-", "_"]
        good_iso_three, good_chars_three = "20250101", []
        good_iso_four, good_chars_four = "2025M01M01", ["M", "N", "P"]
        bad_iso_one, bad_chars_one = "2025-01", ["-"]
        bad_iso_two, bad_chars_two = "202501011", ["-"]
        bad_iso_three, bad_chars_three = "2025-W01-01", []
        bad_iso_four, bad_chars_four = 1234567, ["_", "M"]

        assert ct.iso_formatted_string(good_iso_one, good_chars_one) == (True, "-")
        assert ct.iso_formatted_string(good_iso_two, good_chars_two) == (True, "_")
        assert ct.iso_formatted_string(good_iso_three, good_chars_three) == (True, None)
        assert ct.iso_formatted_string(good_iso_four, good_chars_four) == (True, "M")
        assert ct.iso_formatted_string(bad_iso_one, bad_chars_one) == (False, None)
        assert ct.iso_formatted_string(bad_iso_two, bad_chars_two) == (False, None)
        assert ct.iso_formatted_string(bad_iso_three, bad_chars_three) == (False, None)
        assert ct.iso_formatted_string(bad_iso_four, bad_chars_four) == (False, None)

    def test_iso_formatted_list(self):
        good_iso_one, good_chars_one = ["2025-01-01", "2025-01-02"], []
        good_iso_two, good_chars_two = ["2025PW01P1", "2025PW01P2"], ["-", "P"]
        good_iso_three, good_chars_three = ["20250101", "20250102"], ["2", "5"]
        bad_iso_one, bad_chars_one = ["2025-01-01", "2025-01"], ["-"]
        bad_iso_two, bad_chars_two = ["20250101", "202501011"], ["2", "5"]
        bad_iso_three, bad_chars_three = ["2025-W01-01", "2025-W01-2"], []

        assert ct.iso_formatted_list(good_iso_one, good_chars_one) == (True, None)
        assert ct.iso_formatted_list(good_iso_two, good_chars_two) == (True, "P")
        assert ct.iso_formatted_list(good_iso_three, good_chars_three) == (True, None)
        assert ct.iso_formatted_list(bad_iso_one, bad_chars_one) == (False, None)
        assert ct.iso_formatted_list(bad_iso_two, bad_chars_two) == (False, None)
        assert ct.iso_formatted_list(bad_iso_three, bad_chars_three) == (False, None)

    def test_copy_template_handler(self, tmp_path):
        template_dir = tmp_path / "template_dir"
        template_dir.mkdir()
        template_file = template_dir / "template_file.txt"
        template_file.touch()

        already_file = tmp_path / "already_file.txt"
        already_file.touch()
        with pytest.raises(FileExistsError):
            ct.copy_template_handler(template_file, already_file)
        with pytest.raises(IsADirectoryError):
            ct.copy_template_handler(template_file, template_dir)
        good_target_one = tmp_path / "good_target_one.txt"
        assert ct.copy_template_handler(template_file, good_target_one) == True
        good_target_two = tmp_path / "good_target_two.txt"
        assert ct.copy_template_handler(template_dir, good_target_two) == False

    def test_copy_template_single(self, tmp_path):
        temp_paths = [
            tmp_path / "temp_path_one",
            tmp_path / "temp_path_two",
            tmp_path / "temp_path_three",
        ]
        for temp_path in temp_paths:
            temp_path.mkdir()

        iso_files_one = ["2025-01-01.txt", "2025-01-02.txt"]
        expected_file_one = datetime.date.today().isoformat() + ".txt"
        self.helper_copy_template_single(
            iso_files_one, expected_file_one, temp_paths[0]
        )

        iso_files_two = ["2025-01-01.txt", "2025_01_02.txt"]
        expected_file_two = "template_file-copy.txt"
        self.helper_copy_template_single(
            iso_files_two, expected_file_two, temp_paths[1]
        )

        iso_files_three = ["20250101.txt", "20250102.txt"]
        expected_file_three = (
            datetime.date.today().isoformat().replace("-", "") + ".txt"
        )
        self.helper_copy_template_single(
            iso_files_three, expected_file_three, temp_paths[2]
        )

    def test_copy_template_multiple(self, tmp_path):
        tfo, tdo = self.helper_create_template_structure(tmp_path / "one")
        results_one = ct.copy_template_multiple(tfo, tdo, number_copies=5)
        assert isinstance(results_one, list)
        assert len(results_one) == 5
        assert all(results_one)

        tft, tdt = self.helper_create_template_structure(tmp_path / "two")
        results_two = ct.copy_template_multiple(tft, tdt, number_copies=20)
        assert isinstance(results_two, list)
        assert len(results_two) == 20
        assert all(results_two)

        tfth, tdth = self.helper_create_template_structure(tmp_path / "three")
        results_three = ct.copy_template_multiple(tfth, tdth, number_copies=0)
        assert isinstance(results_three, list)
        assert len(results_three) == 0

    def test_copy_template(self, tmp_path):
        tfo, tdo = self.helper_create_template_structure(tmp_path)
        with pytest.raises(ValueError):
            ct.copy_template(tfo, tdo, number_copies=-1)
        assert ct.copy_template(tfo, tdo, number_copies=1) == [True]
        results = ct.copy_template(tfo, tdo, number_copies=100)
        assert len(results) == 100
        assert all(results)

    def test_analyze_directory(self, tmp_path):
        usual_result = {
            "detected_formatting": False,
            "formatting_type": None,
            "formatting_separator": None,
        }
        temp_paths = [
            tmp_path / "temp_path_one",
            tmp_path / "temp_path_two",
            tmp_path / "temp_path_three",
        ]
        for temp_path in temp_paths:
            temp_path.mkdir()

        first_result = ct.analyze_directory(tmp_path)
        assert first_result == usual_result

        template_file_one, target_dir_one = self.helper_create_template_structure(
            temp_paths[0]
        )
        ct.copy_template(template_file_one, target_dir_one, number_copies=10)
        second_result = ct.analyze_directory(target_dir_one)
        assert second_result == usual_result

        first_iso_files = [
            temp_paths[1] / "2025-01-01.txt",
            temp_paths[1] / "2025-01-02.txt",
        ]
        for iso_file in first_iso_files:
            iso_file.touch()

        third_result = ct.analyze_directory(temp_paths[1])
        assert third_result["detected_formatting"]
        assert third_result["formatting_type"] == "ISO"
        assert third_result["formatting_separator"] == "-"

        second_iso_files = [
            temp_paths[2] / "20250101.txt",
            temp_paths[2] / "20250102.txt",
        ]
        for iso_file in second_iso_files:
            iso_file.touch()
        fourth_result = ct.analyze_directory(temp_paths[2])
        assert fourth_result["detected_formatting"]
        assert fourth_result["formatting_type"] == "ISO"
        assert fourth_result["formatting_separator"] == None

    def helper_copy_template_single(self, iso_names, expected_file, temp_path):
        template_file, target_dir = self.helper_create_template_structure(temp_path)

        iso_files = [target_dir / iso_name for iso_name in iso_names]
        for iso_file in iso_files:
            iso_file.touch()

        result = ct.copy_template_single(template_file, target_dir)
        print(result)
        assert isinstance(result, list)
        assert all(result)
        copied_file = target_dir / expected_file
        assert copied_file.exists()

    @staticmethod
    def helper_create_template_structure(temp_path):
        template_dir = temp_path / "template_dir"
        template_dir.mkdir(parents=True)
        template_file = template_dir / "template_file.txt"
        template_file.touch()
        target_dir = temp_path / "target_dir"
        target_dir.mkdir(parents=True)
        return template_file, target_dir
