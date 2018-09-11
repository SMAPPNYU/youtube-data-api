
Installation
------------

It is recommended to `install this module by using
pip <https://pypi.org/project/youtube-data-api/>`__:

::

    pip install youtube-data-api

.. code:: ipython3

    import os
    import sys
    sys.path.append('../')
    import pandas as pd
    from youtube_api import YoutubeDataApi

.. code:: ipython3

    YT_KEY = os.environ.get('YT_KEY')

.. code:: ipython3

    yt = YoutubeDataApi(YT_KEY)

.. code:: ipython3

    yt.api_version




.. parsed-literal::

    3



.. code:: ipython3

    searches = yt.search(q='alexandria ocasio-cortez',
                         max_results=5)

.. code:: ipython3

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

.. code:: ipython3

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



The parsing step is a functional argument that users can customize so
long as the only argument is dictionary.

You can also get raw JSON from the API by using the ``raw_json`` parser,
or setting parser to ``None``.

.. code:: ipython3

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



We can use these search results as a jumping off point:

.. code:: ipython3

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



.. code:: ipython3

    channel_ids = df_search['channel_id'].tolist()

.. code:: ipython3

    channel_meta = yt.get_channel_metadata(channel_ids)
    df_channel_meta = pd.DataFrame(channel_meta)
    df_channel_meta.head()




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
          <th>channel_id</th>
          <th>title</th>
          <th>account_creation_date</th>
          <th>keywords</th>
          <th>description</th>
          <th>view_count</th>
          <th>video_count</th>
          <th>subscription_count</th>
          <th>playlist_id_likes</th>
          <th>playlist_id_uploads</th>
          <th>topic_ids</th>
          <th>country</th>
          <th>collection_date</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>UCqlYzSgsh5jdtWYfVIBoTDw</td>
          <td>Fox News Insider</td>
          <td>2010-05-24 22:59:16</td>
          <td>"Fox News Channel" "Fox News Insider" "Fox New...</td>
          <td>Fox News Insider is the official live blog of ...</td>
          <td>87814646</td>
          <td>5335</td>
          <td>88218</td>
          <td>None</td>
          <td>UUqlYzSgsh5jdtWYfVIBoTDw</td>
          <td>https://en.wikipedia.org/wiki/Politics|https:/...</td>
          <td>None</td>
          <td>2018-09-05 13:00:59.974571</td>
        </tr>
        <tr>
          <th>1</th>
          <td>UCK7IIV6Q2junGSdYK3BmZMg</td>
          <td>TMZ</td>
          <td>2006-04-10 16:33:09</td>
          <td>Celebrity Gossip "Entertainment News" photos h...</td>
          <td>The LATEST in celebrity gossip and entertainme...</td>
          <td>2938544758</td>
          <td>28237</td>
          <td>3234809</td>
          <td>None</td>
          <td>UUK7IIV6Q2junGSdYK3BmZMg</td>
          <td>https://en.wikipedia.org/wiki/Television_progr...</td>
          <td>None</td>
          <td>2018-09-05 13:00:59.974646</td>
        </tr>
        <tr>
          <th>2</th>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>VICE News</td>
          <td>2013-11-20 15:11:51</td>
          <td>"VICE News" news VICE "VICE Magazine" document...</td>
          <td>VICE News Tonight airs Mon-Thurs 7:30PM on HBO...</td>
          <td>850171581</td>
          <td>3320</td>
          <td>3395698</td>
          <td>LLZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>UUZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>https://en.wikipedia.org/wiki/Society</td>
          <td>US</td>
          <td>2018-09-05 13:00:59.974703</td>
        </tr>
        <tr>
          <th>3</th>
          <td>UCupvZG-5ko_eiXAupbDfxWw</td>
          <td>CNN</td>
          <td>2005-10-02 16:06:36</td>
          <td>CNN "CNN News" news "breaking news"</td>
          <td>CNN operates as a division of Turner Broadcast...</td>
          <td>3555952702</td>
          <td>142391</td>
          <td>4651470</td>
          <td>None</td>
          <td>UUupvZG-5ko_eiXAupbDfxWw</td>
          <td>https://en.wikipedia.org/wiki/Politics|https:/...</td>
          <td>None</td>
          <td>2018-09-05 13:00:59.974755</td>
        </tr>
        <tr>
          <th>4</th>
          <td>UCIRYBXDze5krPDzAEOxFGVA</td>
          <td>Guardian News</td>
          <td>2014-10-22 09:51:00</td>
          <td>"the guardian" guardian wires video news polit...</td>
          <td>The latest news video, live content and news e...</td>
          <td>226810374</td>
          <td>2720</td>
          <td>188842</td>
          <td>LLIRYBXDze5krPDzAEOxFGVA</td>
          <td>UUIRYBXDze5krPDzAEOxFGVA</td>
          <td>https://en.wikipedia.org/wiki/Politics|https:/...</td>
          <td>GB</td>
          <td>2018-09-05 13:00:59.974799</td>
        </tr>
      </tbody>
    </table>
    </div>



Content Analysis of a Channel
-----------------------------

.. code:: ipython3

    channel_playlists = yt.get_playlists(channel_ids[0])
    df_channel_playlists = pd.DataFrame(channel_playlists)
    df_channel_playlists.head()




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
          <th>playlist_name</th>
          <th>playlist_id</th>
          <th>playlist_publish_date</th>
          <th>playlist_n_videos</th>
          <th>channel_id</th>
          <th>channel_name</th>
          <th>collection_date</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>Rohingya Genocide</td>
          <td>PLw613M86o5o74xsZUsa2WGz00HGyk7AoP</td>
          <td>2018-08-28 17:57:40</td>
          <td>4</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>VICE News</td>
          <td>2018-09-05 13:01:00.547527</td>
        </tr>
        <tr>
          <th>1</th>
          <td>The Mueller Investigation</td>
          <td>PLw613M86o5o7S7xjaBsQ32fccvzAbo3q6</td>
          <td>2018-08-22 18:00:52</td>
          <td>13</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>VICE News</td>
          <td>2018-09-05 13:01:00.547597</td>
        </tr>
        <tr>
          <th>2</th>
          <td>Reports on Yemen: VICE News</td>
          <td>PLw613M86o5o4fmmamuzfk5HyVzjcQlFUa</td>
          <td>2018-08-16 16:44:21</td>
          <td>5</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>VICE News</td>
          <td>2018-09-05 13:01:00.547643</td>
        </tr>
        <tr>
          <th>3</th>
          <td>Allison McCann: VICE News Tonight (HBO)</td>
          <td>PLw613M86o5o773pWdt8Odxs_JUDOGuEXN</td>
          <td>2018-08-01 17:51:32</td>
          <td>15</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>VICE News</td>
          <td>2018-09-05 13:01:00.547683</td>
        </tr>
        <tr>
          <th>4</th>
          <td>2018 Emmy Nominated Reports | VICE News</td>
          <td>PLw613M86o5o4cRIuFUOlzIqh5jcFoC2mU</td>
          <td>2018-07-26 16:18:13</td>
          <td>8</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>VICE News</td>
          <td>2018-09-05 13:01:00.547727</td>
        </tr>
      </tbody>
    </table>
    </div>



.. code:: ipython3

    playlist_id = df_channel_playlists.loc[1].playlist_id
    playlist_id




.. parsed-literal::

    'PLw613M86o5o7S7xjaBsQ32fccvzAbo3q6'



.. code:: ipython3

    videos = yt.get_videos_from_playlist_id(playlist_id, parser=None)

.. code:: ipython3

    videos[0]




.. parsed-literal::

    {'kind': 'youtube#playlistItem',
     'etag': '"XI7nbFXulYBIpL0ayR_gDh3eu1k/bPZRQ0F4uxzNmT_FS6J6iDY8qqQ"',
     'id': 'UEx3NjEzTTg2bzVvN1M3eGphQnNRMzJmY2N2ekFibzNxNi41NkI0NEY2RDEwNTU3Q0M2',
     'snippet': {'publishedAt': '2018-08-22T18:01:54.000Z',
      'channelId': 'UCZaT_X_mc0BI-djXOlfhqWQ',
      'title': "Devin Nunes Calls His Own Local Paper 'Fake News' (HBO)",
      'description': 'California Republican Rep. Devin Nunes isn’t just a major Donald Trump defender — he’s also taking a page out of the Trump playbook and attacking his local newspaper as “Fake News.”\n\nIn June, Nunes launched an unusually long ad — running more than two minutes — against the Fresno Bee, for its coverage of a controversy surrounding a winery in which Nunes is invested.\n\n“Sadly, since the last election, The Fresno Bee has worked closely with radical left-wing groups to promote numerous fake news stories about me,” Nunes says in the ad, giving no proof for the claims of collusion.\n\nIt was a rare campaign expenditure for Nunes, who isn’t seen as particularly vulnerable in his deep-red Central Valley district. But it was heard by enough voters in the district that Fresno Bee reporters received an uptick in hate mail, angry social media posts and voicemails denouncing their reporting and the paper.\n\nMackenzie Mays was the Fresno Bee reporter who wrote the original story on the winery controversy. In response to Nunes’ ad, she received voicemails calling her and her colleagues “corrupt bastards” — but she said it wasn’t the first time she’s gotten hate from readers, and their attacks have only gotten more vicious recently — since Trump was elected.\n\nSubscribe to VICE News here: http://bit.ly/Subscribe-to-VICE-News\n\nCheck out VICE News for more: http://vicenews.com\n\nFollow VICE News here:\nFacebook: https://www.facebook.com/vicenews\nTwitter: https://twitter.com/vicenews\nTumblr: http://vicenews.tumblr.com/\nInstagram: http://instagram.com/vicenews\nMore videos from the VICE network: https://www.fb.com/vicevideo',
      'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/LO-X8MMTRco/default.jpg',
        'width': 120,
        'height': 90},
       'medium': {'url': 'https://i.ytimg.com/vi/LO-X8MMTRco/mqdefault.jpg',
        'width': 320,
        'height': 180},
       'high': {'url': 'https://i.ytimg.com/vi/LO-X8MMTRco/hqdefault.jpg',
        'width': 480,
        'height': 360},
       'standard': {'url': 'https://i.ytimg.com/vi/LO-X8MMTRco/sddefault.jpg',
        'width': 640,
        'height': 480},
       'maxres': {'url': 'https://i.ytimg.com/vi/LO-X8MMTRco/maxresdefault.jpg',
        'width': 1280,
        'height': 720}},
      'channelTitle': 'VICE News',
      'playlistId': 'PLw613M86o5o7S7xjaBsQ32fccvzAbo3q6',
      'position': 0,
      'resourceId': {'kind': 'youtube#video', 'videoId': 'LO-X8MMTRco'}}}



.. code:: ipython3

    def custom_parser(item):
        return item['snippet']['resourceId']['videoId']

.. code:: ipython3

    custom_parser(videos[0])




.. parsed-literal::

    'LO-X8MMTRco'



.. code:: ipython3

    video_ids = yt.get_videos_from_playlist_id(playlist_id, parser=custom_parser)

.. code:: ipython3

    df_video_metadata = pd.DataFrame(
        yt.get_video_metadata(video_ids)
    )

.. code:: ipython3

    df_video_metadata




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
          <th>video_view_count</th>
          <th>video_comment_count</th>
          <th>video_like_count</th>
          <th>video_dislike_count</th>
          <th>video_thumbnail</th>
          <th>video_tags</th>
          <th>collection_date</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>LO-X8MMTRco</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-08-22 12:42:39</td>
          <td>Devin Nunes Calls His Own Local Paper 'Fake Ne...</td>
          <td>California Republican Rep. Devin Nunes isn’t j...</td>
          <td>25</td>
          <td>135113</td>
          <td>1090</td>
          <td>2087</td>
          <td>138</td>
          <td>https://i.ytimg.com/vi/LO-X8MMTRco/hqdefault.jpg</td>
          <td>VICE News|VICE News Tonight|VICE on HBO|news|v...</td>
          <td>2018-09-05 13:01:03.969337</td>
        </tr>
        <tr>
          <th>1</th>
          <td>tyBUnEC_VEk</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-08-09 01:03:07</td>
          <td>Fashion Legend André Leon Talley Critiques Pau...</td>
          <td>Paul Manafort, the former chair of President T...</td>
          <td>25</td>
          <td>38723</td>
          <td>218</td>
          <td>1149</td>
          <td>89</td>
          <td>https://i.ytimg.com/vi/tyBUnEC_VEk/hqdefault.jpg</td>
          <td>VICE News|VICE News Tonight|VICE on HBO|news|v...</td>
          <td>2018-09-05 13:01:03.969424</td>
        </tr>
        <tr>
          <th>2</th>
          <td>An2XYJjfAKY</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-08-03 17:21:48</td>
          <td>QAnon Conspiracists Believe Trump and Mueller ...</td>
          <td>If you don't follow QAnon, the internet conspi...</td>
          <td>25</td>
          <td>245994</td>
          <td>3459</td>
          <td>1739</td>
          <td>887</td>
          <td>https://i.ytimg.com/vi/An2XYJjfAKY/hqdefault.jpg</td>
          <td>QAnon believers|We Spoke To The QAnon Believer...</td>
          <td>2018-09-05 13:01:03.969484</td>
        </tr>
        <tr>
          <th>3</th>
          <td>YR2FxeyXw9c</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-08-02 16:37:08</td>
          <td>The Trump Fans Of Q-Anon (HBO)</td>
          <td>President Trump is flying around the country t...</td>
          <td>25</td>
          <td>251507</td>
          <td>3229</td>
          <td>1920</td>
          <td>1077</td>
          <td>https://i.ytimg.com/vi/YR2FxeyXw9c/hqdefault.jpg</td>
          <td>Meet the Trump fans of Q-Anon|Trump fans|QAnon...</td>
          <td>2018-09-05 13:01:03.969539</td>
        </tr>
        <tr>
          <th>4</th>
          <td>SJBQikfYyKs</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-07-17 01:06:14</td>
          <td>American Scholars Say The Real Threat To The U...</td>
          <td>President Trump set off a roar of outrage when...</td>
          <td>25</td>
          <td>111565</td>
          <td>1260</td>
          <td>2324</td>
          <td>411</td>
          <td>https://i.ytimg.com/vi/SJBQikfYyKs/hqdefault.jpg</td>
          <td>russophobia in usa|russophobia|VICE News|VICE ...</td>
          <td>2018-09-05 13:01:03.969592</td>
        </tr>
        <tr>
          <th>5</th>
          <td>9zQU_jI4Mek</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-07-11 00:13:09</td>
          <td>We Spoke To Emin Agalarov About A Conversation...</td>
          <td>When President Donald Trump’s eldest son Don J...</td>
          <td>25</td>
          <td>32803</td>
          <td>239</td>
          <td>362</td>
          <td>172</td>
          <td>https://i.ytimg.com/vi/9zQU_jI4Mek/hqdefault.jpg</td>
          <td>vice emin agalarov interview|emin agalarov|Don...</td>
          <td>2018-09-05 13:01:03.969643</td>
        </tr>
        <tr>
          <th>6</th>
          <td>W5igBNtpoj0</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-05-18 17:27:33</td>
          <td>Here's How Much Americans Bitterly Disagree Ab...</td>
          <td>We’re officially one year into the Russia inve...</td>
          <td>25</td>
          <td>91913</td>
          <td>912</td>
          <td>958</td>
          <td>192</td>
          <td>https://i.ytimg.com/vi/W5igBNtpoj0/hqdefault.jpg</td>
          <td>VICE News|donald trump|fox news|Fox and Friend...</td>
          <td>2018-09-05 13:01:03.969700</td>
        </tr>
        <tr>
          <th>7</th>
          <td>9yPvRaKQikE</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-03-20 00:12:02</td>
          <td>Christopher Wylie: The Whistleblower Who Expos...</td>
          <td>LONDON — Christopher Wylie played a big role i...</td>
          <td>25</td>
          <td>100021</td>
          <td>520</td>
          <td>1426</td>
          <td>298</td>
          <td>https://i.ytimg.com/vi/9yPvRaKQikE/hqdefault.jpg</td>
          <td>Christopher Wylie|Whisteblower|whistleblower|n...</td>
          <td>2018-09-05 13:01:03.969752</td>
        </tr>
        <tr>
          <th>8</th>
          <td>WKve2MdljW4</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-02-06 01:05:11</td>
          <td>Devin Nunes' Democratic Opponent Is Raising Mo...</td>
          <td>Within 72 hours of Devin Nunes’ memo dropping,...</td>
          <td>25</td>
          <td>25632</td>
          <td>262</td>
          <td>347</td>
          <td>181</td>
          <td>https://i.ytimg.com/vi/WKve2MdljW4/hqdefault.jpg</td>
          <td>VICE News|VICE News Tonight|VNT|HBO|Vice|Russi...</td>
          <td>2018-09-05 13:01:03.969803</td>
        </tr>
        <tr>
          <th>9</th>
          <td>m-6ECS4kYJE</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2018-02-02 20:04:02</td>
          <td>How The Nunes Memo Is A Danger To Democracy (HBO)</td>
          <td>There seems to be some real parallels between ...</td>
          <td>25</td>
          <td>122176</td>
          <td>1278</td>
          <td>2027</td>
          <td>2179</td>
          <td>https://i.ytimg.com/vi/m-6ECS4kYJE/hqdefault.jpg</td>
          <td>VICE News Tonight|VICE on HBO|Shawna Thomas|Ri...</td>
          <td>2018-09-05 13:01:03.969852</td>
        </tr>
        <tr>
          <th>10</th>
          <td>VnOf8ZhIH7I</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2017-12-02 01:11:36</td>
          <td>Trump Has A Lot To Be Worried About Now That F...</td>
          <td>Donald Trump’s former national security advise...</td>
          <td>25</td>
          <td>184367</td>
          <td>862</td>
          <td>2680</td>
          <td>611</td>
          <td>https://i.ytimg.com/vi/VnOf8ZhIH7I/hqdefault.jpg</td>
          <td>Donald Trump|Michael Flynn|Trump administratio...</td>
          <td>2018-09-05 13:01:03.969902</td>
        </tr>
        <tr>
          <th>11</th>
          <td>b6bCBzosKyg</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2017-07-18 18:48:48</td>
          <td>Meet Mueller's All-Star Legal Team That Could ...</td>
          <td>President Trump says the federal investigation...</td>
          <td>25</td>
          <td>51516</td>
          <td>527</td>
          <td>1451</td>
          <td>811</td>
          <td>https://i.ytimg.com/vi/b6bCBzosKyg/hqdefault.jpg</td>
          <td>VICE News|news|VICE|documentary|interviews|wor...</td>
          <td>2018-09-05 13:01:03.969953</td>
        </tr>
        <tr>
          <th>12</th>
          <td>aRXMDKrJAu0</td>
          <td>VICE News</td>
          <td>UCZaT_X_mc0BI-djXOlfhqWQ</td>
          <td>2017-07-07 18:22:08</td>
          <td>Flynn Regretted "Lock Her Up" Speech Almost Im...</td>
          <td>The minute Michael Flynn walked off the stage ...</td>
          <td>25</td>
          <td>206539</td>
          <td>520</td>
          <td>1867</td>
          <td>265</td>
          <td>https://i.ytimg.com/vi/aRXMDKrJAu0/hqdefault.jpg</td>
          <td>VICE News|news|VICE|VICE Magazine|documentary|...</td>
          <td>2018-09-05 13:01:03.970002</td>
        </tr>
      </tbody>
    </table>
    </div>



Network Analysis
================

.. code:: ipython3

    df_channel_meta['channel_id'].tolist()




.. parsed-literal::

    ['UCqlYzSgsh5jdtWYfVIBoTDw',
     'UCK7IIV6Q2junGSdYK3BmZMg',
     'UCZaT_X_mc0BI-djXOlfhqWQ',
     'UCupvZG-5ko_eiXAupbDfxWw',
     'UCIRYBXDze5krPDzAEOxFGVA']



.. code:: ipython3

    df_channel_meta['channel_id'][0]




.. parsed-literal::

    'UCqlYzSgsh5jdtWYfVIBoTDw'



.. code:: ipython3

    featured_channels = yt.get_featured_channels(df_channel_meta['channel_id'].tolist())

.. code:: ipython3

    featured_channels




.. parsed-literal::

    [{'UCqlYzSgsh5jdtWYfVIBoTDw': ['UCXIJgqnII2ZOINSWNOGFThA',
       'UCCXoCcu9Rp7NPbTzIvogpZg']},
     {'UCK7IIV6Q2junGSdYK3BmZMg': ['UCE3yf1AcIlXdps2EYbq3lzw',
       'UC9_3h1t3FEvhC-1toDU3fww',
       'UCrJWWrN-jsSau3Kmb1WUeCw']},
     {'UCZaT_X_mc0BI-djXOlfhqWQ': ['UCn8zNIfYAQNdrFRrr8oibKw',
       'UCWF0PiUvUi3Jma2oFgaiX2w',
       'UCfQDD-pbllOCXHYwiXxjJxA',
       'UC0iwHRFpv2_fpojZgQhElEQ',
       'UCB6PV0cvJpzlcXRG7nz6PpQ',
       'UC8C8WuWSsFjWFaTHcUQeQxA',
       'UCaLfMkkHhSA_LaCta0BzyhQ',
       'UC9ISPZsMaBi5mutsgX6LC1g',
       'UCiZCX1R1F3xYGbeXq1JscKA',
       'UCflb1gG-X1dy1Ru5JIk5sPw',
       'UCNDUud96oGK5xQ9gyg913vw',
       'UCroeDtD1dtd1leuxUHDMTXQ']},
     {'UCupvZG-5ko_eiXAupbDfxWw': ['UCRrW0ddrbFnJCbyZqHHv4KQ',
       'UCF93huicBH0WApJjUmrCxzg',
       'UCovKb3Mf_h3bsY9gEWoR-bg',
       'UCgPClNr5VSYC3syrDUIlzLw',
       'UCgCudMsK-kxYxB2RgiS3bzQ',
       'UC1DZpQ2DDExws9Zvl7UcSkg',
       'UCi7GJNg51C3jgmYTUwqoUXA',
       'UCMsgXPD3wzzt8RxHJmXH7hQ']},
     {'UCIRYBXDze5krPDzAEOxFGVA': ['UCHpw8xwDNhU9gdohEcJu4aA',
       'UCSYCo8uRGF39qDCxF870K5Q',
       'UCNHqb1IRxQ5WBsWtO53JL2g',
       'UC4OxS-w63-g00lI7nGkzpcw',
       'UCwD9E_QNwFwrQC7OnPnrg2Q',
       'UCQvWVVSmrbF6ID3_hB7yYqg']}]



.. code:: ipython3

    channels = {}
    for c in featured_channels:
        channels = {**channels, **c}

.. code:: ipython3

    nodes = []
    edges = []
    for d in featured_channels:
        for channel, subs in d.items():
            all_channels += [channel] + subs
            for sub in subs:
                edges.append((channel, sub))

.. code:: ipython3

    import networkx as nx
    G = nx.DiGraph()

.. code:: ipython3

    G




.. parsed-literal::

    <networkx.classes.graph.Graph at 0x2ae1c1270128>



.. code:: ipython3

    G.add_nodes_from(nodes)

.. code:: ipython3

    G.add_edges_from(edges)

.. code:: ipython3

    %matplotlib inline
    import matplotlib.pyplot as plt

.. code:: ipython3

    plt.figure(figsize=(16,8))
    plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    # nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')



.. image:: output_37_0.png

