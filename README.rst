source-inspector
================================

source-inspector is a set of utilities to inspect and analyze source
code and collect interesting data using various tools such as code symbols, strings and comments.
This is also a ScanCode-toolkit plugin.

Homepage: https://github.com/nexB/source-inspector
License: Apache-2.0


Requirements
~~~~~~~~~~~~~

This utility is designed to work on Linux and POSIX OS with these utilities:

- xgettext that comes with GNU gettext.
- universal ctags, version 5.9 or higher, built with JSON support.

On Debian systems run this::

    sudo apt-get install universal-ctags gettext

On MacOS systems run this::

    brew install universal-ctags gettext

To get started:
~~~~~~~~~~~~~~~~

1. Clone this repo

2. Run::

    ./configure --dev
    source venv/bin/activate

3. Run tests with::

    pytest -vvs

4. Run a basic scan to collect symbols and display as YAML on screen::

    scancode --source-symbol tests/data/symbols_ctags/test3.cpp --yaml -

5. Run a basic scan to collect strings and display as YAML on screen::

    scancode --source-string tests/data/symbols_ctags/test3.cpp --yaml -

6. Run a basic scan to collect symbols, strings and comments using `Pygments <https://pygments.org/>`_, and display them as YAML on the screen::

    scancode --pygments-symbol-and-string tests/data/symbols_ctags/test3.cpp --yaml -

7. Run a basic scan to collect symbols and strings using `Tree-Sitter <https://tree-sitter.github.io/tree-sitter/>`_, and display them as YAML on the screen::

    scancode --treesitter-symbol-and-string tests/data/symbols_ctags/test3.cpp --yaml -