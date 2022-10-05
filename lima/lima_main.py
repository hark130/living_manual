# Standard Imports
import sys
# Third Party Imports
# Local Imports


def execute() -> None:
    try:
        sys.exit(main())
    except Exception as err:
        print(f'ERROR: {str(err)}')
        sys.exit(2)  # Failure


def main() -> int:
    # LOCAL VARIABLES
    exit_code = 0  # 0 on success, 1 for bad input, 2 on exception


    # DONE
    return exit_code


if __name__ == '__main__':
    execute()
