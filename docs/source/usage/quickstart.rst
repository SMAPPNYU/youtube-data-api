Installation
------------

It is recommended to `install this module by using
pip <https://pypi.org/project/youtube-data-api/>`__:

::

    pip install youtube-data-api


.. _quickstart:

Quickstart
----------

.. code:: python

    import os
    import pandas as pd
    from youtube_api import YoutubeDataApi

In order to access the API, you'll need to get a `service key <https://developers.google.com/youtube/registering_an_application#Create_API_Keys>`_ from the `Google Cloud Console <https://console.cloud.google.com/>` . I like to store my API keys as environment variables in ``~/.bash_profile`` so that I don't have to hard code them.:

.. code:: python

    YT_KEY = os.environ.get('YOUTUBE_API_KEY') # you can hardcode this, too.
    yt = YouTubeDataAPI(YT_KEY)

We now have created a ``YouTubeDataAPI`` class as ``yt``, which can be used to make API calls, such as searching for the most relevant videos of Alexandra Ocasio-Cortez.

.. code:: python

    searches = yt.search(q='alexandria ocasio-cortez',
                         max_results=5)
    searches[0]

.. parsed-literal::

       {'video_id': 'LlillsHgcaw',
        'channel_title': 'Fox News',
        'channel_id': 'UCXIJgqnII2ZOINSWNOGFThA',
        'video_publish_date': datetime.datetime(2019, 2, 19, 4, 57, 51),
        'video_title': 'Rep. Alexandria Ocasio-Cortez taken to task by fellow progressives',
        'video_description': 'New York City Mayor Bill de Blasio criticizes Alexandria Ocasio-Cortez over her opposition to the Amazon deal.',
        'video_category': None,
        'video_thumbnail': 'https://i.ytimg.com/vi/LlillsHgcaw/hqdefault.jpg',
        'collection_date': datetime.datetime(2019, 2, 20, 14, 48, 19, 487877)}



All API requests are parsed from raw JSON into `dictionaries <https://docs.python.org/3/library/stdtypes.html#typesmapping>` .
Typically an API call returns a list of dictionary objects. This is
perfect for converting into Pandas `DataFrames <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>` , or saving as JSON.

.. code:: python

    df_search = pd.DataFrame(searches)
    df_search[['channel_title', 'video_title', 'video_publish_date']]




.. raw:: html

    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>channel_title</th>
          <th>video_title</th>
          <th>video_publish_date</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>Fox News</td>
          <td>Rep. Alexandria Ocasio-Cortez taken to task by...</td>
          <td>2019-02-19 04:57:51</td>
        </tr>
        <tr>
          <th>1</th>
          <td>Fox News</td>
          <td>Critics mock Ocasio-Cortez's Green New Deal ro...</td>
          <td>2019-02-19 00:34:22</td>
        </tr>
        <tr>
          <th>2</th>
          <td>NBC News</td>
          <td>Rep. Ocasio-Cortez Defends Green New Deal In I...</td>
          <td>2019-02-16 21:40:10</td>
        </tr>
        <tr>
          <th>3</th>
          <td>EL PAIS</td>
          <td>ALEXANDRIA OCASIO-CORTEZ: "Sed valientes con n...</td>
          <td>2019-02-17 11:03:09</td>
        </tr>
        <tr>
          <th>4</th>
          <td>FOX 10 Phoenix</td>
          <td>NO SOCIALISM: President Trump Takes On Alexand...</td>
          <td>2019-02-18 22:20:22</td>
        </tr>
      </tbody>
    </table>



Aside from the default parser, the ``parse`` argument allows users to create custom functions to parse and process API resonses. You can also get raw JSON from the API by using the :meth:`youtube_api.parsers.raw_json` parser, or setting parser to ``None``.

.. code:: python

    yt.search(q='alexandria ocasio-cortez', 
              max_results=1,
              parser=None)



.. parsed-literal::

    [{'kind': 'youtube#searchResult',
      'etag': '"XI7nbFXulYBIpL0ayR_gDh3eu1k/iwS8DlBT9x9lWSRCq4JFPMR-Z00"',
      'id': {'kind': 'youtube#video', 'videoId': 'byc_lBOY_rI'},
      'snippet': {'publishedAt': '2018-07-31T18:52:29.000Z',
       'channelId': 'UCZaT_X_mc0BI-djXOlfhqWQ',
       'title': "Who's Afraid Of Alexandria Ocasio-Cortez? Everyone (HBO)",
       'description': "Alexandria Ocasio-Cortez shocked Democrats when she won a New York City primary over one of the party's entrenched leaders. Her next chapter is likely to be ...",
       'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/byc_lBOY_rI/default.jpg',
         'width': 120,
         'height': 90},
        'medium': {'url': 'https://i.ytimg.com/vi/byc_lBOY_rI/mqdefault.jpg',
         'width': 320,
         'height': 180},
        'high': {'url': 'https://i.ytimg.com/vi/byc_lBOY_rI/hqdefault.jpg',
         'width': 480,
         'height': 360}},
       'channelTitle': 'VICE News',
       'liveBroadcastContent': 'none'}}]

:mod:`youtube_api.parsers` are intended to allow customized data parsing for those who want it, with robust defaults for less advanced users.