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


def generate_template_information(template_directory):
    header_info = ["Filenames", "Creation Date", "Modified Date", "Size"]
    walked_filenames = get_file_path_list(template_directory)
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
    zipped_info = information[0]
    header_info = information[1]
    length_info = information[2]
    zipped_info, header_info, length_info = information

    header_string = ""
    for item_index in range(len(header_info)):
        header_string += format(
            header_info[item_index],
            f"<{length_info[item_index]}",
        )
    header_string += f"\n{"-" * sum(length_info)}\n"

    main_string = ""
    for packaged_data in zipped_info:
        for data_index in range(len(packaged_data)):
            main_string += format(
                packaged_data[data_index],
                f"<{length_info[data_index]}",
            )
        main_string += "\n"

    return header_string + main_string


def get_file_path_list(input_directory):
    usable_directory = input_directory
    if not isinstance(input_directory, pathlib.Path):
        usable_directory = pathlib.Path(input_directory)

    if not usable_directory.exists():
        raise ValueError(f"Supplied directory does not exist: {input_directory}")

    if usable_directory.is_file():
        usable_directory = usable_directory.parent

    file_list = []
    for result in list(usable_directory.rglob("*")):
        if result.is_file():
            file_list.append(result)

    return file_list


def handle_single_stat_file(file_object, stat):
    if not isinstance(file_object, pathlib.Path):
        return ""
    if not file_object.is_file():
        return ""
    try:  # attempt to grab the ISO-formatted string from a stat of file_object.
        match stat:
            case "mt":  # return the ISO-formatted modified time
                modified_seconds = file_object.stat().st_mtime
                return convert_seconds_iso(modified_seconds)
            case "ct":  # return the ISO-formatted creation time
                creation_seconds = file_object.stat().st_birthtime
                return convert_seconds_iso(creation_seconds)
            case "at":  # return the ISO-formatted access time
                access_seconds = file_object.stat().st_atime
                return convert_seconds_iso(access_seconds)
            case "sz":  # return the KB size of the file
                byte_size = file_object.stat().st_size
                return f"{byte_size / 1000} KB"
            case _:  # caller supplied an invalid stat so return empty
                return ""
    except:  # try statement couldn't grab a valid date so return empty
        return ""


def handle_list_stat_file(file_list, stat):
    if not isinstance(file_list, list):
        raise ValueError(
            f"Cannot extract '{stat}' dates from non-list object: {file_list}"
        )
    file_iso_list = []
    for file_object in file_list:
        file_iso_list.append(handle_single_stat_file(file_object, stat))
    return file_iso_list


def convert_seconds_iso(seconds):
    datetime_instance = datetime.datetime.fromtimestamp(seconds)
    return datetime_instance.isoformat(sep=" ", timespec="seconds")
