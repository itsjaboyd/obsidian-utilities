import pytest
import pathlib
from common import common as cm


class TestCommon:
    def test_check_argument_iterable(self):
        with pytest.raises(Exception):
            cm.check_argument_iterable(0)
        for iterable in [[], (), {}, ""]:
            assert cm.check_argument_iterable(iterable)

    def test_check_iterable_types(self):
        with pytest.raises(Exception):
            cm.check_iterable_types(0, int)
        good_iterables = [[0], [""], [pathlib.Path()]]
        good_checks = [int, str, pathlib.Path]
        for iterable, check in zip(good_iterables, good_checks):
            assert cm.check_iterable_types(iterable, check)

        bad_checks = [dict, set, int]
        for iterable, check in zip(good_iterables, bad_checks):
            with pytest.raises(ValueError):
                cm.check_iterable_types(iterable, check)

        bad_iterables = [[0, ""], ["", ()], [pathlib.Path(), 0]]
        for iterable, check in zip(bad_iterables, good_checks):
            with pytest.raises(ValueError):
                cm.check_iterable_types(iterable, check)

    def test_check_argument_type(self):
        arguments = [0, "", {}, (), [], pathlib.Path()]
        good_types = [int, str, dict, tuple, list, pathlib.Path]
        for arg, tp in zip(arguments, good_types):
            assert cm.check_argument_type(arg, tp)

        bad_types = [list, int, str, pathlib.Path, dict, set]
        for arg, tp in zip(arguments, bad_types):
            with pytest.raises(ValueError):
                cm.check_argument_type(arg, tp)

    def test_attempt_pathlike_extraction(self, tmp_path):
        file_one = tmp_path / "file-one.txt"
        assert file_one == cm.attempt_pathlike_extraction(file_one)
        file_two = "file-two.txt"
        result = cm.attempt_pathlike_extraction(file_two)
        assert isinstance(result, pathlib.Path)
        assert file_two == result.name

        bad_suppliers = [0, {}, [], ()]
        for supplier in bad_suppliers:
            with pytest.raises(ValueError):
                result = cm.attempt_pathlike_extraction(supplier)
