"""LIVING MANUAL (LIMA) argument parser."""

# Standard Imports
from pathlib import Path
from typing import Dict
import argparse
import sys
# Third Party Imports
# Local Imports
from lima.lima_validation import validate_path_file, validate_string


# ARGUMENT DICTIONARY KEYS
ARG_DICT_KEY_FILE = 'file'    # -f, --file
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
    file_path = None    # Path object of the target file
    words = None        # Path object to the dirty word list
    arg_dict = {}       # Return value containing arg values
    # Object for parsing command line input into Python objects
    parser = LimaParser(prog='LIVING MANUAL (LIMA)')

    # ARGUMENTS
    # Add
    parser.add_argument('-f', '--file', action='store', required=True,
                        help='Target file to search for dirty words')
    parser.add_argument('-w', '--words', action='store', required=True,
                        help='Dirty word list')
    # Parse
    parsed_args = parser.parse_args()

    # Validate
    # file
    try:
        file_path = _validate_path_arg(file_arg=parsed_args.file, arg_name='--file')
    except AttributeError:
        pass  # Likely indicates a "partial refactor" BUG
    finally:
        arg_dict[ARG_DICT_KEY_FILE] = file_path
    # word
    try:
        words = _validate_path_arg(file_arg=parsed_args.words, arg_name='--words')
    except AttributeError:
        pass  # Likely indicates a "partial refactor" BUG
    finally:
        arg_dict[ARG_DICT_KEY_WORDS] = words

    # DONE
    return arg_dict


def _validate_path_arg(file_arg: str, arg_name: str) -> Path:
    """Validate file arguments and construct Path objects.

    Args:
        file_arg: Absolute or relative filename.
        arg_name: Name of the argument to include in Exception messages.

    Returns:
        Path object for file_arg.

    Raises:
        FileNotFoundError: arg_name value not found
        OSError: arg_name value is not a file
        TypeError: Bad datatype
        ValueError: Blank(?) arg_name value
    """
    validate_string(file_arg, 'file_arg')
    validate_string(arg_name, 'arg_name')
    file_path = Path(file_arg)
    validate_path_file(file_path)
    return file_path
