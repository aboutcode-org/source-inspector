# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/source-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import importlib
import logging

import attr
from commoncode.cliutils import SCAN_GROUP
from commoncode.cliutils import PluggableCommandLineOption
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl
from tree_sitter import Language
from tree_sitter import Parser
from typecode.contenttype import Type

# Tracing flags
TRACE = False
TRACE_LIGHT = False


def logger_debug(*args):
    pass


if TRACE or TRACE_LIGHT:
    import logging
    import sys

    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    def logger_debug(*args):
        return logger.debug(" ".join(isinstance(a, str) and a or repr(a) for a in args))


"""
Extract symbols and strings information from source code files with tree-sitter.
See https://tree-sitter.github.io/
"""


@scan_impl
class TreeSitterSymbolAndStringScannerPlugin(ScanPlugin):
    """
    Scan a source file for symbols and strings using tree-sitter.
    """

    resource_attributes = dict(
        source_symbols=attr.ib(default=attr.Factory(list), repr=False),
        source_strings=attr.ib(default=attr.Factory(list), repr=False),
    )

    options = [
        PluggableCommandLineOption(
            ("--treesitter-symbol-and-string",),
            is_flag=True,
            default=False,
            help="Collect source symbols and strings using tree-sitter.",
            help_group=SCAN_GROUP,
            sort_order=100,
            conflicting_options=["source_symbol", "source_string", "pygments_symbol_and_string"],
        ),
    ]

    def is_enabled(self, treesitter_symbol_and_string, **kwargs):
        return treesitter_symbol_and_string

    def get_scanner(self, **kwargs):
        return get_treesitter_symbols


def get_treesitter_symbols(location, **kwargs):
    """
    Return a mapping of symbols and strings for a source file at ``location``.
    """

    symbols, strings = collect_symbols_and_strings(location=location)
    return dict(
        source_symbols=symbols,
        source_strings=strings,
    )


def get_tree_and_language_info(location):
    """
    Given the `location` of a file, determine the correct parser to use, parse
    the file, and return a tuple of (`tree`, `language_info`).

    Return (None, None) if a parser is not found for the file type at `location`
    """
    tree = None
    language_info = None
    if parser_result := get_parser(location):
        parser, language_info = parser_result

        with open(location, "rb") as f:
            source = f.read()

        tree = parser.parse(source)
        return tree, language_info
    return tree, language_info


def collect_symbols_and_strings(location):
    """
    Return lists containing mappings of symbols and strings collected from file at location.
    """
    symbols, strings = [], []

    tree, language_info = get_tree_and_language_info(location)
    if tree and language_info:
        traverse(tree.root_node, symbols, strings, language_info)

    return symbols, strings


def get_parser(location):
    """
    Get the appropriate tree-sitter parser and string identifier for
    file at location.
    """
    file_type = Type(location)
    language = file_type.programming_language

    if not language or language not in TS_LANGUAGE_WHEELS:
        return

    language_info = TS_LANGUAGE_WHEELS[language]
    wheel = language_info["wheel"]

    try:
        grammar = importlib.import_module(wheel)
    except ModuleNotFoundError:
        raise TreeSitterWheelNotInstalled(f"{wheel} package is not installed")

    LANGUAGE = Language(grammar.language())
    parser = Parser(language=LANGUAGE)

    return parser, language_info


def traverse(node, symbols, strings, language_info):
    """Recursively traverse the parse tree node to collect symbols and strings."""
    if node.type in language_info.get("identifiers"):
        if source_symbol := node.text.decode():
            symbols.append(source_symbol)
    elif node.type in language_info.get("string_literals"):
        if source_string := node.text.decode():
            strings.append(source_string)
    for child in node.children:
        traverse(child, symbols, strings, language_info)


TS_LANGUAGE_WHEELS = {
    "Bash": {
        "wheel": "tree_sitter_bash",
        "identifiers": ["identifier"],
        "string_literals": ["string_literal"],
    },
    "C": {
        "wheel": "tree_sitter_c",
        "identifiers": ["identifier"],
        "string_literals": ["string_literal"],
    },
    "C++": {
        "wheel": "tree_sitter_cpp",
        "identifiers": ["identifier"],
        "string_literals": ["string_literal"],
    },
    "C#": {
        "wheel": "tree_sitter_c_sharp",
        "identifiers": ["identifier"],
        "string_literals": ["string_literal"],
    },
    "Cython": {
        "wheel": "tree_sitter_python",
        "identifiers": ["identifier"],
        "string_literals": ["string_literal"],
    },
    "Go": {
        "wheel": "tree_sitter_go",
        "identifiers": ["identifier"],
        "string_literals": ["raw_string_literal"],
    },
    "Java": {
        "wheel": "tree_sitter_java",
        "identifiers": ["identifier"],
        "string_literals": ["string_literal"],
    },
    "JavaScript": {
        "wheel": "tree_sitter_javascript",
        "identifiers": ["identifier"],
        "string_literals": ["string_fragment"],
    },
    "TypeScript": {
        "wheel": "tree_sitter_javascript",
        "identifiers": ["identifier"],
        "string_literals": ["string_fragment"],
    },
    "Objective-C": {
        "wheel": "tree_sitter_objc",
        "identifiers": ["identifier"],
        "string_literals": ["string_content"],
    },
    "Python": {
        "wheel": "tree_sitter_python",
        "identifiers": ["identifier"],
        "string_literals": ["string_literal"],
    },
    "Rust": {
        "wheel": "tree_sitter_rust",
        "identifiers": ["identifier"],
        "string_literals": ["raw_string_literal"],
    },
    "Swift": {
        "wheel": "tree_sitter_swift",
        "identifiers": ["simple_identifier"],
        "string_literals": ["line_str_text"],
    },
}


class TreeSitterWheelNotInstalled(Exception):
    pass
