"""LIVING MANUAL (LIMA) argument parser."""

# Standard Imports
from pathlib import Path
from typing import Dict
import argparse
import sys
# Third Party Imports
# Local Imports
from lima.lima_validation import validate_path_dir, validate_path_file, validate_string


# ARGUMENT DICTIONARY KEYS
ARG_DICT_KEY_FILE = 'file'    # -f, --file
ARG_DICT_KEY_DIR = 'dir'      # -d, --dir
ARG_DICT_KEY_WORDS = 'words'  # -w, --words


class LimaParser(argparse.ArgumentParser):
    """Overrides default ArgumentParser behavior."""

    def error(self, message):
        """Overrides default error behavior.

        Exits with value 1 on argument parsing failures.
        """
        self.print_help(sys.stderr)
        self.exit(1, f'{self.prog}: ERROR: {message}\n')


def parse_lima_args() -> Dict[str, Path]:
    """Process the command line arguments.

    Returns:
        Dictionary containing the command line arguments, the keys being the
        "ARGUMENT DICTIONARY KEYS".

    Raises:
        FileNotFoundError: --database value not found
        OSError: --database value is not a file
        TypeError: Bad datatype
        ValueError: Blank(?) --database value
    """
    # LOCAL VARIABLES
    parsed_args = None  # Parsed args as an argparse.Namespace object
    file_path = None    # Path object of the file (Use Case 1)
    dir_path = None     # Path object of the directory (Use Case 2)
    words_path = None   # Path object to the dirty word list
    arg_dict = {}       # Return value containing arg values
    # Object for parsing command line input into Python objects
    parser = LimaParser(prog='LIVING MANUAL (LIMA)')
    subs = None         # Subparsers
    file_parser = None  # Use Case 1 (file) subparser
    dir_parser = None   # Use Case 2 (directory) subparser

    # ARGUMENTS
    # Add
    subs = parser.add_subparsers(required=True)
    # Use Case 1: File
    file_parser = subs.add_parser('file', help='Search a file for dirty words')
    file_parser.add_argument('-f', '--file', action='store', required=True,
                             help='Target file to search for dirty words')
    file_parser.add_argument('-w', '--words', action='store', required=True,
                             help='Dirty word list')
    # Use Case 2: Directory
    dir_parser = subs.add_parser('dir', help='Search a directory for files with dirty words')
    dir_parser.add_argument('-d', '--dir', action='store', required=True,
                            help='Search for dirty words in all files found in this directory')
    dir_parser.add_argument('-w', '--words', action='store', required=True,
                            help='Dirty word list')

    # Parse
    parsed_args = parser.parse_args()

    # Validate
    # file
    try:
        file_path = _validate_path_arg(path_arg=parsed_args.file, arg_name='--file')
        validate_path_file(file_path)
    except AttributeError:
        pass  # Likely indicates a "partial refactor" BUG
    finally:
        arg_dict[ARG_DICT_KEY_FILE] = file_path
    # dir
    try:
        dir_path = _validate_path_arg(path_arg=parsed_args.dir, arg_name='--dir')
        validate_path_dir(dir_path)
    except AttributeError:
        pass  # Likely indicates a "partial refactor" BUG
    finally:
        arg_dict[ARG_DICT_KEY_DIR] = dir_path
    # word
    try:
        words_path = _validate_path_arg(path_arg=parsed_args.words, arg_name='--words')
        validate_path_file(words_path)
    except AttributeError:
        pass  # Likely indicates a "partial refactor" BUG
    finally:
        arg_dict[ARG_DICT_KEY_WORDS] = words_path

    # DONE
    return arg_dict


def _validate_path_arg(path_arg: str, arg_name: str) -> Path:
    """Validate file arguments and construct Path objects.

    Args:
        path_arg: Absolute or relative filename.
        arg_name: Name of the argument to include in Exception messages.

    Returns:
        Path object for path_arg.

    Raises:
        FileNotFoundError: arg_name value not found
        OSError: arg_name value is not a file
        TypeError: Bad datatype
        ValueError: Blank(?) arg_name value
    """
    validate_string(path_arg, 'path_arg')
    validate_string(arg_name, 'arg_name')
    file_path = Path(path_arg)
    return file_path
