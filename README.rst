source-inspector
================================

source-inspector is a ScanCode toolkit plugin to collect symbols from source files using various
tools.

This is a work in progress.

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
License: Apache-2.0 AND GPL-2.0

The GPL-2.0 applies only to the bundled Ctags binary.