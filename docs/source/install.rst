:tocdepth: 1

============
Installation
============

Latest realease
===============

You can install the latest release using pip:

.. code-block:: bash

    pip install semanticscholar

Development version
===================

You can install the latest development version from GitHub:

.. code-block:: bash

    git clone git@github.com:danielnsilva/semanticscholar.git
    cd semanticscholar
    pip install .

Alternatively, you can use VCS support:

.. code-block:: bash

    pip install git+https://github.com/danielnsilva/semanticscholar@master

Previous versions
=================

For previous versions of the library, please refer to the `releases page in GitHub <https://github.com/danielnsilva/semanticscholar/releases>`_ or the `Python Package Index <https://pypi.org/project/semanticscholar/>`_.


Requirements
============

* Python 3.8+ (https://www.python.org/)
* tenacity (https://tenacity.readthedocs.io/en/latest/)
* httpx (https://www.python-httpx.org/)
* nest_asyncio (https://github.com/erdewit/nest_asyncio/)
