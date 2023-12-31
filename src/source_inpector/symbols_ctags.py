# -*- coding: utf-8 -*-
#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-plugins for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import logging
import os

import attr

from commoncode import command
from commoncode import fileutils
from commoncode.cliutils import PluggableCommandLineOption
from commoncode.cliutils import SCAN_GROUP
from commoncode.functional import flatten

from plugincode.scan import scan_impl
from plugincode.scan import ScanPlugin


"""
Extract symbols information from source code files with ctags.
"""
LOG = logging.getLogger(__name__)

bin_dir = os.path.join(os.path.dirname(__file__), "bin")



@scan_impl
class CtagsSymbolScannerPlugin(ScanPlugin):
    
    """
    Scan a source file for symbols using Universal Ctags.
    """
    resource_attributes = dict(
        symbols=attr.ib(default=attr.Factory(list), repr=False),

    )

    options = [
        PluggableCommandLineOption(('--source-symbol',),
            is_flag=True, default=False,
            help='Collect symbols using Universal ctags.',
            help_group=SCAN_GROUP,
            sort_order=100),
    ]

    def is_enabled(self, source_symbol, **kwargs):
        return source_symbol

    def get_scanner(self, **kwargs):
        return get_symbols


def get_symbols(location, **kwargs):
    """
    Return a mapping of symbols for a source file at ``location``.
    """
    scanner = SymbolScanner(sourcefile=location)
    return dict(symbols=scanner.symbols())
    
    

class SymbolScanner:
    """
    Scan source files for symbols.
    """

    def __init__(self, sourcefile):
        self.sourcefile = sourcefile

        # use the path
        self.cmd_loc = None

        # nb: those attributes names are api and expected when fingerprinting
        # a list of sources files names (not path)
        self.files = []
        self.files.append(fileutils.file_name(sourcefile))
        # a list of function names
        self.local_functions = []
        self.global_functions = []

        self._collect_and_parse_tags()

    def symbols(self):
        glocal = flatten([self.local_functions, self.global_functions])
        return sorted(glocal)

    def _collect_and_parse_tags(self):
        ctags_args = ["--fields=K", "--c-kinds=fp", "-f", "-", self.sourcefile]
        ctags_temp_dir = fileutils.get_temp_dir()
        envt = {"TMPDIR": ctags_temp_dir}

        try:
            
            rc, stdo, err = command.execute(
                cmd_loc=self.cmd_loc,
                args=ctags_args,
                env=envt,
                to_files=True,
            )

            if rc != 0:
                raise Exception(open(err).read())

            with open(stdo) as lines:
                for line in lines:
                    if "cannot open temporary file" in line:
                        raise Exception("ctags: cannot open temporary file " ": Permission denied")

                    if line.startswith("!"):
                        continue

                    line = line.strip()
                    if not line:
                        continue

                    splitted = line.split("\t")

                    if line.endswith("function\tfile:") or line.endswith("prototype\tfile:"):
                        self.local_functions.append(splitted[0])

                    elif line.endswith("function") or line.endswith("prototype"):
                        self.global_functions.append(splitted[0])
        finally:
            fileutils.delete(ctags_temp_dir)
