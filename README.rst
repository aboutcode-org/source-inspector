source-inspector
================================

source-inspector is a set of utilities to inspect and analyze source
code and collect interesting data using various tools such as code symbols, strings and comments.
This is also a ScanCode-toolkit plugin.

Homepage: https://github.com/aboutcode-org/source-inspector
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



Acknowledgements, Funding, Support and Sponsoring
--------------------------------------------------------

This project is funded, supported and sponsored by:

- Generous support and contributions from users like you!
- the European Commission NGI programme
- the NLnet Foundation
- the Swiss State Secretariat for Education, Research and Innovation (SERI)
- Google, including the Google Summer of Code and the Google Seasons of Doc programmes
- Mercedes-Benz Group
- Microsoft and Microsoft Azure
- AboutCode ASBL
- nexB Inc.



|europa|   |dgconnect|

|ngi|   |nlnet|

|aboutcode|  |nexb|



This project was funded through the NGI0 Core Fund, a fund established by NLnet with financial
support from the European Commission's Next Generation Internet programme, under the aegis of DG
Communications Networks, Content and Technology under grant agreement No 101092990.

|ngizerocore| https://nlnet.nl/project/Back2source-next/



This project was funded through the NGI0 Entrust Fund, a fund established by NLnet with financial
support from the European Commission's Next Generation Internet programme, under the aegis of DG
Communications Networks, Content and Technology under grant agreement No 101069594.

|ngizeroentrust| https://nlnet.nl/project/purl2sym/


.. |nlnet| image:: https://nlnet.nl/logo/banner.png
    :target: https://nlnet.nl
    :height: 50
    :alt: NLnet foundation logo

.. |ngi| image:: https://ngi.eu/wp-content/uploads/thegem-logos/logo_8269bc6efcf731d34b6385775d76511d_1x.png
    :target: https://ngi.eu35
    :height: 50
    :alt: NGI logo

.. |nexb| image:: https://nexb.com/wp-content/uploads/2022/04/nexB.svg
    :target: https://nexb.com
    :height: 30
    :alt: nexB logo

.. |europa| image:: https://ngi.eu/wp-content/uploads/sites/77/2017/10/bandiera_stelle.png
    :target: http://ec.europa.eu/index_en.htm
    :height: 40
    :alt: Europa logo

.. |aboutcode| image:: https://aboutcode.org/wp-content/uploads/2023/10/AboutCode.svg
    :target: https://aboutcode.org/
    :height: 30
    :alt: AboutCode logo

.. |swiss| image:: https://www.sbfi.admin.ch/sbfi/en/_jcr_content/logo/image.imagespooler.png/1493119032540/logo.png
    :target: https://www.sbfi.admin.ch/sbfi/en/home/seri/seri.html
    :height: 40
    :alt: Swiss logo

.. |dgconnect| image:: https://commission.europa.eu/themes/contrib/oe_theme/dist/ec/images/logo/positive/logo-ec--en.svg
    :target: https://commission.europa.eu/about-european-commission/departments-and-executive-agencies/communications-networks-content-and-technology_en
    :height: 40
    :alt: EC DG Connect logo

.. |ngizerocore| image:: https://nlnet.nl/image/logos/NGI0_tag.svg
    :target: https://nlnet.nl/core
    :height: 40
    :alt: NGI Zero Core Logo

.. |ngizerocommons| image:: https://nlnet.nl/image/logos/NGI0_tag.svg
    :target: https://nlnet.nl/commonsfund/
    :height: 40
    :alt: NGI Zero Commons Logo

.. |ngizeropet| image:: https://nlnet.nl/image/logos/NGI0PET_tag.svg
    :target: https://nlnet.nl/PET
    :height: 40
    :alt: NGI Zero PET logo

.. |ngizeroentrust| image:: https://nlnet.nl/image/logos/NGI0Entrust_tag.svg
    :target: https://nlnet.nl/entrust
    :height: 38
    :alt: NGI Zero Entrust logo

.. |ngiassure| image:: https://nlnet.nl/image/logos/NGIAssure_tag.svg
    :target: https://nlnet.nl/image/logos/NGIAssure_tag.svg
    :height: 32
    :alt: NGI Assure logo

.. |ngidiscovery| image:: https://nlnet.nl/image/logos/NGI0Discovery_tag.svg
    :target: https://nlnet.nl/discovery/
    :height: 40
    :alt: NGI Discovery logo






