# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/source-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import json
import os

import saneyaml
from commoncode.testcase import FileBasedTesting
from scancode.cli_test_utils import check_json_scan
from scancode.cli_test_utils import run_scan_click

from source_inspector.symbols_pygments import get_tokens

# Used for tests to regenerate fixtures with regen=True
REGEN_TEST_FIXTURES = os.getenv("SCANCODE_REGEN_TEST_FIXTURES", False)


def check_json(expected, results, regen=REGEN_TEST_FIXTURES):
    """
    Assert if the results data is the same as the expected JSON file.
    """
    if regen:
        with open(expected, "w") as ex:
            json.dump(results, ex, indent=2, separators=(",", ": "))
    with open(expected) as ex:
        expected = json.load(ex)

    if results != expected:
        expected = saneyaml.dump(expected)
        results = saneyaml.dump(results)
        assert results == expected


class TestPygmentsSymbolScannerPlugin(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), "data/symbols_pygments")

    def test_get_tokens_basic(self):
        test_file = self.get_test_loc("test3.cpp")
        expected_loc = self.get_test_loc("test3.cpp-expected-tokens.json", must_exist=False)
        results = list(get_tokens(test_file, with_comments=True))
        check_json(expected_loc, results, regen=REGEN_TEST_FIXTURES)

    def test_get_tokens_long(self):
        test_file = self.get_test_loc("if_ath.c")
        expected_loc = self.get_test_loc("if_ath.c-expected-tokens.json", must_exist=False)
        results = list(get_tokens(test_file, with_comments=True))
        check_json(expected_loc, results, regen=REGEN_TEST_FIXTURES)

    def test_symbols_scanner_basic_cli_cpp(self):
        test_file = self.get_test_loc("test3.cpp")
        result_file = self.get_temp_file("json")
        args = ["--pygments-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("test3.cpp-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_scanner_long_cli(self):
        test_file = self.get_test_loc("if_ath.c")
        result_file = self.get_temp_file("json")
        args = ["--pygments-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("if_ath.c-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)
