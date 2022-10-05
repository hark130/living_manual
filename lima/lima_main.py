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
from lima.lima_args import ARG_DICT_KEY_FILE, ARG_DICT_KEY_WORDS, parse_lima_args
from lima.lima_search import get_dirty_words, search_file


def execute() -> None:
    try:
        sys.exit(main())
    except Exception as err:
        print(f'ERROR: {str(err)}')
        sys.exit(2)  # Failure
    # sys.exit(main())


def main() -> int:
    # LOCAL VARIABLES
    exit_code = 0     # 0 on success, 1 for bad input, 2 on exception, 3 if dirty words found
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
        exit_code = search_file(arg_dict[ARG_DICT_KEY_FILE], dirty_words)

    # DONE
    return exit_code


if __name__ == '__main__':
    execute()
