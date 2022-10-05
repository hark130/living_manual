"""LIVING MANUAL (LIMA) dirty word search functions."""

# Standard Imports
from pathlib import Path
from typing import List
import sys
# Third Party Imports
# Local Imports
from lima.lima_validation import (validate_path_dir, validate_path_file,
                                  validate_string, validate_type)


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


def search_dir(dir_path: Path, dw_list: List[str], case_sensitive: bool = True,
               recursive: bool = False) -> int:
    """Searches dir_path for files that contain dw_list entries.

    Prints findings to stderr.

    Args:
        dir_path: Path object to a directory to search.
        dw_list: A list of non-empty strings to search file_path for.
        case_sensitive: Optional; Considers case when checking file_path contents for dirty words.
        recursive: Optional; If True, recursive search all the child directories found in dir_path.

    Returns:
        0 if no dirty words were found, 3 if dirty words were found.

    Raises:
        FileNotFoundError: dir_path is unavailable.
        OSError: dir_path is not a directory.
        TypeError: Bad data type.
        ValueError: Bad value (e.g., empty string).
    """
    # LOCAL VARIABLES
    target_files = []    # List of files found within dir_path to search for dirty words
    child_dir_list = []  # List of children directories to dir_path
    temp_found = 0       # Temporary return value storage
    found = 0            # 0 if no dirty words were found, 3 if dirty words were found

    # INPUT VALIDATION
    validate_path_dir(dir_path)
    validate_type(recursive, 'recursive', bool)

    # SEARCH IT
    # dir_path
    target_files = [t_file for t_file in dir_path.iterdir() if t_file.is_file()]
    for target_file in target_files:
        temp_found = search_file(file_path=target_file, dw_list=dw_list,
                                 case_sensitive=case_sensitive)
        if temp_found != 0:
            found = temp_found
    # Recurse?
    if recursive:
        child_dir_list = [child_dir for child_dir in dir_path.iterdir() if child_dir.is_dir()]
        for child_dir in child_dir_list:
            temp_found = search_dir(dir_path=child_dir, dw_list=dw_list,
                                    case_sensitive=case_sensitive, recursive=recursive)
            if temp_found != 0:
                found = temp_found

    # DONE
    return found


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
    local_list = dw_list  # Local copy of dw_list contents
    try_harder = False    # Tracks UnicodeDecodeError Exceptions from _search_file_text()

    # INPUT VALIDATION
    validate_path_file(file_path)
    validate_type(dw_list, 'dw_list', list)
    if not dw_list:
        raise ValueError('Dirty word list may not be empty')
    for dw_entry in dw_list:
        validate_string(dw_entry, 'dw_list entry')
    validate_type(case_sensitive, 'case_sensitive', bool)

    # READ IT
    try:
        found = _search_file_text(file_path=file_path, dw_list=local_list,
                                  case_sensitive=case_sensitive)
    except (RuntimeError, UnicodeDecodeError):
        try_harder = True
    if try_harder:
        found = _search_file_bytes(file_path=file_path, dw_list=local_list)

    # DONE
    return found


def _search_file_bytes(file_path: Path, dw_list: List[str]) -> int:
    """Read a file's bytes and search for dw_list entries.

    Prints findings to stderr.  Does not validate input.

    Returns:
        0 if no dirty words were found, 3 if dirty words were found.
    """
    # LOCAL VARIABLES
    found = 0           # 0 if no dirty words were found, 3 if dirty words were found
    file_contents = ''  # Byte content of file_path
    local_list = []     # Local copy of dw_list contents converted to byte objects

    # PREPARE IT
    local_list = [bytes(dw_entry, encoding='UTF-8') for dw_entry in dw_list]

    # READ IT
    file_contents = file_path.read_bytes()

    # SEARCH IT
    for dw_entry in local_list:
        if dw_entry in file_contents:
            found = 3
            print(f'{file_path.absolute()} : {str(dw_entry)[1:]} found in binary file',
                  file=sys.stderr)

    # DONE
    return found


def _search_file_text(file_path: Path, dw_list: List[str], case_sensitive: bool) -> int:
    """Search a UTF-8 encoded file for dw_list entries.

    Prints findings to stderr.  Call _search_file_bytes() if this function raises a
    UnicodeDecodeError.  Does not validate input.

    Returns:
        0 if no dirty words were found, 3 if dirty words were found.

    Raises:
        RuntimeError: UnicodeDecodeError exception wrapped up nice and neat.
        UnicodeDecodeError: Likely, 'utf-8' codec can't decode byte.
    """
    # LOCAL VARIABLES
    found = 0             # 0 if no dirty words were found, 3 if dirty words were found
    file_contents = ''    # Contents of file_path
    local_list = dw_list  # Local copy of dw_list contents

    # READ IT
    try:
        file_contents = file_path.read_text().split('\n')
    except UnicodeDecodeError as err:
        raise RuntimeError(f'UnicodeDecodeError: {str(err)} in {file_path.absolute()}') from err
    else:
        # PREPARE IT
        if not case_sensitive:
            local_list = [dw_entry.lower() for dw_entry in dw_list]
            file_contents = [file_entry.lower() for file_entry in file_contents]
        # SEARCH IT
        for line_num, file_entry in enumerate(file_contents):
            for dw_entry in local_list:
                if dw_entry in file_entry:
                    found = 3
                    print(f'{file_path.absolute()} : line {line_num + 1} : "{dw_entry}" '
                          f'found in "{file_entry}"', file=sys.stderr)

    # DONE
    return found
