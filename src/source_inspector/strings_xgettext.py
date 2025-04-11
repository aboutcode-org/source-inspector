# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/aboutcode-org/source-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import logging
import string

import attr
from commoncode import command
from commoncode.cliutils import SCAN_GROUP
from commoncode.cliutils import PluggableCommandLineOption
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl
from typecode.contenttype import Type

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
            conflicting_options=["treesitter_symbol_and_string", "pygments_symbol_and_string"],
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
    return dict(source_strings=list(collect_strings(location=location, clean=True)))


def collect_strings(location, clean=True):
    """
    Yield mappings of strings collected from file at location.
    Clean strings if ``clean`` is True.
    """
    if not is_xgettext_installed():
        return

    if not Type(location).is_source:
        return

    rc, result, err = command.execute(
        cmd_loc="xgettext",
        args=[
            # this is a trick to force getting UTF back
            # see https://github.com/aboutcode-org/source-inspector/issues/14#issuecomment-2001893496
            '--copyright-holder="ø"',
            "--no-wrap",
            "--extract-all",
            "--from-code=UTF-8",
            "--output=-",
            location,
        ],
        to_files=False,
    )

    if rc != 0:
        raise Exception(err)

    yield from parse_po_text(po_text=result, drop_header=True, clean=clean)


def parse_po_text(po_text, drop_header=False, clean=True):
    """
    Yield mappings of strings collected from the ``po_text`` string.
    Clean strings if ``clean`` is True.
    Drop the "header" first block if ``drop_header`` is True

    The po text lines looks like this:
    - Blocks separated by 2 lines.
    - Optional first header block
    - The first lines starting with #: are comments with the line numbers.
    - The lines starting with #, are flags, not interesting
    - We care about the lines in the middle starting with the first msgid
    - The last line starting with msgstr is empty at first.

    See https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html

    #: symbols_ctags.py:21
    #: symbols_ctags.py:23
    msgid ""
    "Extract symbols information from source code files with ctags."
    #, c-format
    msgstr ""

    #: symbols_ctags.py:39
    msgid "--source-symbol"
    msgstr ""
    """

    blocks = po_text.split("\n\n")
    if drop_header:
        # drop the first block which is the header
        blocks = blocks[1:]

    for block in blocks:
        lines = block.splitlines(False)
        line_numbers = []
        strings = []
        for line in lines:
            if line.startswith("#: "):
                # we can have either of these two forms:
                # #: lineedit.c:1571 lineedit.c:1587 lineedit.c:163
                # #: lineedit.c:1571
                _, _, line = line.partition("#: ")
                filename, _, _ = line.partition(":")
                numbers = line.replace(filename + ":", "")
                numbers = [int(l) for ln in numbers.split() if (l := ln.strip())]
                line_numbers.extend(numbers)

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

        strings = [l.strip('"') for l in strings]
        string = "".join(strings)
        if clean:
            string = clean_string(string)
        if string:
            yield dict(line_numbers=line_numbers, string=string)


def clean_string(s):
    """
    Return a cleaned and normalized string or None.
    """
    s = s.strip('"')
    s = s.replace("\\n", "\n")
    s = s.strip()
    non_printables = {
        "\\a": "\a",
        "\\b": "\b",
        "\\v": "\v",
        "\\f": "\f",
        "\\x01": "\x01",
        "\\x02": "\x02",
        "\\x03": "\x03",
        "\\x04": "\x04",
        "\\x05": "\x05",
        "\\x06": "\x06",
        "\\x0e": "\x0e",
        "\\x0f": "\x0f",
        "\\x10": "\x10",
        "\\x11": "\x11",
        "\\x12": "\x12",
        "\\x13": "\x13",
        "\\x14": "\x14",
        "\\x15": "\x15",
        "\\x16": "\x16",
        "\\x17": "\x17",
        "\\x18": "\x18",
        "\\x19": "\x19",
        "\\x1a": "\x1a",
        "\\x1b": "\x1b",
        "\\x1c": "\x1c",
        "\\x1d": "\x1d",
        "\\x1e": "\x1e",
        "\\x1f": "\x1f",
        "\\x7f": "\x7f",
    }

    for plain, encoded in non_printables.items():
        s = s.replace(plain, "")
        s = s.replace(encoded, "")
    return s


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
