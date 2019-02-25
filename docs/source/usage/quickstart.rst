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

In order to access the API, you'll need to get a `service key <https://developers.google.com/youtube/registering_an_application#Create_API_Keys>`_ from the `Google Cloud Console <https://console.cloud.google.com/>`_ . I like to store my API keys as environment variables in ``~/.bash_profile`` so that I don't have to hard code them.:

.. code:: python

    YT_KEY = os.environ.get('YOUTUBE_API_KEY') # you can hardcode this, too.
    yt = YouTubeDataAPI(YT_KEY)

We now have created a ``YouTubeDataAPI`` class as ``yt``, which can be used to make API calls, such as searching for the most relevant videos of Alexandria Ocasio-Cortez.

.. code:: python

    searches = yt.search(q='alexandria ocasio-cortez',
                         max_results=5)
    print(searches[0])

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



All API requests are parsed from raw JSON into
`dictionaries <https://docs.python.org/3/library/stdtypes.html#typesmapping>`_.

Typically an API call returns a list of dictionary objects. This is
perfect for converting into Pandas `DataFrames <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_, or saving as JSON.

.. code:: python

    df_search = pd.DataFrame(searches)
    df_search.head(5)




.. raw:: html

    <div class="wy-table-responsive">
        <table border="1" class="docutils">
          <thead>
            <tr style="text-align: right;">
              <th></th>
              <th>channel_id</th>
              <th>channel_title</th>
              <th>collection_date</th>
              <th>video_category</th>
              <th>video_description</th>
              <th>video_id</th>
              <th>video_publish_date</th>
              <th>video_thumbnail</th>
              <th>video_title</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th>0</th>
              <td>UCXIJgqnII2ZOINSWNOGFThA</td>
              <td>Fox News</td>
              <td>2019-02-20 14:49:34.262643</td>
              <td>None</td>
              <td>New York City Mayor Bill de Blasio criticizes ...</td>
              <td>LlillsHgcaw</td>
              <td>2019-02-19 04:57:51</td>
              <td>https://i.ytimg.com/vi/LlillsHgcaw/hqdefault.jpg</td>
              <td>Rep. Alexandria Ocasio-Cortez taken to task by...</td>
            </tr>
            <tr>
              <th>1</th>
              <td>UCXIJgqnII2ZOINSWNOGFThA</td>
              <td>Fox News</td>
              <td>2019-02-20 14:49:34.262672</td>
              <td>None</td>
              <td>Alexandria Ocasio-Cortez's new environmental m...</td>
              <td>3EazY4bw6u8</td>
              <td>2019-02-19 00:34:22</td>
              <td>https://i.ytimg.com/vi/3EazY4bw6u8/hqdefault.jpg</td>
              <td>Critics mock Ocasio-Cortez's Green New Deal ro...</td>
            </tr>
            <tr>
              <th>2</th>
              <td>UCeY0bbntWzzVIaj2z3QigXg</td>
              <td>NBC News</td>
              <td>2019-02-20 14:49:34.262693</td>
              <td>None</td>
              <td>Newly-elected Rep. Alexandria Ocasio-Cortez (D...</td>
              <td>8YH0t3H1Y_Y</td>
              <td>2019-02-16 21:40:10</td>
              <td>https://i.ytimg.com/vi/8YH0t3H1Y_Y/hqdefault.jpg</td>
              <td>Rep. Ocasio-Cortez Defends Green New Deal In I...</td>
            </tr>
            <tr>
              <th>3</th>
              <td>UCnsvJeZO4RigQ898WdDNoBw</td>
              <td>EL PAIS</td>
              <td>2019-02-20 14:49:34.262713</td>
              <td>None</td>
              <td>Alexandria Ocasio-Cortez jura en Nueva York su...</td>
              <td>wAmEYOcnu_g</td>
              <td>2019-02-17 11:03:09</td>
              <td>https://i.ytimg.com/vi/wAmEYOcnu_g/hqdefault.jpg</td>
              <td>ALEXANDRIA OCASIO-CORTEZ: "Sed valientes con n...</td>
            </tr>
            <tr>
              <th>4</th>
              <td>UCJg9wBPyKMNA5sRDnvzmkdg</td>
              <td>FOX 10 Phoenix</td>
              <td>2019-02-20 14:49:34.262733</td>
              <td>None</td>
              <td>President Donald Trump is expected to urge Ven...</td>
              <td>VhEo5sm5Eu4</td>
              <td>2019-02-18 22:20:22</td>
              <td>https://i.ytimg.com/vi/VhEo5sm5Eu4/hqdefault.jpg</td>
              <td>NO SOCIALISM: President Trump Takes On Alexand...</td>
            </tr>
          </tbody>
        </table>
    </div>



Aside from the default parser, the ``parse`` argument allows users to create custom functions to parse and process API resonses. You can also get raw JSON from the API by using the :meth:`youtube_api.parsers.raw_json` parser, or setting parser to ``None``.

.. code:: python

    yt.search(q='alexandria ocasio-cortez', 
              max_results=1,
              parser=None)



.. parsed-literal::

    [{'kind': 'youtube#searchResult',
      'etag': '"XpPGQXPnxQJhLgs6enD_n8JR4Qk/aGNxqVTPJsGI6aEI2tVnYhn0vS8"',
      'id': {'kind': 'youtube#video', 'videoId': 'LlillsHgcaw'},
      'snippet': {'publishedAt': '2019-02-19T04:57:51.000Z',
       'channelId': 'UCXIJgqnII2ZOINSWNOGFThA',
       'title': 'Rep. Alexandria Ocasio-Cortez taken to task by fellow progressives',
       'description': 'New York City Mayor Bill de Blasio criticizes Alexandria Ocasio-Cortez over her opposition to the Amazon deal.',
       'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/LlillsHgcaw/default.jpg',
         'width': 120,
         'height': 90},
        'medium': {'url': 'https://i.ytimg.com/vi/LlillsHgcaw/mqdefault.jpg',
         'width': 320,
         'height': 180},
        'high': {'url': 'https://i.ytimg.com/vi/LlillsHgcaw/hqdefault.jpg',
         'width': 480,
         'height': 360}},
       'channelTitle': 'Fox News',
       'liveBroadcastContent': 'none'}}]

:mod:`youtube_api.parsers` are intended to allow customized data parsing for those who want it, with robust defaults for less advanced users.