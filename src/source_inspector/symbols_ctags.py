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
import logging

import attr
from commoncode import command
from commoncode.cliutils import SCAN_GROUP
from commoncode.cliutils import PluggableCommandLineOption
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl
from typecode.contenttype import Type

"""
Extract symbols information from source code files with ctags.
See https://docs.ctags.io/en/stable/man/ctags-json-output.5.html
"""
LOG = logging.getLogger(__name__)


@scan_impl
class CtagsSymbolScannerPlugin(ScanPlugin):
    """
    Scan a source file for symbols using Universal Ctags.
    """

    resource_attributes = dict(
        source_symbols=attr.ib(default=attr.Factory(list), repr=False),
    )

    options = [
        PluggableCommandLineOption(
            ("--source-symbol",),
            is_flag=True,
            default=False,
            help="Collect source symbols using Universal ctags.",
            help_group=SCAN_GROUP,
            sort_order=100,
            conflicting_options=["treesitter_symbol_and_string", "pygments_symbol_and_string"],
        ),
    ]

    def is_enabled(self, source_symbol, **kwargs):
        return source_symbol

    def get_scanner(self, **kwargs):
        return get_symbols


def get_symbols(location, **kwargs):
    """
    Return a mapping of symbols for a source file at ``location``.
    """
    return dict(source_symbols=list(collect_symbols(location=location)))


def collect_symbols(location):
    """
    Yield mappings of symbols collected from file at location.
    """
    if not is_ctags_installed():
        return

    if not Type(location).is_source:
        return

    rc, result, err = command.execute(
        cmd_loc="ctags",
        args=["--output-format=json", "-f", "-", location],
        to_files=False,
    )

    if rc != 0:
        raise Exception(err)

    # set of ctags field names we support
    supported_fields = {
        "name",
        "pattern",
        "file",
        "kind",
        "scope",
        "scopeKind",
        "typeref",
    }

    for line in result.splitlines(False):
        line = line.strip()
        if not line:
            continue
        tag = json.loads(line)

        # Ignore the anonymous tags.
        if (name := tag.get("name")) and is_anon_string(name):
            continue

        if (scope := tag.get("scope")) and "__anon" in scope:
            tag["scope"] = "anonymous"

        # only keep some fields
        # see ctags --output-format=json --list-fields for a full list
        yield {k: v for k, v in tag.items() if k in supported_fields}


def is_anon_string(symbol):
    """
    Check if a symbol is an anonymous string.
    An anonymous symbol starts with `__anon` followed by a hexadecimal string.

    Examples:
    >>> is_anon_string("__anon722f7bb60308")
    True
    >>> is_anon_string("__anon_user_id")
    False

    """
    if symbol.startswith("__anon"):
        hex_part = symbol[6:]
        for c in hex_part:
            if c not in "0123456789abcdef":
                return False
        return True
    return False


_IS_CTAGS_INSTALLED = None


def is_ctags_installed():
    """
    Check if Universal Ctags is installed with json support.
    """
    global _IS_CTAGS_INSTALLED

    if _IS_CTAGS_INSTALLED is None:
        _IS_CTAGS_INSTALLED = False
        try:
            rc, result, err = command.execute(
                cmd_loc="ctags",
                args=["--version"],
                to_files=False,
            )

            if rc != 0:
                raise Exception(err)

            if result.startswith("Universal Ctags") and "+json" in result:
                _IS_CTAGS_INSTALLED = True

        except FileNotFoundError:
            pass

    return _IS_CTAGS_INSTALLED
