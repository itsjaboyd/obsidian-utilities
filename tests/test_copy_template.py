from src.templates import copy_template as ct
import pytest

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
        pass


    def test_copy_template_single(self):
        pass


    def test_copy_template_multiple(self):
        pass


    def test_copy_template(self):
        pass


    def test_analyze_directory(self):
        pass



