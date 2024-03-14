source-inspector
================================

source-inspector is a set of utilities to inspect and analyze source
code and collect interesting data using various tools such as code symbols.
This is also a ScanCode-toolkit plugin.

This is a work in progress.


You will need to have universal ctags installed, version 5.9 or higher, built with JSON support.

On Debian systems run this::

    sudo apt-get install universal-ctags


To get started:


1. Clone this repo
2. Run::

    ./configure --dev
    source venv/bin/activate

3. Run tests with::

    pytest -vvs

4. Run a basic scan to collect symbols and display as YAML on screen::

    scancode --yaml - --source-symbol tests/data/symbols_ctags/test3.cpp

Homepage: https://github.com/nexB/source-inspector
License: Apache-2.0
