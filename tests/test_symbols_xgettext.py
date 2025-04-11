# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/source_inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import os
import platform

import pytest
from commoncode.testcase import FileBasedTesting
from scancode.cli_test_utils import check_json_scan
from scancode.cli_test_utils import run_scan_click

from source_inspector.strings_xgettext import is_xgettext_installed
from source_inspector.strings_xgettext import parse_po_text

# Used for tests to regenerate fixtures with regen=True
REGEN_TEST_FIXTURES = os.getenv("SCANCODE_REGEN_TEST_FIXTURES", False)


class TestXgettextSymbolScannerPlugin(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), "data/strings_xgettext")

    def test_is_xgettext_installed(self):
        assert is_xgettext_installed()

    def test_parse_po_text(self):
        test = """#: symbols_ctags.py:21
msgid ""
"\n"
"Extract symbols information from source code files with ctags.\n"
msgstr ""

#: symbols_ctags.py:29
msgid ""
"\n"
"    Scan a source file for symbols using Universal Ctags.\n"
"    "
msgstr ""

#: symbols_ctags.py:39
msgid "--source-symbol"
msgstr ""

#: symbols_ctags.py:42
msgid "Collect source symbols using Universal ctags."
msgstr ""
"""
        results = list(parse_po_text(test, clean=False))
        expected = [
            {
                "line_numbers": [
                    21,
                ],
                "string": "Extract symbols information from source code files with ctags.",
            },
            {
                "line_numbers": [
                    29,
                ],
                "string": "    Scan a source file for symbols using Universal Ctags.    ",
            },
            {
                "line_numbers": [
                    39,
                ],
                "string": "--source-symbol",
            },
            {
                "line_numbers": [
                    42,
                ],
                "string": "Collect source symbols using Universal ctags.",
            },
        ]

        assert results == expected

        results = list(parse_po_text(test, clean=True))
        expected = [
            {
                "line_numbers": [
                    21,
                ],
                "string": "Extract symbols information from source code files with ctags.",
            },
            {
                "line_numbers": [
                    29,
                ],
                "string": "Scan a source file for symbols using Universal Ctags.",
            },
            {
                "line_numbers": [
                    39,
                ],
                "string": "--source-symbol",
            },
            {
                "line_numbers": [
                    42,
                ],
                "string": "Collect source symbols using Universal ctags.",
            },
        ]

        assert results == expected

    def test_parse_po_text_multilines(self):
        test = """#: tests/data/strings_xgettext/test3.cpp:104
#: tests/data/strings_xgettext/test3.cpp:107
msgid "%"
msgstr ""

#: tests/data/strings_xgettext/test3.cpp:104
#: tests/data/strings_xgettext/test3.cpp:107
#: tests/data/strings_xgettext/test3.cpp:140
#: tests/data/strings_xgettext/test3.cpp:143
#: tests/data/strings_xgettext/test3.cpp:162
#: tests/data/strings_xgettext/test3.cpp:165
#, c-format
msgid "x"
msgstr ""

#: tests/data/strings_xgettext/test3.cpp:123
msgid "/lib/libc-2.2.4.so"
msgstr ""

#: tests/data/strings_xgettext/test3.cpp:140
#: tests/data/strings_xgettext/test3.cpp:162
msgid "/usr/bin/addr2line --functions -C -e %s 0x%"
msgstr ""

#: tests/data/strings_xgettext/test3.cpp:143
#: tests/data/strings_xgettext/test3.cpp:165
msgid "/usr/bin/addr2line --functions -C -e /proc/%d/exe 0x%"
msgstr ""
"""
        results = list(parse_po_text(test))
        expected = [
            {
                "line_numbers": [
                    104,
                    107,
                ],
                "string": "%",
            },
            {
                "line_numbers": [
                    104,
                    107,
                    140,
                    143,
                    162,
                    165,
                ],
                "string": "x",
            },
            {
                "line_numbers": [
                    123,
                ],
                "string": "/lib/libc-2.2.4.so",
            },
            {
                "line_numbers": [
                    140,
                    162,
                ],
                "string": "/usr/bin/addr2line --functions -C -e %s 0x%",
            },
            {
                "line_numbers": [
                    143,
                    165,
                ],
                "string": "/usr/bin/addr2line --functions -C -e /proc/%d/exe 0x%",
            },
        ]

        assert results == expected

    def test_parse_po_text_multilines_on_one_line(self):
        test = """#: tests/data/strings_xgettext/test3.cpp:104
#: tests/data/strings_xgettext/test3.cpp:107
msgid "%"
msgstr ""

#: tests/data/strings_xgettext/test3.cpp:104 tests/data/strings_xgettext/test3.cpp:107 tests/data/strings_xgettext/test3.cpp:140
msgid "x"
msgstr ""
"""
        results = list(parse_po_text(test))
        expected = [
            {
                "line_numbers": [
                    104,
                    107,
                ],
                "string": "%",
            },
            {
                "line_numbers": [
                    104,
                    107,
                    140,
                ],
                "string": "x",
            },
        ]

        assert results == expected

    def test_strings_scanner_basic_cli_cpp(self):
        test_file = self.get_test_loc("test3.cpp")
        result_file = self.get_temp_file("json")
        args = ["--source-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("test3.cpp-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_strings_scanner_multilines_utf8(self):
        test_file = self.get_test_loc("lineedit.c")
        result_file = self.get_temp_file("json")
        args = ["--source-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("lineedit.c-expected.json", must_exist=False)
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    @pytest.mark.skipif(
        platform.system() == "Linux"
        and platform.release().startswith("5.1")
        and "Ubuntu" in platform.uname().version,
        reason="Test not supported on Ubuntu 20",
    )
    def test_strings_scanner_unicode(self):
        test_file = self.get_test_loc("fdisk.c")
        result_file = self.get_temp_file("json")
        args = ["--source-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("fdisk.c-expected.json", must_exist=False)
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)
