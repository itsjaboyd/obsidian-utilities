"""General template module that includes functions related 
    to template directories and template files within an 
    obsidian vault location. 

    Author: Jason Boyd
    Date: January 20, 2025
    Modified: January 21, 2025
"""

import pathlib
import datetime

TABLE_SPACING = 5


def create_directory_table(input_directory):
    """Handler function for building the table string from directory information.

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

    usable_directory = input_directory
    if not isinstance(input_directory, pathlib.Path):
        usable_directory = pathlib.Path(input_directory)

    directory_information = generate_directory_information(usable_directory)
    information_table = build_table_string(directory_information)
    return information_table


def generate_directory_information(input_directory):
    """Given a template directory, gather datetime and size data about
        its underlying files and package this information into a tuple
        returned back to the caller.

    Args:
        input_directory (str, pathlib.Path): the path-like object
            to analyze its underlying files from

    Returns:
        tuple: the zipped information that includes three objects:
            zipped_info: each file instance's datetimes and size data
                packaged in one tuple representing each file.
            header_info: the header list that coincides with the data
                packaged in the zipped_info object.
            length_info: the maximum string length of each header column
                in the zipped_info object for formatting purposes.
    """

    header_info = ["Filenames", "Creation Date", "Modified Date", "Size"]
    walked_filenames = get_file_path_list(input_directory)
    named_filenames = [filename.name for filename in walked_filenames]
    filename_stats = [named_filenames]
    for stat_item in ["ct", "mt", "sz"]:
        filename_stats.append(handle_list_stat_file(walked_filenames, stat_item))
    zipped_info = zip(*filename_stats)
    length_info = []
    for stat_list in filename_stats:
        length_list = [len(element) for element in stat_list]
        length_info.append(max(length_list) + TABLE_SPACING)
    return (zipped_info, header_info, length_info)


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

    if not isinstance(information, tuple):
        raise ValueError(f"Supplied information is not a tuple: {information}")

    if len(information) != 3:
        raise ValueError(f"Supplied information has incorrect length: {information}")

    zipped_info, header_info, length_info = information
    # create the header of the table string that contains column names
    header_string, main_string = "", ""
    for item_index in range(len(header_info)):
        header_string += format(
            header_info[item_index],
            f"<{length_info[item_index]}",
        )
    header_string += f"\n{"-" * sum(length_info)}\n"
    # create the body of the table containing data in zipped_info
    for packaged_data in zipped_info:
        for data_index in range(len(packaged_data)):
            main_string += format(
                packaged_data[data_index],
                f"<{length_info[data_index]}",
            )
        main_string += "\n"

    return header_string + main_string


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

    usable_directory = input_directory
    if not isinstance(input_directory, pathlib.Path):
        usable_directory = pathlib.Path(input_directory)

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

    usable_path = file_object
    if not isinstance(file_object, pathlib.Path):
        usable_path = pathlib.Path(file_object)
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

    if not isinstance(file_list, list):
        raise ValueError(
            f"Cannot extract '{stat}' dates from non-list object: {file_list}"
        )
    file_iso_list = []
    for file_object in file_list:
        file_iso_list.append(handle_single_stat_file(file_object, stat))
    return file_iso_list


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
