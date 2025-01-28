import pathlib
import datetime
import pytest
import random
from templates import templates as tp


class TestTemplates:
    def test_build_table_string(self):
        pass

    def test_calculate_maximum_length(self):
        iterable = [range(1000) for el in range(1000)]
        result = tp.calculate_maximum_length(iterable)
        assert isinstance(result, list)
        assert len(iterable) == len(result)
        expected = {-1 + tp.TABLE_SPACING}
        assert set(result) == expected

        small_case = ["testing", "templates", "fun"]
        result = tp.calculate_maximum_length(small_case)
        assert isinstance(result, list)
        assert len(small_case) == len(result)
        expected = [1 + tp.TABLE_SPACING for el in range(len(small_case))]
        assert result == expected

        result = tp.calculate_maximum_length([[]])
        assert isinstance(result, list)
        assert len(result) == 1
        assert result == [tp.TABLE_SPACING]

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

    def test_create_filename_level(self, tmp_path):
        zero_case = tmp_path
        result = tp.create_filename_level(tmp_path, 0)
        assert result == tmp_path.name
        result = tp.create_filename_level(tmp_path, -100)
        assert result == ""

        expected_levels = "level-one/level-two/level-three.txt"
        small_case = tmp_path / "level-one" / "level-two" / "level-three.txt"
        result = tp.create_filename_level(small_case, 2)
        assert result == expected_levels

        result = tp.create_filename_level(small_case, 100)
        print(result)
        assert f"/{result}" == f"{tmp_path}/{expected_levels}"

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

    def test_get_file_path_list(self, tmp_path):
        three_tests = [
            tmp_path / "test-one",
            tmp_path / "test-two",
            tmp_path / "test-three",
        ]

        for test_path in three_tests:
            with pytest.raises(ValueError):
                tp.get_file_path_list(test_path)

            test_path.mkdir()
            first_result = tp.get_file_path_list(test_path)
            assert isinstance(first_result, list)
            assert len(first_result) == 0

            random_amount = random.randint(0, 4)
            random_levels = random.randint(0, 4)

            self.build_file_tree(test_path, random_amount, random_levels)
            expected_length = self.calculate_file_tree_count(
                random_amount, random_levels
            )
            second_result = tp.get_file_path_list(test_path)
            assert isinstance(second_result, list)
            assert len(second_result) == expected_length

    def test_handle_list_stat_file(self, tmp_path):
        # build a file tree strucutre of 5 files, 5 dirs at 5 levels deep
        self.build_file_tree(tmp_path, 3, 3)
        filename_list = tp.get_file_path_list(tmp_path)
        possible_codes = ["mt", "ct", "at", "sz", "bb", 0, None]
        expected_results = [
            [
                tp.convert_seconds_iso(test_result.stat().st_mtime)
                for test_result in filename_list
            ],
            [
                tp.convert_seconds_iso(test_result.stat().st_birthtime)
                for test_result in filename_list
            ],
            [
                tp.convert_seconds_iso(test_result.stat().st_atime)
                for test_result in filename_list
            ],
            ["0.0 KB" for temp in range(len(filename_list))],
            ["" for temp in range(len(filename_list))],
            ["" for temp in range(len(filename_list))],
            ["" for temp in range(len(filename_list))],
        ]
        for code, expected in zip(possible_codes, expected_results):
            results = tp.handle_list_stat_file(filename_list, code)
            assert isinstance(results, list)
            assert len(results) == len(expected)
            for res, exp in zip(results, expected):
                assert res == exp

    def test_handle_single_stat_file(self, tmp_path):
        test_files = [tmp_path / f"test_file_{index}" for index in range(100)]
        for test_file in test_files:
            test_file.touch()

        possible_codes = ["mt", "ct", "at", "sz", "bb", 0, None]
        for test_file in test_files:
            expected_results = [
                tp.convert_seconds_iso(test_file.stat().st_mtime),
                tp.convert_seconds_iso(test_file.stat().st_birthtime),
                tp.convert_seconds_iso(test_file.stat().st_atime),
                "0.0 KB",
                "",
                "",
                "",
            ]
            for code, expected in zip(possible_codes, expected_results):
                assert tp.handle_single_stat_file(test_file, code) == expected
        directory = tmp_path / "directory"
        directory.mkdir()
        assert tp.handle_single_stat_file(directory, "mt") == ""
        assert tp.handle_single_stat_file(tmp_path / "dir", "mt") == ""

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

    def build_file_tree(self, supplied_path, total_each, levels):
        """Build a file/directory structure where each level includes
        total_each of files and directories. For each leve, then
        recursively build the same number of files and directories
        in each created directory.

        Total Files: sum of (total_each ** levels for each level > 0)
        Total Dirs: same as number of files.
        Total: total files + total dirs
        """

        if levels == 0:
            return

        for index in range(total_each):
            current_name = f"f-{index}-l-{levels}.txt"
            new_file = supplied_path / current_name
            new_file.touch()

        for index in range(total_each):
            current_name = f"d-{index}-l-{levels}"
            new_directory = supplied_path / current_name
            new_directory.mkdir()

            self.build_file_tree(new_directory, total_each, levels - 1)

    @staticmethod
    def calculate_file_tree_count(total_each, levels):
        return sum([total_each**level for level in range(levels, 0, -1)])
