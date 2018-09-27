.. _overview:

YouTube Data API
============================================
YouTube is a social media platform that is often overlooked in academic research. This package seeks to make this data source more accessible, while introducing new applications and methods to analyze this platform.

This client is built for GET requests from public data on YouTube. It does not work for updating data on YouTube Channels you own, or getting data from managed accounts from the `Reporting API <https://developers.google.com/youtube/reporting/v1/reports/>`_.

You can find the software on `Github <http://bit.ly/YouTubeDataAPIGitHub>`_.

**Installation**

You can download the package from PyPI:

.. code:: bash

    pip install youtube-data-api

**Quickstart**

In order to access the API, you'll need to get a `service key <https://developers.google.com/youtube/registering_an_application#Create_API_Keys>`_ from the `Google Cloud Console <https://console.cloud.google.com/>`_.

.. code:: python

    from youtube_api import YoutubeDataApi

    api_key = 'AKAIXXXXXXXX'
    yt = YoutubeDataApi(api_key)

    yt.search('alexandria ocasio-cortez')

There's a more detailed section on the :ref:`quickstart` page.