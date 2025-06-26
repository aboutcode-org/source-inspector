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


class TestTreeSitterSymbolScannerPlugin(FileBasedTesting):
    test_data_dir = os.path.join(os.path.dirname(__file__), "data/symbols_tree_sitter")

    def test_symbols_scanner_basic_cli_cpp(self):
        test_file = self.get_test_loc("cpp/test3.cpp")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("cpp/test3.cpp-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_scanner_long_cli(self):
        test_file = self.get_test_loc("c/if_ath.c")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("c/if_ath.c-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_c_sharp(self):
        test_file = self.get_test_loc("c-sharp/LibraryTypeOptionsDto.cs")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("c-sharp/LibraryTypeOptionsDto.cs-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_objective_c(self):
        test_file = self.get_test_loc("objective-c/BrazeSDKAuthDelegateWrapper.m")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("objective-c/BrazeSDKAuthDelegateWrapper.m-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_javascript(self):
        test_file = self.get_test_loc("javascript/main.js")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("javascript/main.js-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_typescript(self):
        test_file = self.get_test_loc("typescript/main.ts")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("typescript/main.ts-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_swift(self):
        test_file = self.get_test_loc("swift/Client.swift")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("swift/Client.swift-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_go(self):
        test_file = self.get_test_loc("go/client.go")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("go/client.go-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_java(self):
        test_file = self.get_test_loc("java/AssignmentsManager.java")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("java/AssignmentsManager.java-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_python(self):
        test_file = self.get_test_loc("python/cargo.py")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("python/cargo.py-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_rust(self):
        test_file = self.get_test_loc("rust/commit.rs")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("rust/commit.rs-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)

    def test_symbols_strings_cython(self):
        test_file = self.get_test_loc("cython/intbitset.pyx")
        result_file = self.get_temp_file("json")
        args = ["--treesitter-symbol-and-string", test_file, "--json-pp", result_file]
        run_scan_click(args)

        expected_loc = self.get_test_loc("cython/intbitset.pyx-expected.json")
        check_json_scan(expected_loc, result_file, regen=REGEN_TEST_FIXTURES)
