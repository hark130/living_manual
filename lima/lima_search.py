"""LIVING MANUAL (LIMA) dirty word search functions."""

# Standard Imports
from pathlib import Path
from typing import List
import sys
# Third Party Imports
# Local Imports
from lima.lima_validation import validate_path_file, validate_string, validate_type


def get_dirty_words(dw_path: Path) -> List[str]:
    """Parse dirty word file into a list.

    Args:
        dw_path: Path object to the --words file.

    Returns:
        A list of strings to use as dirty words during the search.

    Raises:
        TypeError: Bad data type.
        FileNotFoundError: dw_path is unavailable.
        OSError: dw_path is not a file.
    """
    # LOCAL VARIABLES
    dw_list = []  # List of dirty words to return

    # INPUT VALIDATION
    validate_path_file(dw_path)

    # GET IT
    dw_list = [entry for entry in dw_path.read_text().split('\n') if entry]

    # DONE
    return dw_list


def search_file(file_path: Path, dw_list: List[str], case_sensitive: bool = True) -> int:
    """Searches file_path for dw_list entries.

    Prints findings to stderr.

    Args:
        file_path: Path object to a file to search.
        dw_list: A list of non-empty strings to search file_path for.
        case_sensitive: Optional; Considers case when checking file_path contents for dirty words.

    Returns:
        0 if no dirty words were found, 3 if dirty words were found.

    Raises:
        FileNotFoundError: file_path is unavailable.
        OSError: file_path is not a file.
        TypeError: Bad data type.
        ValueError: Bad value (e.g., empty string).
    """
    # LOCAL VARIABLES
    found = 0             # 0 if no dirty words were found, 3 if dirty words were found
    file_contents = ''    # Contents of file_path
    local_list = dw_list  # Local copy of dw_list contents

    # INPUT VALIDATION
    validate_path_file(file_path)
    validate_type(dw_list, 'dw_list', list)
    if not dw_list:
        raise ValueError('Dirty word list may not be empty')
    for dw_entry in dw_list:
        validate_string(dw_entry, 'dw_list entry')
    validate_type(case_sensitive, 'case_sensitive', bool)

    # READ IT
    file_contents = file_path.read_text().split('\n')

    # PREPARE IT
    if not case_sensitive:
        file_contents = [file_entry.lower() for file_entry in file_contents]
        local_list = [dw_entry.lower() for dw_entry in dw_list]

    # SEARCH IT
    for line_num in range(0, len(file_contents)):
        for dw_entry in local_list:
            if dw_entry in file_contents[line_num]:
                found = 3
                print(f'{file_path.absolute()} : line {line_num + 1} : "{dw_entry}" '
                      f'found in "{file_contents[line_num]}"', file=sys.stderr)

    # DONE
    return found
