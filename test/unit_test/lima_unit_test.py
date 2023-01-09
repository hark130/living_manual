"""Defines LivingManualUnitTest class.

LivingManualUnitTest is the parent class for all LIVING MANUAL (LIMA) related unit test classes.

    Typical usage example:

    from test.unit_test import LivingManualUnitTest
    from my_module_to_test import my_function_to_test as my_function


    class MyUnitTest(LivingManualUnitTest):

        # Child class must override this method
        def call_callable(self):
            return my_function(*self._args, **self._kwargs)

        # Child class must override this method
        def validate_return_value(self):
            self._validate_return_value(return_value=return_value)

        # This is your test case
        def test_stuff(self):
            self.set_test_input(1, 2)
            self.expect_return(3)
"""
# Standard Imports
import os
import sys
from pathlib import Path
from typing import Any, Final
# Third Party Imports
# Local Imports
from hobo.disk_operations import find_path_to_dir
from tediousstart.tediousunittest import TediousUnitTest


REPO_DIR: Final[str] = find_path_to_dir('living_manual')
sys.path.insert(0, os.path.join(REPO_DIR, 'lima'))
TEST_INPUT_DIR: Final[Path] = Path(REPO_DIR) / 'test' / 'unit_test' / 'test_input'


class LivingManualUnitTest(TediousUnitTest):
    """Parent class for all LIVING MANUAL (LIMA) related unit tests.

    Inherit from this class, define necessary functionality for the function you're testing and
    be sure to override the following methods in your child class:
        call_callable()
        validate_return_value()
    """

    # pylint: disable=useless-super-delegation
    def __init__(self, *args, **kwargs) -> None:
        """LivingManualUnitTest ctor."""

        super().__init__(*args, **kwargs)

        self._test_input_dir = TEST_INPUT_DIR  # Default input directory for test files
        self._silent_test = True               # Silence printed output from function call

    def call_callable(self) -> None:
        """Defines how the class will invoke the function call.

        Child class must override this method.  See TediousUnitTest.call_callable() for details.
        """
        # Example Usage:
        # return the_function_you_are_testing(*self._args, **self._kwargs)
        raise NotImplementedError(
            self._test_error.format('The child class must override the call_callable method with '
                                    'the Config Tool function to test.'))

    def validate_return_value(self, return_value: Any) -> None:
        """Defines how the class will validate the return value of the tested call.

        Child class must override this method.
        See TediousUnitTest.validate_return_value() for details.
        """
        # Example Usage:
        # self._validate_return_value(return_value=return_value)
        raise NotImplementedError(
            self._test_error.format('The child class must override the validate_return_value '
                                    'method with the appropriate validation logic'))

    def run_this_test(self, silent: bool = True) -> None:
        """Wrapper around self.run_test()."""
        self._validate_type(silent, 'silent', bool)
        self._silent_test = silent
        self.run_test()
