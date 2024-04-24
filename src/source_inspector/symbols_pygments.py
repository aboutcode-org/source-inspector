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
from commoncode.cliutils import SCAN_GROUP
from commoncode.cliutils import PluggableCommandLineOption
from plugincode.scan import ScanPlugin
from plugincode.scan import scan_impl
from pygments.lexers import get_lexer_for_filename
from pygments.token import Comment
from pygments.token import Literal
from pygments.token import Name
from pygments.token import Punctuation
from pygments.util import ClassNotFound
from textcode import analysis
from typecode.contenttype import Type

from source_inspector.pygments_lexing import get_tokens

"""
Extract strings and symbols from source code files with pygments.
"""
LOG = logging.getLogger(__name__)


@scan_impl
class PygmentsSymbolsAndStringScannerPlugin(ScanPlugin):
    """
    Scan a source file for symbols and strings using Pygments.
    """

    resource_attributes = dict(
        pygments_symbols=attr.ib(default=attr.Factory(list), repr=False),
    )

    options = [
        PluggableCommandLineOption(
            ("--pygments-symbol",),
            is_flag=True,
            default=False,
            help="Collect source symbols and strings using pygments.",
            help_group=SCAN_GROUP,
            sort_order=100,
        ),
    ]

    def is_enabled(self, pygments_symbol, **kwargs):
        return pygments_symbol

    def get_scanner(self, **kwargs):
        return get_pygments_symbols


def get_pygments_symbols(location, **kwargs):
    """
    Return a mapping of symbols and strings for a source file at ``location``.
    """
    return dict(pygments_symbols=list(get_tokens(location=location)))


def get_tokens(location, with_literals=True, with_comments=False):
    """
    Yield a stream of strings tagged as symbols. Include optional literals (aka. strings.) and comments.
    Yield nothing for files that are not parseable.
    """
    if not Type(location).is_source:
        return

    try:
        lexer = get_lexer_for_filename(location)
    except ClassNotFound:
        return

    text = analysis.unicode_text(location)

    symbols = (
        Name.Function,
        Name.Entity,
        Name.Constant,
        Name.Class,
        Name.Namespace,
        Name.Property,
    )

    for pos, ttype, tvalue in lexer.get_tokens_unprocessed(text):
        tvalue = tvalue.strip()
        if not tvalue:
            continue
        if ttype in Punctuation:
            continue

        if with_literals and ttype in (Literal,) and ttype not in (Punctuation):
            yield dict(position=pos, token_type="string", token_value=tvalue)

        elif with_comments and ttype in Comment:  # and ttype != Token.Comment.Preproc:
            yield dict(position=pos, token_type="comment", token_value=tvalue)

        elif ttype in symbols:
            yield dict(position=pos, token_type="symbol", token_value=tvalue)
