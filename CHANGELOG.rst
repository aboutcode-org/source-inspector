Changelog
=========

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
