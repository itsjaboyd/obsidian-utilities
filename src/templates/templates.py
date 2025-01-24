"""General template module that includes functions related 
    to template directories and template files within an 
    obsidian vault location. 

    Author: Jason Boyd
    Date: January 20, 2025
    Modified: January 23, 2025
"""

import pathlib
import datetime
from common import common as cm

TABLE_SPACING = 5


def build_table_string(information):
    """Given a tuple of information (generated from generate_directory_information
        function), build a string that includes a table with a header and the
        coinciding data of each file found in information.

    Args:
        information (tuple): the three-object tuple to build the string table
            from, which again comes from generate_directory_information().

    Raises:
        ValueError: if the supplied information object is not of tuple type.
        ValueError: if the supplied information object does not have size 3.

    Returns:
        str: the table representation of header and data supplied in information.
    """

    cm.check_argument_type(information, tuple)
    if len(information) != 3:
        raise ValueError(f"Supplied information has incorrect length: {information}")

    header_info, zipped_info, length_info = information
    # create the header of the table string that contains column names
    header_string, main_string = "", ""
    for item_index in range(len(header_info)):
        header_string += format(
            header_info[item_index],
            f"<{length_info[item_index]}",
        )
    # create a divider exactly the length of data in the body
    header_string += f"\n{"-" * (sum(length_info) - TABLE_SPACING)}\n"
    # create the body of the table containing data in zipped_info
    for packaged_data in zipped_info:
        for data_index in range(len(packaged_data)):
            main_string += format(
                packaged_data[data_index],
                f"<{length_info[data_index]}",
            )
        main_string += "\n"

    return header_string + main_string


def calculate_maximum_length(multi_information_list):
    """Provided a multidimensional iterable, for each item calculate the
        maximum length present in its iterable and return a list designating
        the maximum length found in each sub-iterable.

    Args:
        multi_information_list (iterable(iterable)): the multidimensional
            iterable oject to extract maximum lengths from.

    Returns:
        list: the list containing the maximum lengths found for each sub-
            iterable. The length of this list should match the length of
            the supplied multi_information_list.
    """

    cm.check_argument_iterable(multi_information_list)
    length_information = []
    for check_list in multi_information_list:
        cm.check_argument_iterable(check_list)
        length_list = length_information_conversion(check_list)
        current_spacing = TABLE_SPACING
        if length_list:
            current_spacing = max(length_list) + TABLE_SPACING
        length_information.append(current_spacing)
    return length_information


def convert_seconds_iso(seconds):
    """Given an integer amount of seconds, attempt to convert this timestamp
        into an ISO-formatted string that extends to the seconds time data-point.

    Args:
        seconds (int): the amount of seconds to convert into ISO-string.

    Returns:
        str: the ISO-formatted string found from the timestamp seconds.
    """

    try:  # attempt to convert seconds into an ISO-formatted date
        datetime_instance = datetime.datetime.fromtimestamp(seconds)
        return datetime_instance.isoformat(sep=" ", timespec="seconds")
    except:  # user supplied something other than an integer for conversion
        return ""


def create_filename_level(path_object, number_levels):
    """Given a path-like object, return its string name based on how
        many levels to go up from the supplied number of levels.

    Args:
        path_object (path-like): the path-like object to create a
            string name from.
        number_levels (int): the number of levels to go up in the
            path to build the name.

    Returns:
        str: the number levels up path name created from path-like object.
    """

    usable_path = cm.attempt_pathlike_extraction(path_object)
    name_order = []
    for level in range(number_levels + 1):
        name_order.append(usable_path.name)
        usable_path = usable_path.parent
    name_order.reverse()
    name_string = "/".join(name_order)
    return name_string


def create_filename_list(path_list):
    """Given an iterable of path-like objects, return back a list of
        filename strings that are unique from eachother in that they
        have been leveled.

    Args:
        path_list (path-like iterable): the path-like iterable to build
            the list of unique string filenames from.

    Returns:
        list: the list of unique string filenames.
    """

    cm.check_argument_iterable(path_list)
    matched_levels = create_matched_level_data(path_list)
    filename_list = []
    for index in range(len(path_list)):
        current_filename = create_filename_level(
            path_list[index], matched_levels[index]
        )
        filename_list.append(current_filename)
    return filename_list


def create_filename_stats(path_list, stat_list):
    """Provided an iterable of pathlib.Path objects and an iterable of
        desired statistics, build a list of filenames, and each stat that
        belongs to the Path() object that was supplied in the stat list.

    Args:
        path_list (iterabl(pathlib.Path)): the pathlist to build the multi-
            dimensional filename and statistics list from.
        stat_list (iterable): the iterable of statistic codes to include
            about each filename found in path_list.

    Returns:
        list: the multidimensional list that includes the filenames, and
            each statistic that was supplied in stat_list.
    """

    cm.check_iterable_types(path_list, pathlib.Path)
    cm.check_argument_iterable(stat_list)
    named_filenames = create_filename_list(path_list)
    filename_stats = [named_filenames]
    for stat in stat_list:
        current_stat_list = handle_list_stat_file(path_list, stat)
        filename_stats.append(current_stat_list)
    return filename_stats


def create_headers_from_codes(code_list):
    """Provided at statistic coded iterable, create a list that includes
        header titles that corresponds to each code in the iterable.

    Args:
        code_list (iterable): the list of codes to match and build the
            resulting header name list from.

    Returns:
        list: the list of header names gathered from each code in the
            supplied iterable of codes.
    """

    cm.check_argument_iterable(code_list)
    header_list = []
    for code in code_list:
        match code:
            case "fn":
                header_name = "Filenames"
            case "ct":
                header_name = "Creation Date"
            case "mt":
                header_name = "Modified Date"
            case "sz":
                header_name = "Size"
            case _:
                header_name = "Unknown"
        header_list.append(header_name)
    return header_list


def create_index_count_dictionary(object_list):
    """Given an iterable, create a dictionary of indexes with zero
        assigned to each as a base count.

    Args:
        object_list (iterable): the iterable with a length to build
            the indexed dictionary from.

    Returns:
        dict: the indexed dictionary filled with number of entries equal
            to the size of the supplied iterable all assigned with zeroes.
    """

    cm.check_argument_iterable(object_list)
    matched_data = {}
    for index in range(len(object_list)):
        matched_data[index] = 0
    return matched_data


def create_indexed_dictionary_list(object_list):
    """Given an iterable, create a list of dictionary objects that contain
        the original object and its index within the list.

    Args:
        object_list (iterable): the iterable to build the list with.

    Returns:
        list: a list of dictionary objects that contain the original object
            and its index in the original iterable.
    """

    cm.check_argument_iterable(object_list)
    object_index_list = []
    for index in range(len(object_list)):
        object_index_list.append({"object": object_list[index], "index": index})
    return object_index_list


def create_matched_level_data(path_list):
    """Given a list of pathlib.Path objects, create a dictionary that
        determines how many levels up one must go before the path
        name becomes unique.

    Args:
        path_list (iterable): the pathlib.Path object iterable to
            build the level dictionary from.

    Returns:
        dict: the level dictionary dictating how many levels up
            paths become unique from eachother.
    """

    cm.check_argument_iterable(path_list)
    cm.check_iterable_types(path_list, pathlib.Path)

    matched_data = create_index_count_dictionary(path_list)
    matched_helper = create_indexed_dictionary_list(path_list)
    while len(matched_helper) > 0:
        removal_indeces = []
        current_names = [ihl["object"].name for ihl in matched_helper]
        current_counts = gather_dictionary_counts(current_names)
        for index in range(len(matched_helper)):
            # if there is an empty name (top level directory) or there is no other match found
            if not current_names[index] or current_counts[current_names[index]] <= 1:
                removal_indeces.append(index)
                continue
            matched_data[matched_helper[index]["index"]] += 1

        matched_helper = remove_indeces_from_list(matched_helper, removal_indeces)
        matched_helper = [
            {"object": previous["object"].parent, "index": previous["index"]}
            for previous in matched_helper
        ]
    return matched_data


def create_directory_table(input_directory, stat_list=[]):
    """Provided a directory, create a table that shows each filename that
        exists in the directory along with any statistics about each file
        found supplied in the stat_list argument.

    Args:
        input_directory (str, pathlib.Path): file-like object to analayze
            sub-files from and build the file table with.

    Raises:
        ValueError: if the supplied input directory is an empty string.

    Returns:
        str: the file table information string analyzed from input directory.
    """

    if isinstance(input_directory, str):
        if not input_directory:  # empty 'directory' supplied
            raise ValueError(f"Supplied directory does not exist: '{input_directory}'")

    usable_directory = cm.attempt_pathlike_extraction(input_directory)
    directory_information = generate_directory_information(usable_directory, stat_list)
    information_table = build_table_string(directory_information)
    return information_table


def gather_dictionary_counts(object_list):
    """Given an iterable of objects, create a dictionary that will
        count each stringified conversion within the supplied iterable.

    Args:
        object_list (iterable): the iterable to build the count from.

    Returns:
        dict: the dictionary of counts of stringified elements in
            the supplied iterable.
    """

    cm.check_argument_iterable(object_list)
    object_counts = {}
    for object_instance in object_list:
        stringed_object = str(object_instance)
        if stringed_object not in object_counts:
            object_counts[stringed_object] = 1
            continue
        object_counts[stringed_object] += 1
    return object_counts


def generate_directory_information(input_directory, stat_list=[]):
    """Given a template directory, gather datetime and size data about
        its underlying files and package this information into a tuple
        returned back to the caller.

    Args:
        input_directory (str, pathlib.Path): the path-like object
            to analyze its underlying files from.
        stat_list (iterable): the list of statistics to gather about
            the underlying files from.

    Returns:
        tuple: the zipped information that includes three objects:
            zipped_info: each file instance's datetimes and size data
                packaged in one tuple representing each file.
            header_info: the header list that coincides with the data
                packaged in the zipped_info object.
            length_info: the maximum string length of each header column
                in the zipped_info object for formatting purposes.
    """

    header_info = create_headers_from_codes(["fn", *stat_list])
    walked_filenames = get_file_path_list(input_directory)
    filename_stats = create_filename_stats(walked_filenames, stat_list)
    base_header_length = length_information_conversion(header_info)
    header_length = [item + TABLE_SPACING for item in base_header_length]
    body_length = calculate_maximum_length(filename_stats)
    length_info = take_larger_comparison(header_length, body_length)
    zipped_info = zip(*filename_stats)
    return (header_info, zipped_info, length_info)


def get_file_path_list(input_directory):
    """Given an input directory, return a list of only files that exist
        in the directory as pathlib.Path objects.

    Args:
        input_directory (str, pathlib.Path): the path-like object to
            anlyze for files in.

    Raises:
        ValueError: if the input directory does not exist in the
            filesystem.

    Returns:
        list: the list of pathlib.Path objects that represent files
            under the input directory.
    """

    usable_directory = cm.attempt_pathlike_extraction(input_directory)
    if not usable_directory.exists():
        raise ValueError(f"Supplied directory does not exist: '{input_directory}'")

    # if the caller supplied a file then utilize its parent directory
    if usable_directory.is_file():
        usable_directory = usable_directory.parent

    file_list = []
    # filter out anything that pathlib says isn't a file
    for result in list(usable_directory.rglob("*")):
        if result.is_file():
            file_list.append(result)
    return file_list


def handle_list_stat_file(file_list, stat):
    """Given a list of file-like paths, perform the stat calculation
        using the single file handler function and return the list.

    Args:
        file_list (list): the list of file-like paths to perfrom stat
            calculations on using the single handler function.
        stat (str): the stat code the caller supplies coinciding with a
            os.stat() variable to calculate with.

    Raises:
        ValueError: if the file list object is not a list.

    Returns:
        list: the list of string representations of each stat object
            performed on each file path.
    """

    cm.check_argument_iterable(file_list)
    file_statted_list = []
    for file_object in file_list:
        file_statted_list.append(handle_single_stat_file(file_object, stat))
    return file_statted_list


def handle_single_stat_file(file_object, stat):
    """Given a file-like object and a statistic code stat, return the correct
        string representation presented by that statistic on the file.

    Args:
        file_object (str, pathlib.Path): the file-like object to perform
            the stat calculation on.
        stat (str): the stat code the caller supplies coinciding with a
            os.stat() variable to calculate with.

    Returns:
        str: the string representation of whichever statistic stat the
            caller uses in nice, human-readable form.
    """

    usable_path = cm.attempt_pathlike_extraction(file_object)
    if not usable_path.is_file():
        return ""
    try:  # attempt to grab the ISO-formatted string from a stat of file_object.
        match stat:
            case "mt":  # return the ISO-formatted modified time
                modified_seconds = usable_path.stat().st_mtime
                return convert_seconds_iso(modified_seconds)
            case "ct":  # return the ISO-formatted creation time
                creation_seconds = usable_path.stat().st_birthtime
                return convert_seconds_iso(creation_seconds)
            case "at":  # return the ISO-formatted access time
                access_seconds = usable_path.stat().st_atime
                return convert_seconds_iso(access_seconds)
            case "sz":  # return the KB size of the file
                byte_size = usable_path.stat().st_size
                return f"{byte_size / 1000} KB"
            case _:  # caller supplied an invalid stat so return empty
                return ""
    except:  # try statement couldn't grab a valid date so return empty
        return ""


def length_information_conversion(information_list):
    """Given an iterable of items, return a list that represents the
        length of each item in the iterable.

    Args:
        information_list (iterable(any)): the iterable to extract
            the lengths of each element from.

    Returns:
        list: the list containing the lengths of each element in
            the supplied iterable.
    """

    cm.check_argument_iterable(information_list)
    length_information = []
    for item in information_list:
        try:
            item_length = len(item)
            length_information.append(item_length)
        except:
            length_information.append(-1)
    return length_information


def remove_indeces_from_list(object_list, indeces_list):
    """Remove the index entries supplied in the index list from the
        supplied object list. If a supplied index does not exist in
        the object list, then it simply will not add it to the result
        list, bypassing any "bad" indeces that are supplied.

    Args:
        object_list (list): the list to remove entries from.
        indeces_list (list, int): the list or single integer index to
            remove from in the supplied object list.

    Returns:
        list: the new list with the specified indeces removed.
    """

    cm.check_argument_iterable(object_list)
    if isinstance(indeces_list, int):
        indeces_list = [indeces_list]

    # caller doesn't wish to remove any indeces so return base list
    if len(indeces_list) == 0:
        return object_list

    reduced_list = []
    for index in range(len(object_list)):
        if index not in indeces_list:
            reduced_list.append(object_list[index])
    return reduced_list


def take_larger_comparison(initial, compare):
    """Provided two iterables of integers, return a list that
        contains the larger item compared between both iterables
        for each item.

    Args:
        initial (iterable(int)): the first compare iterable.
        compare (iterable(int)): the second compare iterable.

    Raises:
        ValueError: if the lists have different lengths.

    Returns:
        list: the larger comparisons between both iterables.
    """

    cm.check_iterable_types(initial, int)
    cm.check_iterable_types(compare, int)

    if len(initial) != len(compare):
        raise ValueError(f"Supplied iterables are different sizes!")

    captured_values = []
    for initial_value, compare_value in zip(initial, compare):
        if initial_value >= compare_value:
            captured_values.append(initial_value)
            continue
        captured_values.append(compare_value)
    return captured_values
