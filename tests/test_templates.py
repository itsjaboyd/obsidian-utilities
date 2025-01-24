import pathlib
import datetime
from templates import templates as tp


class TestTemplates:
    def test_build_table_string(self):
        pass

    def test_calculate_maximum_length(self):
        pass

    def test_convert_seconds_iso(self):
        good_seconds = [1733759516, 1537249319, 1737749516]
        good_results = [
            "2024-12-09 08:51:56",
            "2018-09-17 23:41:59",
            "2025-01-24 13:11:56",
        ]
        for second, result in zip(good_seconds, good_results):
            assert result == tp.convert_seconds_iso(second)
            assert isinstance(result, str)
        bad_seconds = ["test", None, pathlib.Path()]
        for sec in bad_seconds:
            result = tp.convert_seconds_iso(sec)
            assert result == ""
            assert isinstance(result, str)

    def test_create_directory_table(self):
        pass

    def test_create_filename_level(self):
        pass

    def test_create_filename_list(self):
        pass

    def test_create_filename_stats(self):
        pass

    def test_create_headers_from_codes(self):
        full_code_list = ["fn", "ct", "mt", "sz"]
        assert tp.create_headers_from_codes(full_code_list) == [
            "Filenames",
            "Creation Date",
            "Modified Date",
            "Size",
        ]
        none_code_list = ["bt", "fu", "zz"]
        unknown = set(tp.create_headers_from_codes(none_code_list))
        assert unknown == {"Unknown"}
        bad_code_list = [1, pathlib.Path(), None]
        bad_codes = set(tp.create_headers_from_codes(bad_code_list))
        assert bad_codes == {"Unknown"}
        assert tp.create_headers_from_codes([]) == []

    def test_create_index_count_dictionary(self):
        pass

    def test_create_indexed_dictionary_list(self):
        pass

    def test_create_matched_level_data(self):
        pass

    def test_gather_dictionary_counts(self):
        pass

    def test_generate_directory_information(self):
        pass

    def test_get_file_path_list(self):
        pass

    def test_handle_list_stat_file(self):
        pass

    def test_handle_single_stat_file(self):
        pass

    def test_length_information_conversion(self):
        pass

    def test_remove_indeces_from_list(self):
        pass

    def test_take_larger_comparison(self):
        pass
