from templates import copy_template as ct

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


    def test_process_template_location(self):
        pass


    def test_process_directory_location(self):
        pass


    def test_iso_formatted_string(self):
        pass


    def test_iso_formatted_list(self):
        pass


    def test_copy_template_handler(self):
        pass


    def test_copy_template_single(self):
        pass


    def test_copy_template_multiple(self):
        pass


    def test_copy_template(self):
        pass


    def test_analyze_directory(self):
        pass


    
