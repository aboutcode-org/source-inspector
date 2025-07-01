Changelog
=========

v0.7.0
------

- Add support for Cython https://github.com/aboutcode-org/source-inspector/pull/37
- Add the function ``source_inspector.symbols_tree_sitter.get_tree_and_language_info``

v0.6.1
------

- Bump tree-sitter to v0.23.2 with python 3.13 support
- Use released py-tree-sitter-swift from https://github.com/aboutcode-org/tree-sitter-swift
- Add tests for source symbol extraction with tree-sitter in all supported languages

See https://github.com/aboutcode-org/source-inspector/pull/36 for more details.

v0.6.0
------

- Bump tree-sitter to v0.23
- Collect swift source symbols and strings using tree-sitter https://github.com/aboutcode-org/source-inspector/pull/31
- Collect Objective C source symbols and strings using tree-sitter https://github.com/aboutcode-org/source-inspector/pull/30
- Collect C# source symbols and strings using tree-sitter https://github.com/aboutcode-org/source-inspector/pull/32
- Fix javascript and add typescript source symbols and strings collection using tree-sitter https://github.com/aboutcode-org/source-inspector/pull/33

v0.5.2
------

- Update link references of ownership from nexB to aboutcode-org


v0.5.1
------

- Update README with Pygments and Tree-Sitter example by @keshav-space in https://github.com/aboutcode-org/source-inspector/issues/22
- Pin tree-sitter dependencies by @keshav-space in https://github.com/aboutcode-org/source-inspector/issues/23

v0.5.0
------

- Add support to collect strings, comments and symbols from source using Pygments
- Add support to collect strings and symbols from source using tree-sitter


v0.3.0
------

Improve xgettext handlings.
 - Handle empty, whitespace and special characters. https://github.com/nexB/source-inspector/issues/11
 - Properly handle the multiple starting lines for a string. https://github.com/nexB/source-inspector/issues/13
 - Run xgettext with UTF-8 encoding. https://github.com/nexB/source-inspector/issues/14

v0.2.0
------

Add source strings collection using xgettext.
Ignore anonymous symbols in symbols_ctags.
Fix typo in package name.
Rename symbols output to source_symbols.


v0.1.0
------

Initial release with basic source symbols collection using Universal Ctags.

Also available as ScanCode Toolkit plugin.
