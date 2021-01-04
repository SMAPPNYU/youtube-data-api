import sys
import time
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import datetime
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import pandas as pd

from youtube_api.youtube_api_utils import (
    _load_response,
    parse_yt_datetime,
    _chunker,
)
import youtube_api.parsers as P

"""
This script has the YouTubeDataAPI class and functions for the API's endpoints.
"""

__all__ = ['YoutubeDataApi', 'YouTubeDataAPI']

class YouTubeDataAPI:
    """
    The Youtube Data API handles the keys and methods to access data from the YouTube Data API

     :param key: YouTube Data API key. Get a YouTube Data API key here: https://console.cloud.google.com/apis/dashboard
    """
    def __init__(
        self, key, api_version='3', verify_api_key=True, verbose=False, timeout=20
    ):
        """
        :param key: YouTube Data API key
        Get a YouTube Data API key here: https://console.cloud.google.com/apis/dashboard
        """
        self.key = key
        self.api_version = int(api_version)
        self.verbose = verbose
        self._timeout = timeout

        # check API Key
        if not self.key:
            raise ValueError('No API key used to initate the class.')
        if verify_api_key and not self.verify_key():
            raise ValueError('The API Key is invalid')

        # creates a requests sessions for API calls.
        self._create_session()


    def verify_key(self):
        '''
        Checks it the API key is valid.

        :returns: True if the API key is valid, False if the key is not valid.
        :rtype: bool
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


    def _create_session(self, max_retries=2, backoff_factor=.5, status_forcelist=[500, 502, 503, 504], **kwargs):
        '''
        Creates a requests session to retry API calls when any `status_forcelist` codes are returned.

        :param max_retries: How many times to retry an HTTP request (API call) when a `status_forcelist` code is returned
        :type max_retries: int
        :param backoff_factor: How long to wait between retrying API calls. Scales exponentially.
        :type backoff_factor: float
        :param status_forcelist: Retry when any of these http response codes are returned.
        :type status_forcelist: list
        '''
        session = requests.Session()
        retries = Retry(total=max_retries,
                        backoff_factor=backoff_factor,
                        status_forcelist=status_forcelist,
                        **kwargs)
        session.mount('http://', HTTPAdapter(max_retries=retries))
        self.session = session

    def _http_request(self, http_endpoint, timeout_in_n_seconds=False):
        '''
        A wrapper function for making an http request to the YouTube Data API.
        Will print the `http_endpoint` if the YouTubeDataAPI class is instantiated with verbose = True.
        Attempts to load the response of the http request,
        and returns json response.
        '''
        if self.verbose:
            # Print the Http req and replace the API key with a placeholder
            print(http_endpoint.replace(self.key, '{API_KEY_PLACEHOLDER}'))
        response = self.session.get(http_endpoint, timeout=self._timeout)
        response_json = _load_response(response)
        return response_json

    def get_channel_id_from_user(self, username, **kwargs):
        """
        Get a channel_id from a YouTube username. These are the unique identifiers for all YouTube "uers". IE. "Munchies" -> "UCaLfMkkHhSA_LaCta0BzyhQ".

        Read the docs: https://developers.google.com/youtube/v3/docs/channels/list

        :param username: the username for a YouTube channel
        :type username: str

        :returns: YouTube Channel ID for a given username
        :rtype: str
        """
        http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                         "?part=id"
                         "&forUsername={}&key={}".format(self.api_version,
                                                         username, self.key))
        for k,v in kwargs.items():
            http_endpoint += '&{}={}'.format(k, v)
        response_json = self._http_request(http_endpoint)
        channel_id = None
        if response_json.get('items'):
            channel_id = response_json['items'][0]['id']
        return channel_id


    def get_channel_metadata_gen(self, channel_id, parser=P.parse_channel_metadata,
                                 part=["id", "snippet", "contentDetails", "statistics",
                                       "topicDetails", "brandingSettings"],
                                **kwargs):
        '''
        Gets a dictionary of channel metadata given a channel_id, or a list of channel_ids.

        :param channel_id:  channel id(s)
        :type channel_id: str or list
        :param parser: the function to parse the json document.
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: yields the YouTube channel metadata
        :rtype: dict
        '''
        parser=parser if parser else P.raw_json
        part = ','.join(part)
        if isinstance(channel_id, list) or isinstance(channel_id, pd.Series):
            for chunk in _chunker(channel_id, 50):
                id_input = ','.join(chunk)
                http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels?"
                                "part={}&id={}&key={}&maxResults=50".format(
                                    self.api_version, part, id_input, self.key))
                for k,v in kwargs.items():
                    http_endpoint += '&{}={}'.format(k, v)
                response_json = self._http_request(http_endpoint)
                if response_json.get('items'):
                    for item in response_json['items']:
                        yield parser(item)
                else:
                    yield parser(None)


    def get_channel_metadata(self, channel_id, parser=P.parse_channel_metadata,
                             part=["id", "snippet", "contentDetails", "statistics",
                                   "topicDetails", "brandingSettings"],  **kwargs):
        '''
        Gets a dictionary of channel metadata given a channel_id, or a list of channel_ids.

        Read the docs: https://developers.google.com/youtube/v3/docs/channels/list

        :param channel_id: the channel id(s)
        :type channel_id: str or list
        :param parser: the function to parse the json document.
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: the YouTube channel metadata
        :rtype: dict
        '''
        parser=parser if parser else P.raw_json
        channel_meta = []
        if isinstance(channel_id, str):
            part = ','.join(part)
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels?"
                             "part={}&id={}&key={}&maxResults=50".format(
                                 self.api_version, part, channel_id, self.key))
            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)
            response_json = self._http_request(http_endpoint)
            if response_json.get('items'):
                channel_meta = parser(response_json['items'][0])

        elif isinstance(channel_id, list) or isinstance(channel_id, pd.Series):
            for channel_meta_ in self.get_channel_metadata_gen(channel_id,
                                                               parser=parser,
                                                               part=part,
                                                               **kwargs):
                channel_meta.append(channel_meta_)
        else:
            raise TypeError("Could not process the type entered!")

        return channel_meta


    def get_video_metadata_gen(self, video_id, parser=P.parse_video_metadata,
                               part=['statistics','snippet'],  **kwargs):
        '''
        Given a `video_id` returns metrics (views, likes, comments) and metadata (description, category) as a dictionary.

        Read the docs: https://developers.google.com/youtube/v3/docs/videos/list

        :param video_id: The ID of a video IE: "kNbhUWLH_yY", this can be found at the end of YouTube urls and by parsing links using :meth:`youtube_api.youtube_api_utils.strip_youtube_id`.
        :type video_id: str or list of str
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: returns metadata from the inputted ``video_id``s.
        :rtype: dict
        '''
        part = ','.join(part)
        parser=parser if parser else P.raw_json
        if isinstance(video_id, list) or isinstance(video_id, pd.Series):
            for chunk in _chunker(video_id, 50):
                id_input = ','.join(chunk)
                http_endpoint = ("https://www.googleapis.com/youtube/v{}/videos"
                                 "?part={}"
                                 "&id={}&key={}&maxResults=50".format(
                                    self.api_version, part, id_input, self.key))
                for k,v in kwargs.items():
                    http_endpoint += '&{}={}'.format(k, v)
                response_json = self._http_request(http_endpoint)
                if response_json.get('items'):
                    for item in response_json['items']:
                        yield parser(item)
                else:
                    yield parser(None)
        else:
            raise Exception('This function only takes iterables!')


    def get_video_metadata(self, video_id, parser=P.parse_video_metadata, part=['statistics','snippet'],  **kwargs):
        '''
        Given a single or list of `video_id` returns metrics (views, likes, comments) and metadata (description, category) as a dictionary.

        Read the docs: https://developers.google.com/youtube/v3/docs/videos/list

        :param video_id:  the ID of a video IE: ['kNbhUWLH_yY'], this can be found at the end of YouTube urls and by parsing links using :meth:`youtube_api.youtube_api_utils.strip_youtube_id`.
        :type video_id: str or list of str
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: yields a video metadata.
        :rtype: dict
        '''
        video_metadata = []
        parser=parser if parser else P.raw_json
        if isinstance(video_id, str):
            part = ','.join(part)
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/videos"
                             "?part={}"
                             "&id={}&key={}&maxResults=2".format(self.api_version,
                                                                 part, video_id,
                                                                 self.key))
            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)
            response_json = self._http_request(http_endpoint)
            if response_json.get('items'):
                video_metadata = parser(response_json['items'][0])

        elif isinstance(video_id, list) or isinstance(video_id, pd.Series):
            for video_meta in self.get_video_metadata_gen(video_id,
                                                          parser=parser,
                                                          part=part,
                                                          **kwargs):
                video_metadata.append(video_meta)
        else:
            raise TypeError("Could not process the type entered!")

        return video_metadata


    def get_playlists(self, channel_id, next_page_token=False, parser=P.parse_playlist_metadata,
                      part=['id','snippet','contentDetails'], **kwargs):
        '''
        Returns a list of playlist IDs that `channel_id` created.
        Note that playlists can contains videos from any users.

        Read the docs: https://developers.google.com/youtube/v3/docs/playlists/list

        :param channel_id: a channel_id IE: "UCn8zNIfYAQNdrFRrr8oibKw"
        :type channel_id: str
        :param next_page_token: a token to continue from a preciously stopped query IE: "CDIQAA"
        :type next_page_token: str

        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: playlist info that ``channel_id`` is subscribed to.
        :rtype: list of dict
        '''
        parser=parser if parser else P.raw_json
        part = ','.join(part)
        playlists = []
        while True:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/playlists"
                             "?part={}&channelId={}&key={}&maxResults=50".format(
                                 self.api_version, part, channel_id, self.key))
            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)
            response_json = self._http_request(http_endpoint)
            if response_json.get('items'):
                for item in response_json.get('items'):
                    playlists.append(parser(item))
                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    break

        return playlists


    def get_videos_from_playlist_id(self, playlist_id, next_page_token=None,
                                    parser=P.parse_video_url, part=['snippet'], max_results=200000,
                                    **kwargs):
        '''
        Given a `playlist_id`, returns `video_ids` associated with that playlist.

        Note that user uploads for any given channel are from a playlist named "upload playlist id". You can get this value using :meth:`youtube_api.youtube_api.get_channel_metadata` or :meth:`youtube_api.youtube_api_utils.get_upload_playlist_id`. The playlist ID for uploads is always the channel_id with "UU" subbed for "UC".

        Read the docs: https://developers.google.com/youtube/v3/docs/playlistItems

        :param playlist_id: the playlist_id IE: "UUaLfMkkHhSA_LaCta0BzyhQ"
        :type platlist_id: str
        :param next_page_token: a token to continue from a preciously stopped query IE: "CDIQAA"
        :type next_page_token: str
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list
        :param max_results: How many video IDs should returned? Contrary to the name, this is actually the minimum number of results to be returned.
        :type mac_results: int
        
        :returns: video ids associated with ``playlist_id``.
        :rtype: list of dict
        '''
        parser=parser if parser else P.raw_json
        part = ','.join(part)
        videos = []
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/playlistItems"
                             "?part={}&playlistId={}&maxResults=50&key={}".format(
                                 self.api_version, part, playlist_id, self.key))
            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response_json = self._http_request(http_endpoint,
                                               timeout_in_n_seconds=20  )
            if response_json.get('items'):
                for item in response_json.get('items'):
                    videos.append(parser(item))
                    if len(videos) >= max_results:
                        run = False
                        break
                        
                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    run=False
                    break
            else:
                run=False
                break

        return videos


    def get_subscriptions(self, channel_id, next_page_token=False,
                          parser=P.parse_subscription_descriptive,
                          part=['id', 'snippet'], **kwargs):
        '''
        Returns a list of channel IDs that `channel_id` is subscribed to.

        Read the docs: https://developers.google.com/youtube/v3/docs/subscriptions

        :param channel_id: a channel_id IE: "UCn8zNIfYAQNdrFRrr8oibKw"
        :type channel_id: str
        :param next_page_token: a token to continue from a preciously stopped query IE: "CDIQAA"
        :type next_page_token: str
        :param stop_after_n_iteration: stops the API calls after N API calls
        :type stop_after_n_iteration: int
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: channel IDs that ``channel_id`` is subscribed to.
        :rtype: list
        '''
        parser=parser if parser else P.raw_json
        part = ','.join(part)
        subscriptions = []
        while True:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/subscriptions"
                             "?channelId={}&part={}&maxResults=50&key={}".format(
                                 self.api_version, channel_id, part, self.key))
            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response_json = self._http_request(http_endpoint)
            if response_json.get('items'):
                for item in response_json.get('items'):
                    subscriptions.append(parser(item))
                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    return subscriptions

        return subscriptions


    def get_featured_channels_gen(self, channel_id, parser=P.parse_featured_channels,
                                  part=["id", "brandingSettings"], **kwargs):
        '''
        Given a `channel_id` returns a dictionary {channel_id : [list, of, channel_ids]}
        of featured channels.

        Optionally, can take a list of channel IDS, and returns a list of dictionaries.

        Read the docs: https://developers.google.com/youtube/v3/docs/channels/list

        :param channel_id: channel_ids IE: ['UCn8zNIfYAQNdrFRrr8oibKw']
        :type channel_id: str of list of str
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: yields metadata for featured channels
        :rtype: dict
        '''
        parser = parser if parser else P.raw_json
        part = ','.join(part)
        if isinstance(channel_id, list):
            for chunk in _chunker(channel_id, 50):
                id_input = ','.join(chunk)
                http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                                 "?part={}&id={}&key={}".format(
                                     self.api_version, part, id_input, self.key))
                for k,v in kwargs.items():
                    http_endpoint += '&{}={}'.format(k, v)
                response_json = self._http_request(http_endpoint)
                if response_json.get('items'):
                    for item in response_json['items']:
                        yield parser(item)
                else:
                    yield parser(None)

        else:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                             "?part={}&id={}&key={}".format(
                                 self.api_version, part, channel_id, self.key))
            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)
            response = self.session.get(http_endpoint)
            response_json = _load_response(response)
            for item in response_json['items']:
                yield parser(item)


    def get_featured_channels(self, channel_id, parser=P.parse_featured_channels, **kwargs):
        '''
        Given a `channel_id` returns a dictionary {channel_id : [list, of, channel_ids]}
        of featured channels.

        Optionally, can take a list of channel IDs, and returns a list of dictionaries.

        Read the docs: https://developers.google.com/youtube/v3/docs/channels/list


        :param channel_id: channel_ids IE:['UCn8zNIfYAQNdrFRrr8oibKw']
        :type channel_id: str or list of str
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: metadata for featured channels from ``channel_id``.
        :rtype: list of dict
        '''
        featured_channels = []
        for channel in self.get_featured_channels_gen(channel_id, parser=parser, **kwargs):
            featured_channels.append(channel)
        return featured_channels


    def get_video_comments(self, video_id, get_replies=True,
                           max_results=None, next_page_token=False,
                           parser=P.parse_comment_metadata, part = ['snippet'],
                           **kwargs):
        """
        Returns comments and replies to comments for a given video.

        Read the docs: https://developers.google.com/youtube/v3/docs/commentThreads/list


        :param video_id: a video_id IE: "eqwPlwHSL_M"
        :type video_id: str
        :param get_replies: whether or not to get replies to comments
        :type get_replies: bool
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list

        :returns: comments and responses to comments of the given ``video_id``.
        :rtype: list of dict
        """
        parser=parser if parser else P.raw_json
        part = ','.join(part)
        comments = []
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/commentThreads?"
                             "part={}&textFormat=plainText&maxResults=100&"
                             "videoId={}&key={}".format(
                                 self.api_version, part, video_id, self.key))
            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)
            response = self.session.get(http_endpoint)
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
                                     "part={}&textFormat=plainText&maxResults=100&"
                                     "parentId={}&key={}".format(
                                         self.api_version, part, comment_id, self.key))
                    for k,v in kwargs.items():
                        http_endpoint += '&{}={}'.format(k, v)
                    response_json = self._http_request(http_endpoint)
                    if response_json.get('items'):
                        for item in response_json.get('items'):
                            if max_results:
                                if len(comments) >= max_results:
                                    return comments
                            comments.append(parser(item))
        return comments

    def search(self, q=None, channel_id=None,
               max_results=5, order_by="relevance", next_page_token=None,
               published_after=datetime.datetime.timestamp(datetime.datetime(2000,1,1)),
               published_before=datetime.datetime.timestamp(
                   datetime.datetime((3000 if sys.maxsize > 2**31 else 2038),1,1)),
               location=None, location_radius='1km', region_code=None,
               safe_search=None, relevance_language=None, event_type=None,
               topic_id=None, video_duration=None, search_type="video",
               parser=P.parse_rec_video_metadata, part=['snippet'],
               **kwargs):
        """
        Search YouTube for either videos, channels for keywords. Only returns up to 500 videos per search. For an exhaustive search, take advantage of the ``published_after`` and ``published_before`` params. Note the docstring needs to be updated to account for all the arguments this function takes.

        Read the docs: https://developers.google.com/youtube/v3/docs/search/list

        :param q: regex pattern to search using | for or, && for and, and - for not. IE boat|fishing is boat or fishing
        :type q: list or str
        :param max_results: max number of videos returned by a search query.
        :type max_results: int
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :param part: The part parameter specifies a comma-separated list of one or more resource properties that the API response will include. Different parameters cost different quota costs from the API.
        :type part: list
        :param order_by: Return search results ordered by either ``relevance``, ``date``, ``rating``, ``title``, ``videoCount``, ``viewCount``.
        :type order_by: str
        :param next_page_token: A token to continue from a preciously stopped query IE:CDIQAA
        :type next_page_token: str
        :param published_after: Only show videos uploaded after datetime
        :type published_after: datetime
        :param published_before: Only show videos uploaded before datetime
        :type published_before: datetime
        :param location: Coodinates of video uploaded in location.
        :type location: tuple
        :param location_radius: The radius from the ``location`` param to include in the search.
        :type location_radius: str
        :param region_code: search results for videos that can be viewed in the specified country. The parameter value is an ISO 3166-1 alpha-2 country code.
        :type region_code: str
        :param safe_search: whether or not to include restricted content, options are "moderate", "strict", None.
        :type safe_search: str or None
        :param relevance_language: Instructs the API to return search results that are most relevant to the specified language.
        :type relevance_language: str
        :param event_type: whether the video is "live", "completed", or "upcoming".
        :type event_type: str
        :param topic_id: only contain resources associated with the specified topic. The value identifies a Freebase topic ID.
        :type topic_id: str
        :param video_duration: filter on video durations "any", "long", "medium", "short".
        :type video_duration: str
        :param search_type: return results on a "video", "channel", or "playlist" search.

        :returns: incomplete video metadata of videos returned by search query.
        :rtype: list of dict
        """
        if search_type not in ["video", "channel", "playlist"]:
            raise Exception("The value you have entered for `type` is not valid!")

        parser=parser if parser else P.raw_json
        part = ','.join(part)
        videos = []
        while True:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/search?"
                             "part={}&type={}&maxResults=50"
                             "&order={}&key={}".format(
                                 self.api_version, part, search_type, order_by, self.key))
            if q:
                if isinstance(q, list):
                    q = '|'.join(q)
                http_endpoint += "&q={}".format(q)

            if published_after:
                if not isinstance(published_after, float) and not isinstance(published_after, datetime.date):
                    raise Exception("published_after must be a timestamp, not a {}".format(type(published_after)))
                
                if isinstance(published_after, float):
                    published_after = datetime.datetime.utcfromtimestamp(published_after)
                _published_after = datetime.datetime.strftime(published_after, "%Y-%m-%dT%H:%M:%SZ")
                http_endpoint += "&publishedAfter={}".format(_published_after)

            if published_before:
                if not isinstance(published_before, float) and not isinstance(published_before, datetime.date):
                    raise Exception("published_before must be a timestamp, not a {}".format(type(published_before)))
                    
                if isinstance(published_before, float):
                    published_before = datetime.datetime.utcfromtimestamp(published_before)
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

            for k,v in kwargs.items():
                http_endpoint += '&{}={}'.format(k, v)

            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response_json = self._http_request(http_endpoint)
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


    def get_recommended_videos(self, video_id, max_results=5,
                               parser=P.parse_rec_video_metadata,
                               **kwargs):
        """
        Get recommended videos given a video ID. This extends the search API.
        Note that search history does not influence results.

        Read the docs: https://developers.google.com/youtube/v3/docs/search/list

        :param video_id: (str) a video_id IE: "eqwPlwHSL_M"
        :param max_results: (int) max number of recommended vids
        :param parser: the function to parse the json document
        :type parser: :mod:`youtube_api.parsers module`
        :returns: incomplete video metadata from recommended videos of ``video_id``.
        :rtype: list of dict
        """

        return self.search(relatedToVideoId=video_id, order_by='relevance')

    
class YoutubeDataApi(YouTubeDataAPI):
    """Variant case of the main YouTubeDataAPI class. This class will de depricated by version 0.0.21"""
    def __init__(self, key, **kwargs):
        super().__init__(key, **kwargs)