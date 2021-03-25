# Copyright 2021-present, Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

import sys
import glob
import os
import fnmatch

# Declare global variables
EXIT_CODE = 0
ARTICLE_PATH_DEPTH = 4
EXCLUDE_FILES_MD_STRUCT_TEST = [
    '.git/*',
    './src/TESTING/*.[mM][dD]',
    './README.md'
]
EXCLUDE_FILES_ASSETS_STRUCT_TEST = [
    './src/*/*/assets/*',
    './_checks/*',
    './COPYING.txt',
    './LICENSE.txt'
]
TERM_COLORS = {
    'purple': '\033[95m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'bold': '\033[1m',
    'underscore': '\033[4m',
    'reset': '\033[0m'
}


def build_file_list(start_dir: str = "./",
                    file_mask: str = "**/**.*",
                    exclude_list: list = None,
                    recursive: bool = False) -> list:
    """
    Build the file list for the given directory by mask

    :param start_dir: A path to the directory to load files from
    :param file_mask: File mask
    :param exclude_list: An exclude map list
    :param recursive: Load files recursively
    :return: The list of files from the given directory
    :rtype: list
    """
    if exclude_list is None:
        exclude_list = []
    filenames = []
    for filename in glob.iglob(start_dir + file_mask, recursive=recursive):
        filenames.append(filename)

    return exclude_files_from_list(filenames, exclude_list)


def validate_path_depth(file_list: list, depth: int) -> list:
    """
    Walks through the list of files and validate each record directory depth

    :param file_list: The list of file paths to validate
    :param depth: Acceptable directory depth
    :return: The list of files that didn't pass the validation
    :rtype: list
    """

    failed_files = []
    for file in file_list:
        path_elements = os.path.split(file)
        if len(path_elements[0].split(os.sep)) is not depth:
            failed_files.append(file)

    return failed_files


def exclude_files_from_list(file_list: list, exclude_list: list) -> list:
    """
    Apply exclude list to the list of files

    :param file_list: The list of files
    :param exclude_list: The list of exclude masks
    :return: The filtered list of files
    """
    filtered_list = []
    for file in file_list:
        for exclude in exclude_list:
            if fnmatch.fnmatch(file, exclude):
                filtered_list.append(file)

    return [item for item in file_list if item not in set(filtered_list)]


failed_md_depths = validate_path_depth(
    file_list=build_file_list(
        start_dir="./",
        file_mask="**/**.[mM][dD]",
        exclude_list=EXCLUDE_FILES_MD_STRUCT_TEST,
        recursive=True),
    depth=ARTICLE_PATH_DEPTH)

if len(failed_md_depths):
    EXIT_CODE = 1

    print(f"{TERM_COLORS['red']}"
          f"The following MD files did fail the directory structure integrity test:"
          f"{TERM_COLORS['reset']}")
    print(f"\n".join(failed_md_depths))
    print(f"\n{TERM_COLORS['purple']}"
          f"MD files must be placed according to the following directory structure:\n"
          f"{TERM_COLORS['reset']}"
          f"./src/[Category Name Directory]/[Section Name Directory]/\n"
          f"\n")

failed_assets = build_file_list(
    start_dir='./',
    file_mask="**/**.*[!mMdD]",
    exclude_list=EXCLUDE_FILES_ASSETS_STRUCT_TEST,
    recursive=True)

if len(failed_assets):
    EXIT_CODE = 1
    print(f"{TERM_COLORS['red']}"
          f"The following files did fail the assets directory structure integrity test:"
          f"{TERM_COLORS['reset']}")
    print(f"\n".join(failed_assets))
    print(f"\n{TERM_COLORS['purple']}"
          f"Asset files must be placed according to the following directory structure:\n"
          f"{TERM_COLORS['reset']}"
          f"./src/[Category Name Directory]/[Section Name Directory]/assets/\n"
          f"\n")

if not EXIT_CODE:
    print(f"{TERM_COLORS['green']}"
          f"File Structure test has been passed."
          f"{TERM_COLORS['reset']}")
else:
    print(f"{TERM_COLORS['red']}"
          f"File Structure test has been failed."
          f"{TERM_COLORS['reset']}")

sys.exit(EXIT_CODE)
