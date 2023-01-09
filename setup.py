"""Setup script to distribute LIVING MANUAL (LIMA).

This script was written as an easy way to release LIMA as a wheel.
Project-specific macros are defined at the top of the file.  'LIMA_VERSION' should be updated
for each new release.  'LIMA_REQUIRES' will need to be updated if LIMA ever imports additional
third-party libraries.

    Typical usage example:

    python3 setup.py bdist_wheel --dist-dir='dist'
"""

# Standard Imports
import setuptools
# Third Party Imports
# Local Imports
from hobo.disk_operations import destroy_dir, find_path_to_dir, read_file
from hobo.misc import print_exception

LIMA_NAME = 'lima'
LIMA_VERSION = '1.1.0'
LIMA_AUTHOR = 'Dev Crew Team Happy Aku'
LIMA_EMAIL = 'nunya@biz.ns'  # https://iiwiki.us/wiki/.ns
LIMA_DESCRIPTION = 'Dirty word search utility.'
LIMA_URL = 'https://github.com/hark130/living_manual'
LIMA_PYTHON = '>=3.7'  # See: setuptools.setup(python_requires)
LIMA_REQUIRES = []  # See: setuptools.setup(install_requires)


def main() -> None:
    """Builds the LIMA package.

    Gathers and prepares information to include in the package.  Then builds the package.

    Args:
        None

    Raises:
        OSError: Problems with files.
    """
    try:
        # LOCAL VARIABLES
        repo_dir = _find_repo_dir('living_manual')       # Abs path to the top-level repo directory
        long_description = _build_description(repo_dir)  # README.md + CHANGELOG.md

        # SETUP
        setuptools.setup(
            name=LIMA_NAME,
            version=LIMA_VERSION,
            author=LIMA_AUTHOR,
            author_email=LIMA_EMAIL,
            maintainer=LIMA_AUTHOR,
            maintainer_email=LIMA_EMAIL,
            description=LIMA_DESCRIPTION,
            long_description=long_description,
            long_description_content_type='text/markdown',
            url=LIMA_URL,
            # Hard-coded the package name in case we define supporting packages (e.g., testing)
            packages=['lima'],
            classifiers=[
                # Taken from: https://pypi.org/pypi?%3Aaction=list_classifiers
                'Programming Language :: Python :: 3',
                'Intended Audience :: Developers',
                'Natural Language :: English',
                'Operating System :: OS Independent',
                'Topic :: Software Development :: Testing',
            ],
            python_requires=LIMA_PYTHON,
            install_requires=LIMA_REQUIRES,
            entry_points={'console_scripts': ['lima=lima.lima_main:main']}
        )

        # CLEAN UP
        destroy_dir(f'{LIMA_NAME}.egg-info')
        destroy_dir('build')

    # pylint: disable=broad-except
    except Exception as err:
        print_exception(err)
    # pylint: enable=broad-except


#############################
# INTERNAL HELPER FUNCTIONS #
#############################


def _build_description(repo_dir: str) -> str:
    """Builds the LIMA description.

    Builds a long description for LIMA by concatenating the README.md and CHANGELOG.md.  Input
    validation handled by internal helper functions.

    Args:
        repo_dir: The absolute path to the LIMA directory.

    Returns:
        A string containing the concatenated contents of README.md and CHANGELOG.md.

    Raises:
        FileNotFoundError: repo_dir, README.md, or CHANGELOG.md is not found.
        OSError: README.md or CHANGELOG.md is not a file or repo_dir is not a directory.
        TypeError: Invalid data type.
        ValueError: Empty repo_dir string.
    """
    # LOCAL VARIABLES
    long_description = ''  # Long description for LIMA

    # BUILD IT
    long_description = _get_readme(repo_dir)

    # DONE
    return long_description


def _find_repo_dir(repo_dir_name: str) -> str:
    """Finds the LIMA directory.

    Finds the root-level LIMA directory starting at the current working directory.  It calls
    hobo.disk_operations.find_path_to_dir() under the hood.

    Args:
        repo_dir_name: The name of the top-level LIMA repo directory.

    Returns:
        A string containing the absolute path to repo_dir_name.

    Raises:
        OSError: repo_dir_name isn't found.
    """
    return find_path_to_dir(dir_to_find=repo_dir_name)


def _get_readme(repo_dir: str) -> str:
    """Reads the LIMA README.

    Reads the LIMA README.md and returns it as a string.  Input validation handled by
    hobo.read_file().

    Args:
        repo_dir: The absolute path to the LIMA directory.

    Returns:
        A string containing the contents of README.md.

    Raises:
        FileNotFoundError: repo_dir or README.md is not found.
        OSError: repo_dir is not a directory or README.md is not a file.
        TypeError: Invalid data type.
        ValueError: Empty string.
    """
    return read_file(repo_dir, 'README.md')  # Contents of the README.md


if __name__ == '__main__':
    main()
