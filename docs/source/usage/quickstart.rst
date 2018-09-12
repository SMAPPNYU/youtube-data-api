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

In order to access the API, you'll need to get a `service key <https://developers.google.com/youtube/registering_an_application#Create_API_Keys>`_ from the `Google Cloud Console <https://console.cloud.google.com/>`_. I like to store my API keys as environment variables in ``~/.bash_profile`` so that I don't have to hard code them.:

.. code:: python

    YT_KEY = os.environ.get('YOUTUBE_API_KEY') # you can hardcode this, too.
    yt = YoutubeDataApi(YT_KEY)

We now have created a ``YoutubeDataAPi`` class as ``yt``, which can be used to make API calls, such as searching for the most relevant videos of Alexandra Ocasio-Cortez.

.. code:: python

    searches = yt.search(q='alexandria ocasio-cortez',
                         max_results=5)
    searches[0]

.. parsed-literal::

    OrderedDict([('video_id', 'byc_lBOY_rI'),
                 ('channel_title', 'VICE News'),
                 ('channel_id', 'UCZaT_X_mc0BI-djXOlfhqWQ'),
                 ('video_publish_date',
                  datetime.datetime(2018, 7, 31, 18, 52, 29)),
                 ('video_title',
                  "Who's Afraid Of Alexandria Ocasio-Cortez? Everyone (HBO)"),
                 ('video_description',
                  "Alexandria Ocasio-Cortez shocked Democrats when she won a New York City primary over one of the party's entrenched leaders. Her next chapter is likely to be ..."),
                 ('video_thumbnail',
                  'https://i.ytimg.com/vi/byc_lBOY_rI/hqdefault.jpg'),
                 ('collection_date',
                  datetime.datetime(2018, 9, 5, 14, 47, 53, 196104))])



All API requests are parsed from raw JSON into
`orderedDictionaries <https://docs.python.org/3/library/collections.html#collections.OrderedDict>`__.
Typically an API call returns a list of OrderedDict objects. This is
perfect for converting into Pandas DataFrames, or saving as JSON.

.. code:: python

    df_search = pd.DataFrame(searches)
    df_search




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>video_id</th>
          <th>channel_title</th>
          <th>channel_id</th>
          <th>video_publish_date</th>
          <th>video_title</th>
          <th>video_description</th>
          <th>video_category</th>
          <th>video_thumbnail</th>
          <th>collection_date</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>r1yvfdUG5pQ</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-06-28 16:42:29</td>
          <td>Alexandria Ocasio-Cortez: There's Room For Dem...</td>
          <td>First-time candidate and 28-year-old Alexandri...</td>
          <td>None</td>
          <td>https://i.ytimg.com/vi/r1yvfdUG5pQ/hqdefault.jpg</td>
          <td>2018-09-05 13:00:59.386546</td>
        </tr>
        <tr>
          <th>1</th>
          <td>VjsjoaQXrhI</td>
          <td>TMZ</td>
          <td>UCK7IIV6Q2junGSdYK3BmZMg</td>
          <td>2018-08-27 13:17:45</td>
          <td>Viola Davis Endorses NY Congressional Candidat...</td>
          <td>Viola Davis has one person in mind when it com...</td>
          <td>None</td>
          <td>https://i.ytimg.com/vi/VjsjoaQXrhI/hqdefault.jpg</td>
          <td>2018-09-05 13:00:59.386617</td>
        </tr>
        <tr>
          <th>2</th>
          <td>I3wSSShwwwo</td>
          <td>CNN</td>
          <td>UCupvZG-5ko_eiXAupbDfxWw</td>
          <td>2018-08-09 09:31:43</td>
          <td>Cuomo presses Ocasio-Cortez on healthcare</td>
          <td>Democratic congressional candidate Alexandria ...</td>
          <td>None</td>
          <td>https://i.ytimg.com/vi/I3wSSShwwwo/hqdefault.jpg</td>
          <td>2018-09-05 13:00:59.386663</td>
        </tr>
        <tr>
          <th>3</th>
          <td>iC0l6tKbBJs</td>
          <td>Fox News Insider</td>
          <td>UCqlYzSgsh5jdtWYfVIBoTDw</td>
          <td>2018-07-19 12:56:02</td>
          <td>Joe Lieberman: If Ocasio-Cortez is a Party Mod...</td>
          <td>As seen on Your World with Neil Cavuto Former ...</td>
          <td>None</td>
          <td>https://i.ytimg.com/vi/iC0l6tKbBJs/hqdefault.jpg</td>
          <td>2018-09-05 13:00:59.386708</td>
        </tr>
        <tr>
          <th>4</th>
          <td>lAb2QMw9h_w</td>
          <td>Guardian News</td>
          <td>UCIRYBXDze5krPDzAEOxFGVA</td>
          <td>2018-06-28 09:16:39</td>
          <td>'This is the beginning': Alexandria Ocasio-Cor...</td>
          <td>Victorious Democratic candidate addresses supp...</td>
          <td>None</td>
          <td>https://i.ytimg.com/vi/lAb2QMw9h_w/hqdefault.jpg</td>
          <td>2018-09-05 13:00:59.386746</td>
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