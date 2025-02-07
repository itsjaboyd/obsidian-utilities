"""
    This module houses the Analyzer class and related functionality needed for 
    analyzing directories for formmating, separators, and other information.

    Author: Jason Boyd
    Date: February 6, 2025
    Modified: February 7, 2025
"""

import pathlib
from configuration import configuration as cf
from common import common as cm


class Analyzer:
    """
    The Analyzer class takes an optional directory for initialization that may
    be a fully qualified path, or a name of a directory that exists in configuration
    under the PATHS section. This class should be used to analyze directories for
    information about their file and sub-directory formatting.
    """

    def __init__(self, directory=None):
        config = cf.Configuration()
        self.vault = config.get("PATHS", "vault")
        self.directory = directory
        if directory is None:
            return
        # attempt a configuration extraction if the path does not exist
        directory_path = cm.attempt_pathlike_extraction(directory)
        if not directory_path.exists():
            self.directory = config.get("PATHS", directory)

    def __str__(self):
        return f"Analyzer Instance (vault: {self.vault}, directory: {self.directory})"

    def analyze(self, directory=None, files=True, deep=False):
        pass

    @staticmethod
    def common_position_characters(strings):
        cm.check_iterable_types(strings, str)
        commonality = set()
        for comparer, *elements in zip(*strings):
            if all(comparer == matcher for matcher in elements):
                commonality.add(comparer)
        return sorted(list(commonality))

    @staticmethod
    def common_characters(strings):
        cm.check_iterable_types(strings, str)
        string_sets = [set(element) for element in strings]
        return set.intersection(*string_sets)

    @staticmethod
    def gather_directories_files(directory, deep=False):
        directory_path = cm.attempt_pathlike_extraction(directory)
        directory_objects = Analyzer.gather_directory_objects(directory_path, deep)
        directories, files = [], []
        for element in directory_objects:
            if element.is_dir():
                directories.append(element)
            if element.is_file():
                files.append(element)
        return directories, files

    @staticmethod
    def gather_directory_objects(directory, deep=False):
        directory_path = cm.attempt_pathlike_extraction(directory)
        if not directory_path.is_dir():
            raise ValueError(f"Supplied directory is not a directory: {directory}.")
        # gather all items recursively if deep otherwise iterate the directory
        return directory_path.rglob("*") if deep else directory_path.iterdir()
