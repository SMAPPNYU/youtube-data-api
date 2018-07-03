import os
import time
import sys
import json
import requests
import datetime
from collections import OrderedDict
import pandas as pd
from pytube import YouTube
import warnings

from youtube_api_utils import *
import parsers as P


class YoutubeDataApi:
    """
    The Youtube Data API handles the keys and methods to access data from the YouTube Data API
    """
    def __init__(self, key):
        """
        :param key: YouTube Data API key
        Get a YouTube Data API key here: https://console.cloud.google.com/apis/dashboard
        """

        if verify_key(key):
            self.key = key
        else:
            warnings.warn("Your key was invalid!")
            sys.exit()

    def get_channel_id_from_user(self, username, verbose=1, handle_error=True):
        """
        Get a channel_id from a YouTube username.
        To get video_ids from the channel_id, you need to get the "upload playlist id".
        This can be done using `get_upload_playlist()` for `get_channel_metadata()`.

        :param username: the username for a YouTube channel
        :type username: str
        :param verbose: logging settings
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: the YouTube channel id for the given username
        """
        http_endpoint = ("https://www.googleapis.com/youtube/v3/channels"
                         "?part=id"
                         "&forUsername={}&key={}".format(username, self.key))
        response = requests.get(http_endpoint)
        response_json = load_response(response, verbose, handle_error)
        if response_json:
            if "items" in response_json and response_json['items']:
                channel_id = response_json['items'][0]['id']
                return channel_id
            else:
                return -1
        else:
            return response_json


    def get_video_metadata(self, video_id, verbose=1, parser=P.parse_video_metadata, handle_error=True):
        '''
        Given a `video_id` returns metrics (views, likes, comments) and metadata (description, category) as a dictionary.

        :param video_id: (str or list of str) the ID of a video IE:kNbhUWLH_yY, this can be found at the end of Youtube urls and by parsing links using `get_youtube_id()`
        :param key: (str) the API key to the Youtube Data API.
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: video_ids (str or list of str) a list of dictionaries containing metadata.
        '''
        get_one = True
        if isinstance(video_id, list):
            get_one = False
            if len(video_id) > 50:
                raise Exception("Max length of list is 50!")
            video_id = ','.join(video_id)

        http_endpoint = ("https://www.googleapis.com/youtube/v3/videos"
                         "?part=statistics,snippet"
                         "&id={}&key={}&maxResults=50".format(video_id, self.key))
        response = requests.get(http_endpoint)
        response_json = load_response(response, verbose, handle_error)
        video_meta = []
        if response_json:
            for item in response_json['items']:
                video_meta_ = parser(item)
                video_meta.append(video_meta_)
        if len(video_meta) == 1 and get_one:
            video_meta = video_meta[0]

        return video_meta


    def get_video_urls_from_playlist_id(self, playlist_id, next_page_token=False,
                                        cutoff_date=datetime.datetime(1990,1,1),
                                        verbose=1, parser=P.parse_video_url, handle_error=True):
        '''
        Given a `playlist_id`, returns a list of `video_ids` associated with that playlist.
        Note that to user uploads are a playlist from channels.
        Typically this pattern is just the channel ID with UU subbed as the first two letters.
        You can access this using the function `get_upload_playlist_id`, or from the `playlist_id_likes`
        key returned from `get_channel_metadata`.

        :param playlist_id: (str) the playlist_id IE:UUaLfMkkHhSA_LaCta0BzyhQ
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA
        :param cutoff_date: (datetime) a date for the minimum publish date for videos from a playlist_id.
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: video_ids (list of str) a list of video ids associated with `playlist_id`.
        '''
        if playlist_id == -1:
            raise Exception("playlist_id was -1")
        video_ids = []
        iterations = 0
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v3/playlistItems"
                             "?part=snippet&playlistId={}"
                             "&maxResults=50&key={}".format(playlist_id, self.key))

            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = load_response(response, verbose, handle_error)
            if response_json:
                for item in response_json['items']:
                    v_id = parser(item)
                    if v_id['publish_date'] <= cutoff_date:
                        run = False
                        break
                    video_ids.append(v_id)

                try:
                    next_page_token = response_json['nextPageToken']
                    iterations += 1
                    log(">> {} Videos parsed. Next Token = {}".format(len(video_ids), next_page_token),
                       verbose=verbose)
                except:
                    run = False
            time.sleep(.1)

        return video_ids


    def get_channel_metadata(self, channel_id, verbose=1, parser=P.parse_channel_metadata, handle_error=True):
        '''
        Gets a dictionary of channel metadata given a channel_id, or a list of channel_ids.

        :param channel_id: (str or list of str) the channel id(s)
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: dictionary of metadata from the channel
        '''
        get_one = True
        if isinstance(channel_id, list):
            if len(channel_id) > 50:
                raise Exception("Max length of list is 50!")
            get_one = False
            channel_id = ','.join(channel_id)
        http_endpoint = ("https://www.googleapis.com/youtube/v3/channels"
                         "?part=id,snippet,contentDetails,statistics,topicDetails,brandingSettings"
                         "&id={}&key={}&maxResults=50".format(channel_id, self.key))
        response = requests.get(http_endpoint)
        response_json = load_response(response, verbose, handle_error)

        channel_meta = []
        if response_json:
            for item in response_json['items']:
                channel_meta_ = parser(item)
                channel_meta.append(channel_meta_)
        else:
            channel_meta = [OrderedDict()]
        if len(channel_meta) == 1 and get_one:
            channel_meta = channel_meta[0]

        return channel_meta


    def get_subscriptions(self, channel_id, next_page_token=False,
                          parser = P.parse_subscription_descriptive,
                          verbose= 1, handle_error=True):
        '''
        Returns a list of channel IDs that `channel_id` is subscribed to.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA
        :param stop_after_n_iteration: (int) stops the API calls after N API calls
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: subscription_ids (list) of channel IDs that `channel_id` is subscrbed to.
        '''
        subscriptions = []
        iterations = 0
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v3/subscriptions"
                             "?channelId={}&part=id,snippet"
                             "&maxResults=50&key={}".format(channel_id, self.key))

            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)

            response = requests.get(http_endpoint)
            response_json = load_response(response, verbose, handle_error)
            if not response_json:
                run = False
                break

            for item in response_json['items']:
                sub_meta = parser(item)
                subscriptions.append(sub_meta)

            try:
                next_page_token = response_json['nextPageToken']
                iterations += 1
                log(">> {} subscriptions parsed. Next Token = {}".format(
                    len(subscriptions), next_page_token),
                    verbose=verbose)
            except:
                run = False

            time.sleep(.1)

        return subscriptions


    def get_featured_channels(self, channel_id, verbose=1, parser=P.parse_featured_channels, handle_error=True):
        '''
        Given a `channel_id` returns a dictionary {channel_id : [list, of, channel_ids]}
        of featured channels.

        Optionally, can take a list of channel IDS, and returns a list of dictionaries.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: A dictionary of featured channels
        '''
        get_one = True
        if isinstance(channel_id, list):
            get_one = False
            if len(channel_id) > 50:
                 raise Exception("Max length of list is 50!")
            channel_id = ','.join(channel_id)
        http_endpoint = ("https://www.googleapis.com/youtube/v3/channels"
                         "?part=id,brandingSettings"
                         "&id={}&key={}".format(channel_id, self.key))
        response = requests.get(http_endpoint)
        response_json = load_response(response, verbose, handle_error)

        feat_channels = []
        if response_json:
            for item in response_json['items']:
                feat_channel_ = parser(item)
                feat_channels.append(feat_channel_)

        if len(feat_channels) == 1 and get_one:
            feat_channels = feat_channels[0]

        return feat_channels


    def get_playlists(self, channel_id, next_page_token=False,
                      verbose=1, parser=P.parse_playlist_metadata, handle_error=True):
        '''
        Returns a list of playlist IDs that `channel_id` created.
        Note that playlists can contains videos from any users.

        :param channel_id: (str) a channel_id IE:UCn8zNIfYAQNdrFRrr8oibKw
        :param next_page_token: (str) a token to continue from a preciously stopped query IE:CDIQAA
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: playlists (list of dicts) of playlist IDs that `channel_id` is subscribed to.
        '''
        playlists = []
        iterations = 0
        run = True
        while run:
            http_endpoint = ("https://www.googleapis.com/youtube/v3/playlists"
                             "?part=id,snippet,contentDetails"
                             "&channelId={}&key={}&maxResults=50".format(channel_id, self.key))
            if next_page_token:
                http_endpoint += "&pageToken={}".format(next_page_token)
            response = requests.get(http_endpoint)
            response_json = load_response(response, verbose, handle_error)
            if not response_json:
                run = False
                break

            for item in response_json['items']:
                playlist_meta = parser(item)
                playlists.append(playlist_meta)

            try:
                next_page_token = response_json['nextPageToken']
                iterations += 1
                log(">> {} playlists parsed. Next Token = {}".format(
                    len(playlists), next_page_token),
                    verbose=verbose)
            except:
                run = False

        return playlists


    def get_video_comments(self, video_id, get_replies = True,
                           cutoff_date=datetime.datetime(1990,1,1),
                           verbose=1, parser=P.parse_comment_metadata, handle_error=True):
        """
        Returns a list of comments on a given video

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param get_replies: (bool) whether or not to get replies to comments
        :param stop_after_n_iteration: (int) stops the API calls after N API calls
        :param cutoff_date: (datetime) a date for the minimum publish date for comments from a video_id.
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: comments (list of dicts) of comments from the comments section on a given video_id
        """

        comments = []

        init_http_endpoint = ("https://www.googleapis.com/youtube/v3/commentThreads?"
                             "part=snippet&textFormat=plainText&maxResults=100&"
                             "videoId={}&key={}".format(video_id,self.key))

        response = requests.get(init_http_endpoint)

        json_doc = load_response(response, verbose, handle_error)

        if not json_doc:
            return []
        if not json_doc.get('items'):
            return []

        comments = [parser(comment) for comment in json_doc['items']]

        log(">> {} comments parsed. Next Token = {}".format(
                    len(comments), json_doc.get('nextPageToken')),
                    verbose=verbose)

        while json_doc.get('nextPageToken'):
            token = json_doc.get('nextPageToken')
            new_http_endpoint = ("https://www.googleapis.com/youtube/v3/commentThreads?"
                             "part=snippet&textFormat=plainText&maxResults=100&"
                             "videoId={}&key={}&pageToken={}".format(video_id,self.key,token))
            response = requests.get(new_http_endpoint)
            json_doc = load_response(response, verbose, handle_error)
            comments.extend([parser(comment) for comment in json_doc['items']])

            log(">> {} comments parsed. Next Token = {}".format(
                    len(comments), json_doc.get('nextPageToken')),
                    verbose=verbose)

        if get_replies:
            current_num = len(comments)

            for comment in comments:
                if comment['reply_count']:
                    if comment['reply_count'] > 0:
                        reply_http_endpoint = ("https://www.googleapis.com/youtube/v3/comments?"
                                     "part=snippet&textFormat=plainText&maxResults=100&"
                                     "parentId={}&key={}".format(comment['comment_id'],self.key))
                        response = requests.get(reply_http_endpoint)
                        json_doc = load_response(response, verbose, handle_error)
                        comments.extend([parser(comment) for comment in json_doc['items']])

                        if len(comments) > current_num:
                            log(">> {} comments parsed.".format(
                                len(comments)),
                                verbose=verbose)
                            current_num = len(comments)


        return comments


    def get_captions(self, video_id, lang_code='en', verbose=1, parser=P.parse_caption_track):
        """
        Grabs captions given a video id using the PyTube and BeautifulSoup Packages

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param lang_code: (str) language to get captions in
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: the captions from a given video_id

        """
        url = get_url_from_video_id(video_id)
        vid = YouTube(url)
        try:
            captions = vid.captions.get_by_language_code(lang_code)
        except Exception as e:
            log(handle_caption_error(e, verbose=verbose))

        resp = {}
        if not captions:
            resp['caption'] = None
        else:
            clean_cap = text_from_html(captions.xml_captions)
            log("Captions for {} collected".format(video_id),
                    verbose=verbose)

            resp['caption'] = clean_cap

        resp['video_id'] = video_id
        resp['collection_date'] = datetime.datetime.now()

        return resp


    def get_recommended_videos(self, video_id, max_results=25,
                               parser=P.parse_rec_video_metadata,
                               verbose=1):
        """
        Grabs captions given a video id using the PyTube and BeautifulSoup Packages

        :param video_id: (str) a vide_id IE: eqwPlwHSL_M
        :param max_results: (int) max number of recommended vids
        :param verbose: (int) determines how errors are printed to the system. 1 is print 2 is log 0 is silent.
        :param parser: (func) the function to parse the json document
        :param handle_error: whether or not the module handles errors itself or exits the system
        :type handle_error: bool

        :returns: a list of videos and video metadata for recommended videos

        """
        if not isinstance(video_id, str):
            raise Exception("Only string values permitted")

        http_endpoint = ("https://www.googleapis.com/youtube/v3/search?"
                         "part=snippet&type=video&maxResults={}&"
                         "relatedToVideoId={}&key={}".format(max_results, video_id, self.key))

        response_json = load_response(requests.get(http_endpoint))
        recommended_vids = [parser(item) for item in response_json['items']]

        return recommended_vids