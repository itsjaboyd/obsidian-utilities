"""
    This module houses the Analyzer class and related functionality needed for 
    analyzing directories for formmating, separators, and other information.

    Author: Jason Boyd
    Date: February 6, 2025
    Modified: February 6, 2025
"""

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
        """Find all common characters that share the same position in string_list.

        Args:
            string_list (iterable): the iterable to find the common characters from.

        Returns:
            list: the unique list of sorted characters that all share the same position.
        """

        commonality = set()
        for comparer, *elements in zip(*strings):
            if all(comparer == matcher for matcher in elements):
                commonality.add(comparer)
        return sorted(list(commonality))

    @staticmethod
    def gather_directories(directory):
        pass

    @staticmethod
    def gather_directory_objects(directory):
        pass

    @staticmethod
    def gather_files(directory):
        pass
