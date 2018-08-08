import time
import requests
import datetime
from collections import OrderedDict
from pytube import YouTube

# fix importing errors
from youtube_api.youtube_api_utils import *
import youtube_api.parsers as P

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
        if self.verify_key():
            pass
        else:
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

        :param username: the username for a YouTube channel
        :type username: str

        :returns: the YouTube channel id for the given username
        """
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/channels/list'.format(self.api_version)

        def _get_channel_id_from_user(self, username):
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                             "?part=id"
                             "&forUsername={}&key={}".format(self.api_version, username, self.key))
            response = requests.get(http_endpoint)
            response_json = _load_response(response)
            if response_json.get('items'):
                channel_id = response_json['items'][0]['id']
                return channel_id


        if isinstance(username, list):
            channel_ids = []
            for username_ in username:
                channel_ids_ = _get_channel_id_from_user(username_)
                channel_ids.append(channel_ids_)

        elif isinstance(username, str):
            channel_ids = _get_channel_id_from_user(username)

        return channel_ids

        # TODO: catch error for not founded username
        else:
            raise Exception(_error_message(response, self.key, api_doc_point))


    def get_video_metadata_gen(self, video_id, parser=P.parse_video_metadata):
        '''
        Given a `video_id` returns metrics (views, likes, comments) and metadata (description, category) as a dictionary.

        :param video_id: (str or list of str) the ID of a video IE:['kNbhUWLH_yY'], this can be found at the end of Youtube urls and by parsing links using `get_youtube_id()`
        :param key: (str) the API key to the Youtube Data API.
        :param parser: (func) the function to parse the json document

        :returns: a list of dictionaries containing metadata.
        '''
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/videos/list'.format(self.api_version)
        if isinstance(video_id, list):
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
                        video_meta = parser(item)
                        yield video_meta_
        else:
            raise Expection('This function only takes iterables!')


    def get_video_metadata(self, video_id, parser=P.parse_video_metadata):
        '''
        Given a single or list of `video_id` returns metrics (views, likes, comments) and metadata (description, category) as a dictionary.

        :param video_id: (str or list of str) the ID of a video IE: ['kNbhUWLH_yY'], this can be found at the end of Youtube urls and by parsing links using `get_youtube_id()`
        :param key: (str) the API key to the Youtube Data API.
        :param parser: (func) the function to parse the json document.

        :returns: a list of dictionaries containing metadata.
        '''
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/videos/list'.format(self.api_version)

        if isinstance(video_id, str):
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/videos"
                             "?part=statistics,snippet"
                             "&id={}&key={}&maxResults=2".format(
                                 self.api_version, video_id, self.key))
            response = requests.get(http_endpoint)
            response_json  = _load_response(response)

            if response_json.get('items'):
                video_metadata = parser(response_json['items'][0])

        else: # iterable
            video_metadata = []
            for video_meta in self.get_video_metadata_gen(video_id):
                video_metadata.append(video_meta)

        return video_metadata


    def get_playlists_gen(self, channel_id, next_page_token=False,
                      parser=P.parse_playlist_metadata):
        '''
        Returns a list of playlist IDs that `channel_id` created.
        Note that playlists can contains videos from any users.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA

        :returns: yields generator of dictionaries of playlist info that `channel_id` is subscribed to.
        '''
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/playlistItems/list'.format(self.api_version)
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/playlists"
                             "?part=id,snippet,contentDetails"
                             "&channelId={}&key={}&maxResults=50".format(self.api_version, channel_id, self.key))
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = load_response(response)

            if response_json.get('items'):
                for item in response_json.get('items'):
                    playlist_meta = parser(item)
                    yield playlist_meta

                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    run = False
            else:
                raise Exception(_error_message(response, self.key, api_doc_point))


    def get_playlists(self, channel_id, **kwargs):
        '''
        Returns a list of playlist IDs that `channel_id` created.
        Note that playlists can contains videos from any users.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA

        :returns: list of dictionaries of playlist info that `channel_id` is subscribed to.
        '''
        playlists = []
        for playlist in self.get_playlists_gen(channel_id, **kwargs):
            playlists.append(playlist)
        return playlists


    def get_videos_from_playlist_id_gen(self, playlist_id, next_page_token=False,
                                        cutoff_date=datetime.datetime(1990,1,1),
                                        parser=P.parse_video_url):
        '''
        Given a `playlist_id`, returns a generator of `video_ids` associated with that playlist.
        Note that to user uploads are a playlist from channels.
        Typically this pattern is just the channel ID with UU subbed as the first two letters.
        You can access this using the function `get_upload_playlist_id`, or from the `playlist_id_likes`
        key returned from `get_channel_metadata`.

        :param playlist_id: (str) the playlist_id IE:UUaLfMkkHhSA_LaCta0BzyhQ
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA
        :param cutoff_date: (datetime) a date for the minimum publish date for videos from a playlist_id.
        :param parser: (func) the function to parse the json document

        :returns: a generator of video ids associated with `playlist_id`.
        '''
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/playlistItems/list'.format(self.api_version)
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/playlistItems"
                             "?part=snippet&playlistId={}"
                             "&maxResults=50&key={}".format(self.api_version, playlist_id, self.key))

            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = load_response(response)

            if response_json.get('items'):
                for item in response_json.get('items'):
                    publish_date = parse_yt_datetime(item['snippet'].get('publishedAt'))
                    if publish_date <= cutoff_date:
                        run = False
                        break
                    v_id = parser(item)
                    yield v_id

                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    run = False
                time.sleep(.1)

            else:
                raise Exception(_error_message(response, self.key, api_doc_point))


    def get_videos_from_playlist_id(self, playlist_id, **kwargs):
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
        output = []
        for playlist_id in self.get_videos_from_playlist_id_gen(playlist_id, **kwargs):
            output.append(playlist_id)
        return output


    def get_subscriptions_gen(self, channel_id, next_page_token=False,
                             parser = P.parse_subscription_descriptive):
        '''
        Returns a list of channel IDs that `channel_id` is subscribed to.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA
        :param parser: (func) the function to parse the json document

        :returns: subscription_ids (list) of channel IDs that `channel_id` is subscirbed to.
        '''
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/subscriptions/list'.format(self.api_version)
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/subscriptions"
                             "?channelId={}&part=id,snippet"
                             "&maxResults=50&key={}".format(self.api_version, channel_id, self.key))

            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = load_response(response, verbose, handle_error)

            if response_json.get('items'):
                for item in response_json.get('items'):
                    sub_meta = parser(item)
                    yield sub_meta

                if response_json.get('nextPageToken'):
                    next_page_token = response_json.get('nextPageToken')
                else:
                    run = False
            else:
                raise Exception(_error_message(response, self.key, api_doc_point))
            time.sleep(.1)


    def get_subscriptions(self, channel_id, **kwargs):
        '''
        Returns a list of channel IDs that `channel_id` is subscribed to.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA
        :param stop_after_n_iteration: (int) stops the API calls after N API calls
        :param parser: (func) the function to parse the json document

        :returns: subscription_ids (list) of channel IDs that `channel_id` is subscrbed to.
        '''
        subscriptions = []
        for sub in self.get_subscriptions_gen(channel_id, **kwargs):
            subscriptions.append(sub)
        return subscriptions


    def get_featured_channels_gen(self, channel_id, verbose=1, parser=P.parse_featured_channels, handle_error=True):
        '''
        Given a `channel_id` returns a dictionary {channel_id : [list, of, channel_ids]}
        of featured channels.

        Optionally, can take a list of channel IDS, and returns a list of dictionaries.

        :param channel_id: (str or list) of channel_ids IE:['UCn8zNIfYAQNdrFRrr8oibKw']
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: A dictionary of featured channels
        '''
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/channels/list'.format(self.api_version)
        if isinstance(channel_id, list):
            for chunk in _chunker(channel_id, 50):
                id_input = ','.join(chunk)

                http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                                 "?part=id,brandingSettings"
                                 "&id={}&key={}".format(self.api_version, id_input, self.key))

                response = requests.get(http_endpoint)
                response_json = _load_response(response)

                if response_json.get('items'):
                    for item in response_json['items']:
                        feat_channel_ = parser(item)

                        yield feat_channel_

                else:
                    raise Exception(_error_message(response, self.key, api_doc_point))

        else:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/channels"
                             "?part=id,brandingSettings"
                             "&id={}&key={}".format(self.api_version, channel_id, self.key))

            response = requests.get(http_endpoint)
            response_json = _load_response(response)

            for item in response['items']:
                feat_channels = parser(item)

                yield feat_channel_


    def get_featured_channels(self, channel_id, **kwargs):
        '''
        Given a `channel_id` returns a dictionary {channel_id : [list, of, channel_ids]}
        of featured channels.

        Optionally, can take a list of channel IDs, and returns a list of dictionaries.

        :param channel_id: (str or list) of channel_ids IE:['UCn8zNIfYAQNdrFRrr8oibKw']
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: A dictionary of featured channels
        '''
        featured_channels = []
        for channel in self.get_featured_channels_gen(channel_id, **kwargs):
            featured_channels.append(channel)
        return featured_channels


    def get_video_comments_gen(self, video_id, get_replies=True,
                               cutoff_date=datetime.datetime(1990,1,1),
                               next_page_token=False, parser=P.parse_comment_metadata):
        """
        Returns a list of comments on a given video

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param get_replies: (bool) whether or not to get replies to comments
        :param cutoff_date: (datetime) a date for the minimum publish date for comments from a video_id.
        :param parser: (func) the function to parse the json document

        :returns: comments (list of dicts) of comments from the comments section on a given video_id
        """
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/commentThreads/list'.format(self.api_version)

        comments = []
        run = True

        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v{}/commentThreads?"
                             "part=snippet&textFormat=plainText&maxResults=100&"
                             "videoId={}&key={}".format(self.api_version, video_id,self.key))
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = _load_response(response)

            if response_json.get('items'):
                for item in response_json.get('items'):
                    publish_date = parse_yt_datetime(item['snippet'].get('publishedAt'))
                    if publish_date <= cutoff_date:
                        run = False
                        break
                    comment_ = parser(item)
                    yield comment_
            else:
                raise Exception(_error_message(response, self.key, api_doc_point))

            if response.get('nextPageToken'):
                next_page_token = response_json['nextPageToken']
            else:
                run = False
            time.sleep(0.1)


        if get_replies:
            api_doc_point = 'https://developers.google.com/youtube/v{}/docs/comments/list'.format(self.api_version)

            for comment in comments:
                if comment.get('reply_count') and comment.get('reply_count') > 0:
                    comment_id = comment.get('comment_id')
                    http_endpoint = ("https://www.googleapis.com/youtube/v{}/comments?"
                                 "part=snippet&textFormat=plainText&maxResults=100&"
                                 "parentId={}&key={}".format(self.api_version, comment_id,self.key))
                    response = requests.get(http_endpoint)
                    response_json = _load_response(response)

                    if response_json.get('items'):
                        for comment in response_json.get('items'):
                            comment_ = parser(comment)
                            yield comment_
                    else:
                        raise Exception(_error_message(response, self.key, api_doc_point))
                    time.sleep(0.1)



    def get_video_comments(self, video_id, get_replies=True,
                           cutoff_date=datetime.datetime(1990,1,1),
                           next_page_token=False, parser=P.parse_comment_metadata):
        """
        Returns a list of comments on a given video

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param get_replies: (bool) whether or not to get replies to comments
        :param cutoff_date: (datetime) a date for the minimum publish date for comments from a video_id.
        :param parser: (func) the function to parse the json document

        :returns: comments (list of dicts) of comments from the comments section on a given video_id
        """
        comments = []
        for comment in self.get_video_comments_gen(video_id, **kwargs):
            comments.append(comment)
        return comments


    def _get_captions(self, video_id, lang_code='en', parser=P.parse_caption_track):
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
            resp['video_id'] = video_id
            resp['collection_date'] = datetime.datetime.now()

        else:
            raise Exception(_caption_error_message(captions))

        return resp

    def get_captions(self, video_id, **kwargs):
        """
        Grabs captions given a video id using the PyTube and BeautifulSoup Packages

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param lang_code: (str) language to get captions in
        :param parser: (func) the function to parse the json document

        :returns: the captions from a given video_id
        """
        if isinstance(video_id, str):
            captions = self._get_captions(video_id, **kwargs)
        else:
            captions = []
            for v_id in video_id:
                captions.append(self._get_captions(video_id, **kwargs))
        return captions

    def get_recommended_videos(self, video_id, max_results=25,
                               parser=P.parse_rec_video_metadata):
        """
        Grabs captions given a video id using the PyTube and BeautifulSoup Packages

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param max_results: (int) max number of recommended vids
        :param parser: (func) the function to parse the json document


        :returns: a list of videos and video metadata for recommended videos

        """
        api_doc_point = 'https://developers.google.com/youtube/v{}/docs/search/list'.format(self.api_version)

        if not isinstance(video_id, str):
            raise Exception("Only string values permitted")

        http_endpoint = ("https://www.googleapis.com/youtube/v{}/search?"
                         "part=snippet&type=video&maxResults={}&"
                         "relatedToVideoId={}&key={}".format(self.api_version,
                            max_results, video_id, self.key))

        recommended_vids = []
        response = requests.get(http_endpoint)
        response_json = _load_response(response)

        if response_json.get('items'):
            for item in response_json.get('items'):
                item_ = parser(item)
                recommended_vids.append(item_)
        else:
            raise Exception(_error_message(response, self.key, api_doc_point))

        return recommended_vids
