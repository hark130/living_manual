"""LIVING MANUAL (LIMA) data type validation."""

# Standard Imports
from pathlib import Path
from typing import Any
# Third Party Imports
# Local Imports


def validate_path_file(path_file: Path) -> None:
    """Validate a Path object as a file.

    Args:
        path_file: Path object to validate as a file.

    Raises:
        TypeError: Bad data type.
        FileNotFoundError: path_file is unavailable.
        OSError: path_file is not a file.
    """
    # INPUT VALIDATION
    if path_file is None:
        raise TypeError('Path has not been defined')
    validate_type(path_file, 'path_file', Path)

    # VALIDATE IT
    if not path_file.exists():
        raise FileNotFoundError(f'Unable to locate {path_file.absolute()}')
    if not path_file.is_file():
        raise OSError(f'{path_file.absolute()} is not a file')


def validate_string(validate_this: str, param_name: str, can_be_empty: bool = False) -> None:
    """Standardizes how this module validates string parameters.

    Verifies validate_this is a string. Type validation is handled by validate_type().

    Args:
        validate_this: The parameter to validate.
        param_name: The name of the parameter to be used in exception messages.
        can_be_empty: Optional; If False, this function verifies validate_this is not empty.

    Raises:
        TypeError: validate_this is not a string.
        ValueError: validate_this is empty and can_be_empty is False.
    """
    # LOCAL VARIABLES
    bad_val = '"{}" can not be empty'  # Template for empty strings

    # VALIDATION
    validate_type(validate_this, param_name, str)
    if not validate_this and not can_be_empty:
        raise ValueError(bad_val.format(param_name))


def validate_type(var: Any, var_name: str, var_type: type) -> None:
    """Standardizes how variables are type-validated.

    Verifies var is the same type represented in var_type. This function does not validate input.

    Args:
        var: The variable to type-validate.
        var_name: The name of the variable to be used in exception messages.
        var_type: The expected variable type.

    Raises:
        TypeError: Invalid data type.
    """
    if not isinstance(var, var_type):
        raise TypeError(f'{var_name} expected type {var_type}, instead received type {type(var)}')
