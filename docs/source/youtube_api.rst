.. _api:

API Guide
===================

The YouTube Data API has a single class :class:`YoutubeDataApi`, which is authenticates your API key and provides a functions to interact with the API.

youtube_api.youtube_api module
------------------------------
This is the client class to access the YouTube API.

.. automodule:: youtube_api.youtube_api
    :members:
    :undoc-members:
    :show-inheritance:


youtube_api.parsers module
--------------------------
Every function from the :mod:`youtube_api.youtube_api` class has an argument for ``parser``. ``parser`` can be any function that takes a dictionary as input. Here are the default parser fucntions for each function. Use these as templates to build your own custom parsers, or use the :meth:`youtube_api.parsers.raw_json` or ``None`` as the ``parser`` argument for the raw API response.

.. automodule:: youtube_api.parsers
    :members:
    :undoc-members:
    :show-inheritance:

youtube_api.youtube_api_utils module
------------------------------------
These are utils used by the client class, with some additional functions for analysis.

.. automodule:: youtube_api.youtube_api_utils
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: youtube_api
    :members:
    :undoc-members:
    :show-inheritance:
