"""Creates the FindManifestFiles test class.

    Facilitate unit testing of post_tool.misc.find_manifest_files().

    Typical usage example:

    python -m unittest                                # Runs every test case it can find
    python -m test.unit_test                          # Runs all unit test cases
    python -m test.unit_test.test_lima_search         # Runs only these test cases
    python -m test.unit_test.test_lima_search -k n01  # Runs only this Normal 01
"""
# Standard Imports
from pathlib import Path
from typing import Any
import os
import sys
import unittest
# Third Party Imports
from hobo.disk_operations import create_file
from tediousstart.tediousstart import execute_test_cases
# Local Imports
# pylint: disable=wrong-import-order
from test.unit_test.lima_unit_test import LivingManualUnitTest, REPO_DIR, TEST_INPUT_DIR
sys.path.insert(0, os.path.join(REPO_DIR, 'lima'))  # Put all lima_* imports after this line
# pylint: disable=wrong-import-position
from lima.lima_search import search_file  # noqa: E402


class RedirectStdStreams(object):
    """Temporarily redirect output streams.

    Lifted from: https://stackoverflow.com/a/6796752
    """
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


class SearchFileUnitTest(LivingManualUnitTest):
    """Executes an lima_search.search_file() unit test."""

    # pylint: disable=useless-super-delegation
    def __init__(self, *args, **kwargs) -> None:
        """LivingManualUnitTest ctor."""

        super().__init__(*args, **kwargs)
        # Template input filename
        self._input_filename = 'LIMA-unit_test-lima_search-Normal{}-input.{}'

    def call_callable(self) -> int:
        """Defines how to call the function."""
        # LOCAL VARIABLES
        return_value = None  # Return value from function call
        devnull = None       # Shunt for output
        
        # CALL IT
        if self._silent_test:
            devnull = open(os.devnull, 'w')  # Shunt for output
            with RedirectStdStreams(stdout=devnull, stderr=devnull):
                return_value = search_file(*self._args, **self._kwargs)
        else:
            return_value = search_file(*self._args, **self._kwargs)

        # DONE
        if devnull:
            devnull.close()
        return return_value

    def validate_return_value(self, return_value: Any) -> None:
        """Defines how to validate the return value."""
        self._validate_return_value(return_value=return_value)


class SearchFileNormalUnitTest(SearchFileUnitTest):
    """Organizes all the Normal test cases."""

    def test_n01(self) -> None:
        """Plain text: no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('01', 'txt')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        # print(f'{self._args}')  # DEBUGGING
        # print(f'{self._kwargs}')  # DEBUGGING
        # print(f'{self._defined_test_input}')  # DEBUGGING
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    def test_n02(self) -> None:
        """Plain text: dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('02', 'txt')
        dirty_words = ['Before Guido', 'code is broken', 'fix my code']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    def test_n03(self) -> None:
        """Plain text: no dirty words found; keyword arguments."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('03', 'txt')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(file_path=target, dw_list=dirty_words, encoding=encoding,
                            case_sensitive=case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    def test_n04(self) -> None:
        """ELF File: no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('04', 'elf')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    def test_n05(self) -> None:
        """ELF File: dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('05', 'elf')
        dirty_words = ['Waiting...']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    def test_n06(self) -> None:
        """PE File (UTF-8): no dirty words found.

        As it turns out, PE files have utf-8 strings in the binary but string literals are
        encoded as utf-16.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('06', 'exe')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    def test_n07(self) -> None:
        """PE File (UTF-8): dirty words found.

        As it turns out, PE files have utf-8 strings in the binary but string literals are
        encoded as utf-16."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('07', 'exe')
        dirty_words = ['HelloWorld.exe']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    def test_n08(self) -> None:
        """PE File (UTF-16): no dirty words found.

        As it turns out, PE files have utf-8 strings in the binary but string literals are
        encoded as utf-16.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('08', 'exe')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-16'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    def test_n09(self) -> None:
        """PE File (UTF-16): dirty words found.

        As it turns out, PE files have utf-8 strings in the binary but string literals are
        encoded as utf-16.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('09', 'exe')
        dirty_words = ['Dragon Feet']
        encoding = 'utf-16'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n10(self) -> None:
        """Archive (zip): no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('10', 'zip')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n11(self) -> None:
        """Archive (zip): dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('11', 'zip')
        dirty_words = ['LIMA-unit_test-lima_search-Normal01-input.txt']  # The file inside
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n12(self) -> None:
        """Archive (tar): no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('12', 'tar')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n13(self) -> None:
        """Archive (tar): dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('13', 'tar')
        dirty_words = ['this one is mine']  # Compressed file contents?!
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n14(self) -> None:
        """Archive (gz): no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('14', 'gz')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n15(self) -> None:
        """Archive (gz): dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('15', 'gz')
        dirty_words = ['original.txt']  # Archive member filename
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n16(self) -> None:
        """Archive (tar.gz): no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('16', 'tar.gz')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-16'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n17(self) -> None:
        """Archive (tar.gz): dirty words STILL NOT found.

        It appears as if there's really nothing to find here.  I manually verified by
        inspecting the archive with xxd.  I see nothing to recognize here.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('17', 'tar.gz')
        dirty_words = ['original']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)  # Even the original base filename can't be found!

        # RUN IT
        self.run_this_test()

    @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n16(self) -> None:
        """Archive (7z): no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('16', '7z')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n17(self) -> None:
        """Archive (7z): dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('17', '7z')
        dirty_words = ['Dragon Feet']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()



class SearchFileErrorUnitTest(SearchFileUnitTest):
    """Organizes all the Error test cases."""

    def test_e01(self) -> None:
        """."""
        # self.set_test_input('This is not a list of Path objects')
        # self.expect_exception(TypeError, '')
        # self.run_this_test()

    def test_e02(self) -> None:
        """."""
        # test_input = self.create_datum_group(num_packets=0)
        # test_input.append('This is not a Path object')
        # self.set_test_input(test_input)
        # self.expect_exception(TypeError, '')
        # self.run_this_test()

if __name__ == '__main__':
    execute_test_cases()
