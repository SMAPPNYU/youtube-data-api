'''
Last Updated: 11/30/2018

Tests the parameters for the channel methods in the YoutubeDataApi

TO DO
=====
* _chunker
* _load_response
* _text_from_html
* strip_youtube_id
* get_channel_id_from_custom_url

Functions Tested
================
def _chunker(l, chunksize)

def _load_response(response)

def _text_from_html(html_body)

def parse_yt_datetime(date_str)

def strip_video_id_from_url(url)

def get_upload_playlist_id(channel_id)

def get_liked_playlist_id(channel_id)

def is_user(channel_url)

def strip_youtube_id(channel_url)

def get_channel_id_from_custom_url(url)

def get_url_from_video_id(video_id)                                  

DONE 
====
* get_upload_playlist_id
* get_liked_playlist_id
* parse_yt_datetime
* strip_video_id_from_url
* is_user
* get_url_from_video_id
'''

import sys
import os
sys.path.append('../')
import unittest
import requests
import datetime

from youtube_api import YoutubeDataApi
from youtube_api import youtube_api_utils as utils

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.upload_id = 'UU3XTzVzaHQEd30rQbuvCtTQ'
        cls.liked_id = 'LL3XTzVzaHQEd30rQbuvCtTQ'
        cls.date = '2018-03-14T20:53:14.000Z'
        cls.datetime_date = datetime.datetime(2018, 3, 14, 20, 53, 14)
        cls.user_url = 'https://www.youtube.com/user/LastWeekTonight'
        cls.channel_url = 'https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.video_id = '481YX6T9Xzs'
        cls.video_url = 'https://youtube.com/watch?v=481YX6T9Xzs'
        
    #Written by Megan Brown on 11/30/2018
    def test_get_upload_playlist_id(self):
        resp = utils.get_upload_playlist_id(self.channel_id)
        
        self.assertEqual(resp, self.upload_id)
      
    #Written by Megan Brown on 11/30/2018
    def test_get_liked_playlist_id(self):
        resp = utils.get_liked_playlist_id(self.channel_id)
        
        self.assertEqual(resp, self.liked_id)
        
    #Verified by Megan Brown on 11/30/2018
    def test_parse_yt_datetime(self):
        resp = utils.parse_yt_datetime(self.date)
        self.assertEqual(resp, self.datetime_date)
        
    #Verified by Megan Brown on 11/30/2018
    def test_strip_video_id_from_url(self):
        resp = utils.strip_video_id_from_url(self.video_url)
        self.assertEqual(resp, self.video_id)
        
    #Verified by Megan Brown on 11/30/2018
    def test_is_user(self):
        resp = utils.is_user(self.user_url)
        self.assertTrue(resp)
        
        resp = utils.is_user(self.channel_url)
        self.assertFalse(resp)
        
    #Verified by Megan Brown on 11/30/2018
    def test_get_url_from_video_id(self):
        resp = utils.get_url_from_video_id(self.video_id)
        self.assertEqual(resp, self.video_url)
        
if __name__ == '__main__':
    unittest.main()