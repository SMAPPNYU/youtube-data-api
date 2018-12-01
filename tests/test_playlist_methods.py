'''
Last Updated: 11/30/2018

Tests the parameters for the channel methods in the YoutubeDataApi

TO DO
=====
* get_playlists
    * channel_id
    * next_page_token
    * parser
    * part
* get_video_from_playlist_id
    * playlist
    * next_page_token
    * published_after
    * parser
    * part

Functions Tested
================
def get_playlists(self, channel_id, next_page_token=False, parser=P.parse_playlist_metadata,
                      part=['id','snippet','contentDetails'], **kwargs)
                      
def get_videos_from_playlist_id(self, playlist_id, next_page_token=None,
                                    published_after=datetime.datetime(1990,1,1),
                                    parser=P.parse_video_url, part=['snippet'], **kwargs)
                                 

DONE 
====


'''

import sys
import os
sys.path.append('../')
import unittest
import requests

from youtube_api import YoutubeDataApi

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.playlist_id = ''
