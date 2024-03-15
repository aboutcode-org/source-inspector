# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/source-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import logging

import attr
from commoncode import command
from commoncode.cliutils import SCAN_GROUP
from commoncode.cliutils import PluggableCommandLineOption
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl

"""
Extract strinsg from source code files with xgettext.
"""
LOG = logging.getLogger(__name__)


@scan_impl
class XgettextStringScannerPlugin(ScanPlugin):
    """
    Scan a source file for strings using GNU xgettext.
    """

    resource_attributes = dict(
        source_strings=attr.ib(default=attr.Factory(list), repr=False),
    )

    options = [
        PluggableCommandLineOption(
            ("--source-string",),
            is_flag=True,
            default=False,
            help="Collect source strings using xgettext.",
            help_group=SCAN_GROUP,
            sort_order=100,
        ),
    ]

    def is_enabled(self, source_string, **kwargs):
        return source_string

    def get_scanner(self, **kwargs):
        return get_source_strings


def get_source_strings(location, **kwargs):
    """
    Return a mapping of strings for a source file at ``location``.
    """
    return dict(source_strings=list(collect_strings(location=location, strip=True)))


def collect_strings(location, strip=False):
    """
    Yield mappings of strings collected from file at location.
    Strip strings if ``strip`` is True.
    """
    if not is_xgettext_installed():
        return

    rc, result, err = command.execute(
        cmd_loc="xgettext",
        args=["--omit-header", "--no-wrap", "--extract-all", "--output=-", location],
        to_files=False,
    )

    if rc != 0:
        raise Exception(open(err).read())

    yield from parse_po_text(po_text=result, strip=strip)


def parse_po_text(po_text, strip=False):
    """
    Yield mappings of strings collected from the ``po_text`` string.
    Strip strings if ``strip`` is True.

    The po text lines looks like this:
    - Blocks sperated by 2 lines.
    - The first lines starting with #: are comments with the line numbers.
    - The lines starting with #, are flags, not interesting
    - We care about the lines in the middle starting with the first msgid
    - The last line starting with msgstr is empty at first.

    See https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html

    #: symbols_ctags.py:21
    #: symbols_ctags.py:23
    msgid ""
    "Extract symbols information from source code files with ctags.\n"
    #, c-format
    msgstr ""

    #: symbols_ctags.py:39
    msgid "--source-symbol"
    msgstr ""
    """

    for chunk in po_text.split("\n\n"):
        lines = chunk.splitlines(False)
        line_numbers = []
        strings = []
        for line in lines:
            if line.startswith("#: "):
                _, _, start_line = line.rpartition(":")
                line_numbers.append(int(start_line.strip()))

            elif line.startswith(
                (
                    "msgstr",
                    "#,",
                    "# ",
                    "#|",
                )
            ):
                continue

            elif line.startswith("msgid "):
                _msgid, _, line = line.partition(" ")
                strings.append(line)

            elif line.startswith('"'):
                strings.append(line)

        strings = [l.strip('"').replace("\\n", "\n") for l in strings]
        string = "".join(strings)
        if strip:
            string = string.strip()

        yield dict(line_numbers=line_numbers, string=string)


_IS_XGETTEXT_INSTALLED = None


def is_xgettext_installed():
    """
    Check if GNU xgettext is installed.
    """
    global _IS_XGETTEXT_INSTALLED

    if _IS_XGETTEXT_INSTALLED is None:
        _IS_XGETTEXT_INSTALLED = False
        try:
            rc, result, err = command.execute(
                cmd_loc="xgettext",
                args=["--version"],
                to_files=False,
            )

            if rc != 0:
                raise Exception(err)

            if result.startswith("xgettext (GNU gettext-tools)"):
                _IS_XGETTEXT_INSTALLED = True

        except FileNotFoundError:
            pass

    return _IS_XGETTEXT_INSTALLED
