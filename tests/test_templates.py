import pathlib
import datetime
import pytest
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
        iterable = range(1000)
        result = tp.create_index_count_dictionary(iterable)
        assert isinstance(result, dict)
        assert len(result) == len(iterable)
        assert all([isinstance(key, int) for key in result.keys()])
        assert all([element == 0 for element in result.values()])
        assert max(result.keys()) == len(iterable) - 1
        assert tp.create_index_count_dictionary([]) == {}

    def test_create_indexed_dictionary_list(self):
        iterable = range(1000)
        result = tp.create_indexed_dictionary_list(iterable)
        assert isinstance(result, list)
        assert len(result) == len(iterable)
        for element, index in zip(result, iterable):
            assert isinstance(element, dict)
            assert set(element.keys()) == {"object", "index"}
            assert element["object"] == index
            assert element["index"] == index
        small_case = [25, datetime.date.today(), pathlib.Path()]
        result = tp.create_indexed_dictionary_list(small_case)
        assert len(result) == len(small_case)
        for element, case in zip(result, small_case):
            assert isinstance(element, dict)
            assert set(element.keys()) == {"object", "index"}
            assert element["object"] == case
        assert tp.create_indexed_dictionary_list([]) == []

    def test_create_matched_level_data(self):
        pass

    def test_gather_dictionary_counts(self):
        iterable = range(1000)
        result = tp.gather_dictionary_counts(iterable)
        assert isinstance(result, dict)
        assert len(result) == len(iterable)
        assert all([element == 1 for element in result.values()])
        assert all([isinstance(element, str) for element in result.keys()])
        small_case = ["bingo", 1, 2, 2, str(datetime.date.today())]
        result = tp.gather_dictionary_counts(small_case)
        assert len(result) == 4
        assert set(result.keys()) == {"bingo", "1", "2", str(datetime.date.today())}
        counts = [1, 1, 2, 1]
        for element, count in zip(result, counts):
            assert result[element] == count
        assert tp.gather_dictionary_counts([]) == {}

    def test_generate_directory_information(self):
        pass

    def test_get_file_path_list(self):
        pass

    def test_handle_list_stat_file(self):
        pass

    def test_handle_single_stat_file(self):
        pass

    def test_length_information_conversion(self):
        iterable = range(1000)
        result = tp.length_information_conversion(iterable)
        assert isinstance(result, list)
        assert len(result) == len(iterable)
        assert all([element == -1 for element in result])

        iterable = "thisismyreallylongstringforiterating"
        result = tp.length_information_conversion(iterable)
        assert isinstance(result, list)
        assert len(result) == len(iterable)
        assert all([element == 1 for element in result])

        small_case = ["test", range(100), datetime, []]
        result = tp.length_information_conversion(small_case)
        assert isinstance(result, list)
        assert len(result) == len(small_case)
        assert result == [4, 100, -1, 0]
        assert tp.length_information_conversion([]) == []

    def test_remove_indeces_from_list(self):
        iterable, removal = range(1000), range(1000)
        result = tp.remove_indeces_from_list(iterable, removal)
        assert isinstance(result, list)
        assert result == []

        result = tp.remove_indeces_from_list(iterable, [])
        assert result == iterable

        small_case = ["abc", {}, 100, ["test"], ()]
        removal = [1, 3, 8, 9, -1]
        result = tp.remove_indeces_from_list(small_case, removal)
        assert len(result) == 3
        assert result == ["abc", 100, ()]

    def test_take_larger_comparison(self):
        initial, compare = range(1000), range(1000)
        result = tp.take_larger_comparison(initial, compare)
        assert isinstance(result, list)
        assert list(initial) == result

        initial = [1, 3, 6, 9, 21, 24, 39]
        compare = [0, 4, 5, 11, 18, 23, 50]
        expected = [1, 4, 6, 11, 21, 24, 50]
        result = tp.take_larger_comparison(initial, compare)
        assert result == expected

        with pytest.raises(ValueError):
            tp.take_larger_comparison([], [0])
        assert tp.take_larger_comparison([], []) == []
