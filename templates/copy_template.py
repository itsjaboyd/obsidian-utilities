"""
    Copy template file(s) to target directories. Users may utilize Obsidian 
    plugins to automatically populate fields within the note body, so make 
    sure to open notes within the Obsidian application to perform any updates 
    to a note as necessary. This module provides the functionality to copy 
    template files from a template directory location to a target location, 
    with the ability to copy in multiples.

    Author: Jason Boyd
    Date: January 3, 2025
    Modified: January 3, 2025
"""

import pathlib
import datetime
import shutil

