import datetime
from common import common as cm


class DateParser:
    def __init__(self, date_string, separator="-"):
        self.date_string = date_string
        self.separator = separator
        self.formatted = False
        self.category = None

    def __str__(self):
        pass

    def parse(self, string_object):
        # string object could be a single string or list of strings
        pass

    @staticmethod
    def iso_formatted_string(iso_string, common_characters):
        """Given a string, check if its ISO-formatted based on a list of common characters.

        Args:
            iso_string (str): the string to determine if its ISO-formatted.
            common_characters (iterable): the common characters to check formatting against.

        Returns:
            tuple: two elements, the first bool telling if iso_string is ISO-formatted, and
                the second string denoting the character that separates the ISO elements.
        """

        use_iso_string = str(iso_string)
        iso_separated_char = None
        if len(use_iso_string) not in [8, 10]:
            return (False, None)

        if len(iso_string) == 10:
            for common_char in common_characters:
                split_iso = iso_string.split(common_char)
                if DateParser.iso_proper_length_parts(split_iso):
                    use_iso_string = iso_string.replace(common_char, "-")
                    iso_separated_char = common_char
                    break
        try:
            new_date = datetime.date.fromisoformat(use_iso_string)
            return (True, iso_separated_char)
        except:
            return (False, iso_separated_char)

    @staticmethod
    def iso_proper_length_parts(iso_part_list):
        """Given an ISO-spearated parts list, determine if the lengths of its parts are
            ISO-formatted worthy.

        Args:
            iso_part_list (list): the parts of an ISO string that the function checks
                lengths against to determine ISO-formatted worthiness.

        Returns:
            bool: wether the parts list matches the ISO-formatted lengths required.
        """

        cm.check_argument_iterable(iso_part_list)
        if len(iso_part_list) != 3:
            return False
        if len(iso_part_list[0]) != 4:
            return False
        if len(iso_part_list[1]) == 3:
            if len(iso_part_list[2]) != 1:
                return False
        if len(iso_part_list[1]) == 2:
            if len(iso_part_list[2]) != 2:
                return False
        return True


def iso_formatted_list(string_list, common_characters):
    """Determine if a string list has all ISO-formatted elements based on a list of
        common characters.

    Args:
        string_list (_type_): the string list to determine if elements are ISO-formatted.
        common_characters (iterable): the common characters to check formatting against.

    Returns:
        tuple: two elements, the first bool telling if all list elements are ISO-formatted,
            and the second string denoting the character that separates the ISO elements.
    """
    cm.check_iterable_types(string_list, str)
    cm.check_iterable_types(common_characters, str)
    iso_formatted_results = [
        DateParser.iso_formatted_string(ifi, common_characters) for ifi in string_list
    ]
    results = list(zip(*iso_formatted_results))
    if all(results[0]) and len(set(results[1])) <= 1:
        return (True, results[1][-1])
    return (False, None)
