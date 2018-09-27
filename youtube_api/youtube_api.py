import time
import requests
import datetime
from collections import OrderedDict
import warnings
import urllib.parse
from pytube import YouTube
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import pandas as pd

# fix importing errors
from youtube_api.youtube_api_utils import *
import youtube_api.parsers as P

"""
This script has the YouTubeDataApi class and functions for the API's endpoints.
"""

__all__ = ['YoutubeDataApi']

class YoutubeDataApi:
    """
    The Youtube Data API handles the keys and methods to access data from the YouTube Data API
    """
    def __init__(self, key, api_version='3'):
        """
        :param key: YouTube Data API key
        Get a YouTube Data API key here: https://console.cloud.google.com/apis/dashboard
        """
        self.key = key
        self.api_version = int(api_version)

        if not self.key:
            raise ValueError('No API key used to initate the class.')
        if not self.verify_key():
            raise ValueError('The API Key is invalid')


    def verify_key(self):
        '''
        Checks it the API key is valid.
        '''
        http_endpoint = ("https://www.googleapis.com/youtube/v{}/playlists"
                         "?part=id&id=UC_x5XG1OV2P6uZZ5FSM9Ttw&"
                         "key={}&maxResults=2".format(self.api_version, self.key))
        response = requests.get(http_endpoint)
        try:
            response.raise_for_status()
            return True
        except:
            return False

        
    def get_channel_id_from_user(self, username):
        """
        Get a channel_id from a YouTube username.
        To get video_ids from the channel_id, you need to get the "upload playlist id".
        This can be done using `get_upload_playlist()` for `get_channel_metadata()`.
        
        Read the docs: https://developers.google.com/youtube/v3/docs/channels/list

        :param username: the username for a YouTube channel
        :type username: str

        :returns: the YouTube channel id for the given username
        """
        http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                         "?part=id"
                         "&forUsername={}&key={}".format(self.api_version, 
                                                         username, self.key))
        response = requests.get(http_endpoint)
        response_json = _load_response(response)
        channel_id = None
        if response_json.get('items'):
            channel_id = response_json['items'][0]['id']
        return channel_id
    
    
    def get_channel_metadata_gen(self, channel_id, parser=P.parse_channel_metadata):
        '''
        Gets a dictionary of channel metadata given a channel_id, or a list of channel_ids.

        :param channel_id: (str or list of str) the channel id(s)
        :type channel_id: str or list
        :param parser: (func) the function to parse the json document.

        :returns: the YouTube channel metadata
        '''
        parser=parser if parser else P.raw_json
        if isinstance(channel_id, list) or isinstance(channel_id, pd.Series):
            for chunk in _chunker(channel_id, 50):
                http_endpoint = ("https://www.googleapis.com/youtube/v3/channels?"
                                "part=id,snippet,contentDetails,statistics,"
                                 "topicDetails,brandingSettings&"
                                 "id={}&key={}&maxResults=50".format(','.join(chunk),
                                                                     self.key))
                response = requests.get(http_endpoint)
                response_json = _load_response(response)
                if response_json.get('items'):
                    for item in response_json['items']:
                        yield parser(item)
                else:
                    yield parser(None)
                    
                    
    def get_channel_metadata(self, channel_id, parser=P.parse_channel_metadata):
        '''
        Gets a dictionary of channel metadata given a channel_id, or a list of channel_ids.

        :param channel_id: (str or list of str) the channel id(s)
        :type channel_id: str or list
        :param parser: (func) the function to parse the json document.

        :returns: the YouTube channel metadata
        '''
        parser=parser if parser else P.raw_json
        channel_meta = []
        if isinstance(channel_id, str):
            http_endpoint = ("https://www.googleapis.com/youtube/v3/channels?"
                             "part=id,snippet,contentDetails,statistics,"
                             "topicDetails,brandingSettings&"
                             "id={}&key={}&maxResults=50".format(channel_id, 
                                                                 self.key))
            response = requests.get(http_endpoint)
            response_json = _load_response(response)
            if response_json.get('items'):
                channel_meta = parser(response_json['items'][0])
                    
        elif isinstance(channel_id, list) or isinstance(channel_id, pd.Series):
            for channel_meta_ in self.get_channel_metadata_gen(channel_id):
                channel_meta.append(channel_meta_)
        else:
            raise TypeError("Could not process the type entered!")

        return channel_meta
    
        
    def get_video_metadata_gen(self, video_id, parser=P.parse_video_metadata):
        '''
        Given a `video_id` returns metrics (views, likes, comments) and metadata (description, category) as a dictionary.
        
        Read the docs: https://developers.google.com/youtube/v3/docs/videos/list

        :param video_id: (str or list of str) the ID of a video IE:['kNbhUWLH_yY'], this can be found at the end of Youtube urls and by parsing links using `get_youtube_id()`
        :param parser: (func) the function to parse the json document

        :returns: a list of dictionaries containing metadata.
        '''
        parser=parser if parser else P.raw_json
        if isinstance(video_id, list) or isinstance(video_id, pd.Series):
            for chunk in _chunker(video_id, 50):
                id_input = ','.join(chunk)
                http_endpoint = ("https://www.googleapis.com/youtube/v{}/videos"
                                 "?part=statistics,snippet"
                                 "&id={}&key={}&maxResults=50".format(
                                    self.api_version, id_input, self.key))
                response = requests.get(http_endpoint)
                response_json = _load_response(response)
                if response_json.get('items'):
                    for item in response_json['items']:
                        yield parser(item)
                else:
                    yield parser(None)
        else:
            raise Expection('This function only takes iterables!')


    def get_video_metadata(self, video_id, parser=P.parse_video_metadata):
        '''
        Given a single or list of `video_id` returns metrics (views, likes, comments) and metadata (description, category) as a dictionary.
        
        Read the docs: https://developers.google.com/youtube/v3/docs/videos/list

        :param video_id: (str or list of str) the ID of a video IE: ['kNbhUWLH_yY'], this can be found at the end of Youtube urls and by parsing links using `get_youtube_id()`
        :param parser: (func) the function to parse the json document.

        :returns: a list of dictionaries containing metadata.
        '''
        video_metadata = []
        if isinstance(video_id, str):
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/videos"
                             "?part=statistics,snippet"
                             "&id={}&key={}&maxResults=2".format(self.api_version, 
                                                                 video_id, self.key))
            response = requests.get(http_endpoint)
            response_json  = _load_response(response)
            if response_json.get('items'):
                video_metadata = parser(response_json['items'][0])

        elif isinstance(video_id, list) or isinstance(video_id, pd.Series):
            for video_meta in self.get_video_metadata_gen(video_id):
                video_metadata.append(video_meta)
        else:
            raise TypeError("Could not process the type entered!")

        return video_metadata


    def get_playlists(self, channel_id, next_page_token=False, 
                      parser=P.parse_playlist_metadata):
        '''
        Returns a list of playlist IDs that `channel_id` created.
        Note that playlists can contains videos from any users.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA

        :returns: list of dictionaries of playlist info that `channel_id` is subscribed to.
        '''
        parser=parser if parser else P.raw_json
        playlists = []
        while True:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/playlists"
                             "?part=id,snippet,contentDetails"
                             "&channelId={}&key={}&maxResults=50".format(self.api_version,
                                                                         channel_id, self.key))
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = _load_response(response)
            if response_json.get('items'):
                for item in response_json.get('items'):
                    playlists.append(parser(item))
                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    break
                    
        return playlists


    def get_videos_from_playlist_id(self, playlist_id, next_page_token=None,
                                    published_after=datetime.datetime(1990,1,1),
                                    parser=P.parse_video_url):
        '''
        Given a `playlist_id`, returns a list of `video_ids` associated with that playlist.
        Note that to user uploads are a playlist from channels.
        Typically this pattern is just the channel ID with UU subbed as the first two letters.
        You can access this using the function `get_upload_playlist_id`, or from the `playlist_id_likes`
        key returned from `get_channel_metadata`.

        :param playlist_id: (str) the playlist_id IE:UUaLfMkkHhSA_LaCta0BzyhQ
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA
        :param cutoff_date: (datetime) a date for the minimum publish date for videos from a playlist_id.
        :param parser: (func) the function to parse the json document

        :returns: a list dictionaries with video ids associated with `playlist_id`.
        '''
        parser=parser if parser else P.raw_json
        videos = []
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/playlistItems"
                             "?part=snippet&playlistId={}"
                             "&maxResults=50&key={}".format(self.api_version,
                                                            playlist_id, self.key))
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = _load_response(response)
            if response_json.get('items'):
                for item in response_json.get('items'):
                    publish_date = parse_yt_datetime(item['snippet'].get('publishedAt'))
                    if publish_date <= published_after:
                        run=False
                        break
                    videos.append(parser(item))
                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    run=False
                    break
                    
        return videos


    def get_subscriptions(self, channel_id, next_page_token=False, 
                          parser=P.parse_subscription_descriptive):
        '''
        Returns a list of channel IDs that `channel_id` is subscribed to.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA
        :param stop_after_n_iteration: (int) stops the API calls after N API calls
        :param parser: (func) the function to parse the json document

        :returns: subscription_ids (list) of channel IDs that `channel_id` is subscrbed to.
        '''
        parser=parser if parser else P.raw_json
        subscriptions = []
        while True:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/subscriptions"
                             "?channelId={}&part=id,snippet"
                             "&maxResults=50&key={}".format(self.api_version, 
                                                            channel_id, self.key))
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = _load_response(response)
            if response_json.get('items'):
                for item in response_json.get('items'):
                    subscriptions.append(parser(item))
                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    return subscriptions

        return subscriptions


    def get_featured_channels_gen(self, channel_id, parser=P.parse_featured_channels):
        '''
        Given a `channel_id` returns a dictionary {channel_id : [list, of, channel_ids]}
        of featured channels.

        Optionally, can take a list of channel IDS, and returns a list of dictionaries.
        
        Read the docs: https://developers.google.com/youtube/v3/docs/channels/list

        :param channel_id: (str or list) of channel_ids IE:['UCn8zNIfYAQNdrFRrr8oibKw']
        :param parser: (func) the function to parse the json document

        :returns: A dictionary of featured channels
        '''
        parser=parser if parser else P.raw_json
        if isinstance(channel_id, list):
            for chunk in _chunker(channel_id, 50):
                http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                                 "?part=id,brandingSettings"
                                 "&id={}&key={}".format(self.api_version, 
                                                        ','.join(chunk), self.key))
                response = requests.get(http_endpoint)
                response_json = _load_response(response)
                if response_json.get('items'):
                    for item in response_json['items']:
                        yield parser(item)
                else:
                    yield parser(None)

        else:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                             "?part=id,brandingSettings"
                             "&id={}&key={}".format(self.api_version, 
                                                    channel_id, self.key))

            response = requests.get(http_endpoint)
            response_json = _load_response(response)
            for item in response['items']:
                yield parser(item)


    def get_featured_channels(self, channel_id, **kwargs):
        '''
        Given a `channel_id` returns a dictionary {channel_id : [list, of, channel_ids]}
        of featured channels.

        Optionally, can take a list of channel IDs, and returns a list of dictionaries.

        :param channel_id: (str or list) of channel_ids IE:['UCn8zNIfYAQNdrFRrr8oibKw']
        :param parser: (func) the function to parse the json document

        :returns: A dictionary of featured channels
        '''
        featured_channels = []
        for channel in self.get_featured_channels_gen(channel_id, **kwargs):
            featured_channels.append(channel)
        return featured_channels

    
    def get_video_comments(self, video_id, get_replies=True,
                           max_results=None,
                           next_page_token=False, parser=P.parse_comment_metadata):
        """
        Returns a list of comments on a given video

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param get_replies: (bool) whether or not to get replies to comments
        :param cutoff_date: (datetime) a date for the minimum publish date for comments from a video_id.
        :param parser: (func) the function to parse the json document

        :returns: comments (list of dicts) of comments from the comments section on a given video_id
        """
        parser=parser if parser else P.raw_json
        comments = []
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/commentThreads?"
                             "part=snippet&textFormat=plainText&maxResults=100&"
                             "videoId={}&key={}".format(self.api_version, 
                                                        video_id, self.key))
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)
            response = requests.get(http_endpoint)
            response_json = _load_response(response)
            if response_json.get('items'):
                items = response_json.get('items')
                for item in items:
                    if max_results:
                        if len(comments) >= max_results:
                            return comments
                    comments.append(parser(item))

            if response_json.get('nextPageToken'):
                next_page_token = response_json['nextPageToken']
            else: 
                run=False
                break

        if get_replies:
            for comment in comments:
                if comment.get('reply_count') and comment.get('reply_count') > 0:
                    comment_id = comment.get('comment_id')
                    http_endpoint = ("https://www.googleapis.com/youtube/v{}/comments?"
                                 "part=snippet&textFormat=plainText&maxResults=100&"
                                 "parentId={}&key={}".format(self.api_version,
                                                             comment_id,
                                                             self.key))
                    response = requests.get(http_endpoint)
                    response_json = _load_response(response)
                    if response_json.get('items'):
                        for item in response_json.get('items'):
                            if max_results:
                                if len(comments) >= max_results:
                                    return comments
                            comments.append(parser(item))

        return comments


    def get_captions(self, video_id, lang_code='en', parser=P.parse_caption_track):
        """
        Grabs captions given a video id using the PyTube and BeautifulSoup Packages

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param lang_code: (str) language to get captions in
        :param parser: (func) the function to parse the json document

        :returns: the captions from a given video_id
        """
        def _get_captions(video_id, lang_code='en', parser=P.parse_caption_track):
            """
            Grabs captions given a video id using the PyTube and BeautifulSoup Packages

            :param video_id: (str) a vide_id IE: eqwPlwHSL_M
            :param lang_code: (str) language to get captions in
            :param parser: (func) the function to parse the json document

            :returns: the captions from a given video_id
            """
            url = get_url_from_video_id(video_id)
            vid = YouTube(url)
            captions = vid.captions.get_by_language_code(lang_code)

            resp = {}
            if captions:
                clean_cap = _text_from_html(captions.xml_captions)
                resp['caption'] = clean_cap
            else:
                resp['caption'] = None
            resp['video_id'] = video_id
            resp['collection_date'] = datetime.datetime.now()

            return resp
        
        if isinstance(video_id, str):
            captions = _get_captions(video_id, **kwargs)
        else:
            captions = []
            for v_id in video_id:
                captions.append(_get_captions(video_id, **kwargs))
        return captions

    
    def get_recommended_videos(self, video_id, max_results=5,
                               safe_search=None,
                               parser=P.parse_rec_video_metadata):
        """
        Get recommended videos given a video ID
        
        Read the docs: https://developers.google.com/youtube/v3/docs/search/list
        
        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param max_results: (int) max number of recommended vids
        :param parser: (func) the function to parse the json document


        :returns: a list of videos and video metadata for recommended videos

        """
        http_endpoint = ("https://www.googleapis.com/youtube/v{}/search?"
                         "part=snippet&type=video&maxResults={}&"
                         "relatedToVideoId={}&key={}".format(self.api_version,
                                                             max_results, 
                                                             video_id, 
                                                             self.key))
        parser=parser if parser else P.raw_json
        if safe_search:
            http_endpoint += '&safeSearch={}'.format(safe_search)
        response = requests.get(http_endpoint)
        response_json = _load_response(response)
        recommended_vids = []
        if response_json.get('items'):
            for item in response_json.get('items'):
                recommended_vids.append(parser(item))

        return recommended_vids

    
    def search(self, q, channel_id=None,
               max_results=5, order_by="relevance", next_page_token=None,
               published_after=datetime.datetime(2000,1,1),
               published_before=datetime.datetime(3000,1,1),
               location=None, location_radius='1km', 
               region_code=None, safe_search=None, 
               relevance_language=None, event_type=None,
               topic_id=None, video_duration=None,
               parser=P.parse_rec_video_metadata, search_type="video",
               exhaustive=False,
               verbose=False):
        """
        Search YouTube for either videos, channels for keywords. Only returns up to 500 videos per search. For an exhaustive search, take advantage of the ``published_after`` and ``published_before`` params. Note the docstring needs to be updated to account for all the arguments this function takes.
        
        Read the docs: https://developers.google.com/youtube/v3/docs/search/list

        :param q: (list or str) regex pattern to search using | for or, && for and, and - for not.
        :param max_results: (int) max number of recommended vids
        :param parser: (func) the function to parse the json document
        

        :returns: a list of videos and video metadata for recommended videos

        """
        if search_type not in ["video", "channel", "playlist"]:
            raise Exception("The value you have entered for `type` is not valid!")
            
        parser=parser if parser else P.raw_json
        videos = []
        while True:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/search?"
                             "part=snippet&type={}&maxResults=50"
                             "&order={}&key={}".format(self.api_version, search_type, 
                                                       order_by, self.key))
            if q:
                if isinstance(q, list):
                    q = '|'.join(q)
                http_endpoint += "&q={}".format(q)
            
            if published_after:
                if not isinstance(published_after, datetime.date):
                    raise Exception("published_after must be a datetime, not a {}".format(type(published_after)))
                _published_after = datetime.datetime.strftime(published_after, "%Y-%m-%dT%H:%M:%SZ")
                http_endpoint += "&publishedAfter={}".format(_published_after)
            
            if published_before:
                if not isinstance(published_before, datetime.date):
                    raise Exception("published_before must be a datetime, not a {}".format(type(published_before)))
                _published_before = datetime.datetime.strftime(published_before, "%Y-%m-%dT%H:%M:%SZ")
                http_endpoint += "&publishedBefore={}".format(_published_before)
            
            if channel_id:
                http_endpoint += "&channelId={}".format(channel_id)
            
            if location:
                if isinstance(location, tuple):
                    location = urllib.parse.quote_plus(str(location).strip('()').replace(' ', ''))
                http_endpoint += "&location={}&locationRadius={}".format(location, 
                                                                         location_radius)
            if region_code:
                http_endpoint += "&regionCode={}".format(region_code) 
            
            if safe_search:
                if not safe_search in ['moderate', 'strict', 'none']:
                    raise "Not proper safe_search."
                http_endpoint += '&safeSearch={}'.format(safe_search)
            
            if relevance_language:
                http_endpoint += '&relevanceLanguage={}'.format(relevance_language)
            
            if event_type:
                if not event_type in ['completed', 'live', 'upcoming']:
                    raise "Not proper event_type!"
                http_endpoint += '&eventType={}'.format(event_type)
            
            if topic_id:
                http_endpoint += '&topicId={}'.format(topic_id)
                
            if video_duration:
                if not video_duration in ['short', 'long', 'medium', 'any']:
                    raise "Not proper video_duration"
                http_endpoint += '&videoDuration={}'.format(video_duration)
           
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = _load_response(response)
            if response_json.get('items'):
                for item in response_json.get('items'):
                    videos.append(parser(item))
                if max_results:
                    if len(videos) >= max_results:
                        videos = videos[:max_results]
                        break
                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                    time.sleep(.1)
                else:
                    break
            else:
                break

        return videos
