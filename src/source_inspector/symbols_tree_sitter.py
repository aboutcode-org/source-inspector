# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/source-inspector for support or download.
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


def collect_symbols_and_strings(location):
    """
    Return lists containing mappings of symbols and strings collected from file at location.
    """
    symbols, strings = [], []

    if parser_result := get_parser(location):
        parser, string_id = parser_result

        with open(location, "rb") as f:
            source = f.read()

        tree = parser.parse(source)
        traverse(tree.root_node, symbols, strings, string_id)

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

    wheel = TS_LANGUAGE_WHEELS[language]["wheel"]
    string_id = TS_LANGUAGE_WHEELS[language]["string_id"]

    try:
        grammar = importlib.import_module(wheel)
    except ModuleNotFoundError:
        raise TreeSitterWheelNotInstalled(f"{wheel} package is not installed")

    LANGUAGE = Language(grammar.language(), language)
    parser = Parser()
    parser.set_language(LANGUAGE)

    return parser, string_id


def traverse(node, symbols, strings, string_id, depth=0):
    """Recursively traverse the parse tree node to collect symbols and strings."""
    if node.type == "identifier":
        if source_symbol:=node.text.decode():
            symbols.append(source_symbol)
    elif node.type == string_id:
        if source_string:=node.text.decode("unicode_escape").replace('"', ""):
            strings.append(source_string)
    for child in node.children:
        traverse(child, symbols, strings, string_id, depth + 1)


TS_LANGUAGE_WHEELS = {
    "Bash": {"wheel": "tree_sitter_bash", "string_id": "raw_string"},
    "C": {"wheel": "tree_sitter_c", "string_id": "string_literal"},
    "C++": {"wheel": "tree_sitter_cpp", "string_id": "string_literal"},
    "Go": {"wheel": "tree_sitter_go", "string_id": "raw_string_literal"},
    "Java": {"wheel": "tree_sitter_java", "string_id": "string_literal"},
    "JavaScript": {"wheel": "tree_sitter_javascript", "string_id": "string"},
    "Python": {"wheel": "tree_sitter_python", "string_id": "string"},
    "Rust": {"wheel": "tree_sitter_rust", "string_id": "raw_string_literal"},
}


class TreeSitterWheelNotInstalled(Exception):
    pass
