..
   Developer Notes:
   This is the index file that outlines the usage principles for the AAanalysis package.
   Files for individual usage principles are stored in the /usage_principles directory.

   This document provides an overview of:
   - Component diagram (illustrating internal dependencies)

   Instead of including comprehensive tables here, refer to tables in tables.rst with concise explanations.
   Always include brief code examples that mirror the corresponding usage examples.
..

.. _usage_principles:

Usage Principles
================
To get started with AAanalysis, import it as follows:

.. code-block:: python

    import aaanalysis as aa

AAanalysis provides a handful of DataFrames for seamless data management. Starting with amino acid scale information
(**df_scales**, **df_cat**) and protein sequences (**df_seq**), it enables segmentation into parts (**df_parts**)
and accommodates user-defined splitting (**split_kws**). Our CPP algorithm then utilizes these to generate
physicochemical features (**df_feat**) by comparing protein sequence sets.

See the primary analysis pipeline of the AAanalysis framework in this diagram:

.. image:: /_artwork/diagrams/components.png
   :align: center
   :alt: AAanalysis workflow

   AAanalysis pipeline illustrating the typical data flow, represented as data frames, with key
   methods (Python classes) highlighted by black squares.

Details on the foundational concepts of AAnalysis are provided by the following sections:

.. toctree::
   :maxdepth: 1

   usage_principles/aaontology
   usage_principles/aaclust
   usage_principles/feature_identification
   usage_principles/pu_learning
   usage_principles/xai
