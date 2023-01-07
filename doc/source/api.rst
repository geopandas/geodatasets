.. _reference:


API reference
=============

The ``xyzdata`` package has top-level functions that will cover 95% of use cases and
other tooling handling the database.

Top-level API
-------------

In most cases, you will be using :func:`~xyzdata.get_path` to download the data and get the path
to the local storage, :func:`~xyzdata.get_url` to get the link to the original dataset in its
online location and :func:`~xyzdata.fetch` to pre-download data to the local storage.

.. currentmodule:: xyzdata

.. autofunction:: get_path

.. autofunction:: get_url

.. autofunction:: fetch

Database-level API
------------------

The database of dataset metadata is handled via custom dict-based classes.

.. class:: DataItem

   A dict with attribute-access and that can be called to update keys.

.. autoclass:: Bunch
   :exclude-members: clear, copy, fromkeys, get, items, keys, pop, popitem, setdefault, update, values
   :members: flatten, query_name