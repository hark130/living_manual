"""LIVING MANUAL (LIMA) argument parser."""

# Standard Imports
from pathlib import Path
from typing import Any, Dict
import argparse
import sys
# Third Party Imports
# Local Imports
from lima.lima_validation import validate_path_dir, validate_path_file, validate_string

DEFAULT_ENCODING = 'utf-8'  # Default encoding
# Supported --encoding values
SUPPORTED_ENCODINGS = [DEFAULT_ENCODING, 'utf-16']

# ARGUMENT DICTIONARY KEYS
ARG_DICT_KEY_FILE = 'file'      # -f, --file
ARG_DICT_KEY_DIR = 'dir'        # -d, --dir
ARG_DICT_KEY_WORDS = 'words'    # -w, --words
ARG_DICT_KEY_RECUR = 'recurse'  # -r, --recursive
ARG_DICT_KEY_ENCODE = 'encode'  # -e, --encoding


class LimaParser(argparse.ArgumentParser):
    """Overrides default ArgumentParser behavior."""

    def error(self, message):
        """Overrides default error behavior.

        Exits with value 1 on argument parsing failures.
        """
        self.print_help(sys.stderr)
        self.exit(1, f'{self.prog}: ERROR: {message}\n')


def parse_lima_args() -> Dict[str, Any]:
    """Process the command line arguments.

    Returns:
        Dictionary containing the command line arguments, the keys being the
        "ARGUMENT DICTIONARY KEYS".

    Raises:
        FileNotFoundError: --database value not found
        NotImplementedError: --encoding value not supported
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
    subs = None         # Subparsers
    file_parser = None  # Use Case 1 (file) subparser
    dir_parser = None   # Use Case 2 (directory) subparser
    # Object for parsing command line input into Python objects
    parser = LimaParser(prog='LIVING MANUAL (LIMA)')

    # ARGUMENTS
    # Add
    subs = parser.add_subparsers(required=True)
    # Use Case 1: File
    file_parser = subs.add_parser('file', help='Search a file for dirty words')
    file_parser.add_argument('-f', '--file', action='store', required=True,
                             help='Target file to search for dirty words')
    file_parser.add_argument('-w', '--words', action='store', required=True,
                             help='Dirty word list')
    file_parser = _add_encoding_arg(file_parser)  # Add --encoding to the sub-parser
    # Use Case 2: Directory
    dir_parser = subs.add_parser('dir', help='Search a directory for files with dirty words')
    dir_parser.add_argument('-d', '--dir', action='store', required=True,
                            help='Search for dirty words in all files found in this directory')
    dir_parser.add_argument('-w', '--words', action='store', required=True,
                            help='Dirty word list')
    dir_parser.add_argument('-r', '--recursive', action='store_true', required=False,
                            help='Search all child directories', default=False)
    dir_parser = _add_encoding_arg(dir_parser)  # Add --encoding to the sub-parser

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
    # recursive
    try:
        arg_dict[ARG_DICT_KEY_RECUR] = parsed_args.recursive
    except AttributeError:
        arg_dict[ARG_DICT_KEY_RECUR] = False  # Likely indicates a "partial refactor" BUG
    # encoding
    try:
        arg_dict[ARG_DICT_KEY_ENCODE] = parsed_args.encoding
    except AttributeError:
        arg_dict[ARG_DICT_KEY_ENCODE] = DEFAULT_ENCODING
    finally:
        if arg_dict[ARG_DICT_KEY_ENCODE] not in SUPPORTED_ENCODINGS:
            raise NotImplementedError(f'Unsupported encoding "{arg_dict[ARG_DICT_KEY_ENCODE]}"')

    # DONE
    return arg_dict


def _add_encoding_arg(lparser: LimaParser) -> LimaParser:
    """SPOT for the encoding argument.

    Does not validate input.

    Args:
        lparser: Parser to add encoding support to.

    Returns:
        Modified lparser.
    """
    lparser.add_argument('-e', '--encoding', action='store', required=False,
                         help='Target encoding to use: ' + ', '.join(SUPPORTED_ENCODINGS)
                              + f' (default: {DEFAULT_ENCODING})',
                         default=DEFAULT_ENCODING)
    return lparser


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
    validate_string(arg_name, 'arg_name')
    validate_string(path_arg, arg_name)
    file_path = Path(path_arg)
    return file_path
