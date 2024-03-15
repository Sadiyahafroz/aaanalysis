..
   Developer Notes:
   This is the landing page for the AAanalysis documentation using Sphinx, containing the root `toctree` directive.
   The documentation will be hosted on Read the docs.
..

Welcome to the AAanalysis documentation!
========================================
.. include:: index/badges.rst
.. include:: index/overview.rst

Install
=======
**AAanalysis** can be installed either from `PyPi <https://pypi.org/project/aaanalysis>`_ or
`conda-forge <https://anaconda.org/conda-forge/aaanalysis>`_:

.. code-block:: bash

   pip install -u aaanalysis
   or
   conda install -c conda-forge aaanalysis

**Note**: Please use Python 3.9 and pip to avoid any dependency issues. Support for Python 3.10 to 3.12 is
planned for the next release.

.. toctree::
   :maxdepth: 1
   :caption: OVERVIEW

   index/introduction.rst
   index/CONTRIBUTING_COPY.rst
   index/usage_principles.rst
   index/evaluation.rst

.. toctree::
   :maxdepth: 1
   :caption: EXAMPLES

   tutorials.rst

.. toctree::
   :maxdepth: 2
   :caption: REFERENCES

   api.rst

.. toctree::
   :maxdepth: 1

   index/tables.rst
   index/references.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Citation
========

.. include:: index/citations.rst
