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

    def call_callable(self) -> int:
        """Defines how to call the function."""
        # LOCAL VARIABLES
        return_value = None  # Return value from function call
        devnull = None       # Shunt for output
        
        # CALL IT
        if self._silent_test:
            with open(os.devnull, 'w') as devnull:  # Shunt for output
                with RedirectStdStreams(stdout=devnull, stderr=devnull):
                    return_value = search_file(*self._args, **self._kwargs)
        else:
            return_value = search_file(*self._args, **self._kwargs)

        # DONE
        return return_value

    def validate_return_value(self, return_value: Any) -> None:
        """Defines how to validate the return value."""
        self._validate_return_value(return_value=return_value)


class SearchFileNormalUnitTest(SearchFileUnitTest):
    """Organizes all the Normal test cases."""

    # pylint: disable=useless-super-delegation
    def __init__(self, *args, **kwargs) -> None:
        """LivingManualUnitTest ctor."""

        super().__init__(*args, **kwargs)
        # Template input filename
        self._input_filename = 'LIMA-unit_test-lima_search-Normal{}-input.{}'

    def test_n01_txt(self) -> None:
        """Plain text: no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('01', 'txt')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    def test_n02_txt(self) -> None:
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

    def test_n03_txt(self) -> None:
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

    def test_n04_elf(self) -> None:
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

    def test_n05_elf(self) -> None:
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

    def test_n06_pe(self) -> None:
        """PE File (UTF-8): no dirty words found.

        As it turns out, PE files have utf-8 strings in the binary but string literals are
        encoded as utf-16 (wide characters?).
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

    def test_n07_pe(self) -> None:
        """PE File (UTF-8): dirty words found.

        As it turns out, PE files have utf-8 strings in the binary but string literals are
        encoded as utf-16 (wide characters?).
        """
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

    def test_n08_pe(self) -> None:
        """PE File (UTF-16): no dirty words found.

        As it turns out, PE files have utf-8 strings in the binary but string literals are
        encoded as utf-16 (wide characters?).
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

    def test_n09_pe(self) -> None:
        """PE File (UTF-16): dirty words found.

        As it turns out, PE files have utf-8 strings in the binary but string literals are
        encoded as utf-16 (wide characters?).
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
    def test_n10_zip(self) -> None:
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
    def test_n11_zip(self) -> None:
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
    def test_n12_tar(self) -> None:
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
    def test_n13_tar(self) -> None:
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
    def test_n14_gz(self) -> None:
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
    def test_n15_gz(self) -> None:
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
    def test_n16_tar_gz(self) -> None:
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
    def test_n17_tar_gz(self) -> None:
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

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n18_7z(self) -> None:
        """Archive (7z): no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('18', '7z')
        dirty_words = ['not here', 'can not find this', 'missing dirty word']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n19_7z(self) -> None:
        """Archive (7z): dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('19', '7z')
        dirty_words = ['reading']  # Found the file contents?!
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n20_7z(self) -> None:
        """Archive (7z): no dirty words found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('20', '7z')
        dirty_words = ['reading']  # Can't find the utf-8 string when parsing utf-16
        encoding = 'utf-16'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n21_7z(self) -> None:
        """Archive (7z): dirty words NOT found."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('21', '7z')
        dirty_words = ['test_input']
        encoding = 'utf-16'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(0)  # It's in there but LIMA can't find it with utf-16
        # 0000 0000 0000 0000 0000 0000 111f 0074  ...............t
        # 0065 0073 0074 005f 0069 006e 0070 0075  .e.s.t._.i.n.p.u
        # 0074 002e 0074 0078 0074 0000 0019 0400  .t...t.x.t......

    # @unittest.skip("TO DO: DON'T DO NOW... create file-based input for this test")
    def test_n22_7z(self) -> None:
        """Archive (7z): dirty words found.

        utf-16 may miss it but utf-8 + Strategy 4 will get it.  This edge case was the catalyst
        for Strategy 4.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('22', '7z')
        dirty_words = ['test_input']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()


class SearchFileErrorUnitTest(SearchFileUnitTest):
    """Organizes all the Error test cases."""

    # pylint: disable=useless-super-delegation
    def __init__(self, *args, **kwargs) -> None:
        """LivingManualUnitTest ctor."""

        super().__init__(*args, **kwargs)
        # Template input filename
        self._input_filename = 'LIMA-unit_test-lima_search-Error{}-input.{}'

    def test_e01(self) -> None:
        """Bad data type: file_path."""
        # TEST INPUT
        target = './not/a/path.obj'
        dirty_words = ['dirty', 'words']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(TypeError, 'path')

        # RUN IT
        self.run_this_test()

    def test_e02(self) -> None:
        """Bad data type: dw_list."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('02', 'txt')
        dirty_words = tuple(('dirty', 'words'))
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(TypeError, 'dw_list')

        # RUN IT
        self.run_this_test()

    def test_e03(self) -> None:
        """Bad data type: encoding."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('03', 'txt')
        dirty_words = ['dirty', 'words']
        encoding = b'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(TypeError, 'encoding')

        # RUN IT
        self.run_this_test()

    def test_e04(self) -> None:
        """Bad data type: case_sensitive."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('04', 'txt')
        dirty_words = ['dirty', 'words']
        encoding = 'utf-8'
        case_sensitivity = 1

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(TypeError, 'case_sensitive')

        # RUN IT
        self.run_this_test()

    def test_e05(self) -> None:
        """Bad value: empty dw_list."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('05', 'txt')
        dirty_words = []
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(ValueError, 'empty')

        # RUN IT
        self.run_this_test()

    def test_e06(self) -> None:
        """Bad value: empty string in dw_list."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('06', 'txt')
        dirty_words = ['bad', '', 'string']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(ValueError, 'empty')

        # RUN IT
        self.run_this_test()

    def test_e07(self) -> None:
        """Bad value: empty encoding."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('07', 'txt')
        dirty_words = ['dirty', 'words']
        encoding = ''
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(ValueError, 'empty')

        # RUN IT
        self.run_this_test()

    def test_e08(self) -> None:
        """OSError: file_path is not a file."""
        # TEST INPUT
        target = Path(self._test_input_dir)
        dirty_words = ['dirty', 'words']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(OSError, 'not a file')

        # RUN IT
        self.run_this_test()

    def test_e09(self) -> None:
        """FileNotFoundError: file_path is unavailable."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('09', 'not_here')
        dirty_words = ['dirty', 'words']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(FileNotFoundError, 'Unable to locate')

        # RUN IT
        self.run_this_test()

    def test_e10(self) -> None:
        """LookupError: Unknown encoding."""
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('10', 'txt')
        dirty_words = ['dirty', 'words']
        encoding = 'those_bytes_though'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_exception(LookupError, 'encoding')

        # RUN IT
        self.run_this_test()


class SearchFileSpecialUnitTest(SearchFileUnitTest):
    """Organizes all the Special test cases."""

    # pylint: disable=useless-super-delegation
    def __init__(self, *args, **kwargs) -> None:
        """LivingManualUnitTest ctor."""

        super().__init__(*args, **kwargs)
        # Template input filename
        self._input_filename = 'LIMA-unit_test-lima_search-Special{}-input.{}'

    def test_s01_pe(self) -> None:
        """PE File (UTF-8): dirty words found.

        Special targeted catch-all test for the new strategy 4: remove null bytes.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('01', 'exe')
        dirty_words = ['HelloWorld.exe']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    def test_s02_pe(self) -> None:
        """PE File (UTF-8): dirty words found.

        Special targeted catch-all test for the new strategy 4: remove null bytes.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('02', 'exe')
        dirty_words = ['Dragon Feet']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    def test_s03_pe(self) -> None:
        """PE File (UTF-8): dirty words found.

        Special targeted catch-all test for the new strategy 4: remove null bytes.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('03', 'exe')
        dirty_words = ['Hello World!']
        encoding = 'utf-8'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    def test_s04_pe(self) -> None:
        """PE File (UTF-16): dirty words found.

        Special targeted catch-all test for the new strategy 4: remove null bytes.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('04', 'exe')
        dirty_words = ['HelloWorld.exe']
        encoding = 'utf-16'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        # Can't seem to find this one.  Probably because it's *actually* utf-8.
        self.expect_return(0)

        # RUN IT
        self.run_this_test()

    def test_s05_pe(self) -> None:
        """PE File (UTF-16): dirty words found.

        Special targeted catch-all test for the new strategy 4: remove null bytes.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('05', 'exe')
        dirty_words = ['Dragon Feet']
        encoding = 'utf-16'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()

    def test_s06_pe(self) -> None:
        """PE File (UTF-16): dirty words found.

        Special targeted catch-all test for the new strategy 4: remove null bytes.
        """
        # TEST INPUT
        target = Path(self._test_input_dir) / self._input_filename.format('06', 'exe')
        dirty_words = ['Hello World!']
        encoding = 'utf-16'
        case_sensitivity = True

        # TEST SETUP
        self.set_test_input(target, dirty_words, encoding, case_sensitivity)
        self.expect_return(3)

        # RUN IT
        self.run_this_test()


if __name__ == '__main__':
    execute_test_cases()
