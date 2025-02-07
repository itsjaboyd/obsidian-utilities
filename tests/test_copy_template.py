from templates import copy_template as ct
import pytest
import datetime


class TestCopyTemplate:

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

    def test_calculate_multiple_copied_paths(self, tmp_path):
        tpf, tgd = self.helper_create_template_structure(tmp_path)
        empty_result = ct.calculate_multiple_copied_paths(tpf, tgd, 0)
        assert isinstance(empty_result, list)
        assert empty_result == []

        tgd_files = [
            tgd / "test.txt",
            tgd / "number-one.txt",
            tgd / "2025-01-01.txt",
        ]
        for tgd_file in tgd_files:
            tgd_file.touch()

        copy_expected = ct.calculate_multiple_copied_paths(tpf, tgd, 2)
        assert isinstance(empty_result, list)
        for index in range(len(copy_expected)):
            expected_name = f"{tpf.stem}-copy-{index}{tpf.suffix}"
            assert copy_expected[index].name == expected_name

        for tgd_file in tgd_files:
            tgd_file.unlink(missing_ok=True)
        tgd_files = [
            tgd / "20250101.txt",
            tgd / "20020202.txt",
            tgd / "16651212.txt",
        ]
        for tgd_file in tgd_files:
            tgd_file.touch()

        copy_expected = ct.calculate_multiple_copied_paths(tpf, tgd, 2)
        todays_date_iso = datetime.date.today().isoformat()
        todays_date_iso = todays_date_iso.replace("-", "")
        assert isinstance(empty_result, list)
        for index in range(len(copy_expected)):
            expected_name = f"{todays_date_iso}-copy-{index}{tpf.suffix}"
            assert copy_expected[index].name == expected_name

    def test_calculate_single_copied_paths(self, tmp_path):
        tpf, tgd = self.helper_create_template_structure(tmp_path)
        tgd_files = [
            tgd / "test.txt",
            tgd / "number-one.txt",
            tgd / "2025-01-01.txt",
        ]
        for tgd_file in tgd_files:
            tgd_file.touch()
        copy_name = tpf.stem + "-copy" + tpf.suffix
        result = ct.calculate_single_copied_paths(tpf, tgd)
        assert isinstance(result, list) and len(result) == 1
        assert result[-1].name == copy_name
        result = ct.calculate_single_copied_paths(tpf, tgd, False)
        assert result[-1].name == copy_name

        for tgd_file in tgd_files:
            tgd_file.unlink(missing_ok=True)
        tgd_files = [
            tgd / "20250101.txt",
            tgd / "20020202.txt",
            tgd / "16651212.txt",
        ]
        for tgd_file in tgd_files:
            tgd_file.touch()
        todays_date_iso = datetime.date.today().isoformat()
        todays_date_iso = todays_date_iso.replace("-", "")
        expected_name = todays_date_iso + tpf.suffix
        result = ct.calculate_single_copied_paths(tpf, tgd)
        assert isinstance(result, list) and len(result) == 1
        assert result[-1].name == expected_name
        result = ct.calculate_single_copied_paths(tpf, tgd, False)
        assert result[-1].name == copy_name

    def test_calculate_copied_paths(self):
        pass

    def test_copy_template(self, tmp_path):
        tfo, tdo = self.helper_create_template_structure(tmp_path)
        with pytest.raises(ValueError):
            ct.copy_template(tfo, tdo, number_copies=-1)
        assert ct.copy_template(tfo, tdo, number_copies=1) == [True]
        results = ct.copy_template(tfo, tdo, number_copies=100)
        assert len(results) == 100
        assert all(results)

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

    def test_verify_copies_target(self):
        pass

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
