"""LIVING MANUAL (LIMA) entry point.

    Typical usage example:

    from lima.lima_main import execute

    if __name__ == '__main__':
        execute()
"""

# Standard Imports
import sys
# Third Party Imports
# Local Imports
from lima.lima_args import ARG_DICT_KEY_DIR, ARG_DICT_KEY_FILE, ARG_DICT_KEY_WORDS, parse_lima_args
from lima.lima_search import get_dirty_words, search_dir, search_file


# pylint: disable=broad-except
def execute() -> None:
    """Entry point for the LIMA package.

    Raises:
        None.  Prints all Exceptions to stderr and exits with exit code 2.
    """
    try:
        sys.exit(main())
    except Exception as err:
        print(f'ERROR: {str(err)}', file=sys.stderr)
        sys.exit(2)  # Failure


def main() -> int:
    """Entry point for the LIMA module.

    Returns:
        # 0 on success, 1 for bad input, 2 on exception, 3 if dirty words found
    """
    # LOCAL VARIABLES
    exit_code = 0     # 0 on success, 1 for bad input, 2 on exception, 3 if dirty words found
    temp_exit = 0     # Temporary exit code for successive function calls
    arg_dict = {}     # Dictionary of command line arguments
    dirty_words = []  # List of dirty words parsed from the command line

    # PARSE ARGS
    try:
        arg_dict = parse_lima_args()
    except (FileNotFoundError, OSError, TypeError, ValueError) as err:
        print(f'ERROR: {str(err)}')
        exit_code = 1
    else:
        dirty_words = get_dirty_words(arg_dict[ARG_DICT_KEY_WORDS])
        # Use Case 1
        if arg_dict[ARG_DICT_KEY_FILE]:
            temp_code = search_file(arg_dict[ARG_DICT_KEY_FILE], dirty_words)
            if temp_code != 0:
                exit_code = temp_code
        # Use Case 2
        if arg_dict[ARG_DICT_KEY_DIR]:
            temp_code = search_dir(arg_dict[ARG_DICT_KEY_DIR], dirty_words)
            if temp_code != 0:
                exit_code = temp_code

    # DONE
    return exit_code


if __name__ == '__main__':
    execute()
