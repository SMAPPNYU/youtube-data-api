'''
Last Updated: 12/28/2018

Tests the parameters for the channel methods in the YoutubeDataApi

TO DO
=====
* get_channel_metadata_gen
    * channel_id -- both list and indiv
    * parser
    * part
* get_channel_metadata
    * channel_id -- both list and indiv
    * parser
    * part
* get subscriptions
    * next page token
    * channel_id -- both list and indiv
    * parser
    * part
* get_featured_channels_gen
    * next page token
    * channel_id -- both list and indiv
    * parser
    * part
* get_featured_channels
    * next page token
    * channel_id -- both list and indiv
    * parser
    * part

Functions Tested
================
def get_channel_id_from_user(self, username, **kwargs)

def get_channel_metadata_gen(self, channel_id, parser=P.parse_channel_metadata,
                                 part=["id", "snippet", "contentDetails", "statistics",
                                       "topicDetails", "brandingSettings"],
                                **kwargs)
                                
def get_channel_metadata(self, channel_id, parser=P.parse_channel_metadata,
                             part=["id", "snippet", "contentDetails", "statistics",
                                   "topicDetails", "brandingSettings"],  **kwargs)

def get_subscriptions(self, channel_id, next_page_token=False,
                          parser=P.parse_subscription_descriptive,
                          part=['id', 'snippet'], **kwargs)

def get_featured_channels(self, channel_id, parser=P.parse_featured_channels, **kwargs)

def get_featured_channels_gen(self, channel_id, parser=P.parse_featured_channels,
                                  part=["id", "brandingSettings"], **kwargs)                                   
                                  

DONE 
====
* get_channel_id_from_user

'''

import sys
import os
sys.path.append('../')
import unittest
import requests

from youtube_api import YoutubeDataApi
import youtube_api_utils as utils

class TestVideo(unittest.TestCase):

    def __init__():
        self.key = os.environ.get('YT_KEY')
        self.yt = YoutubeDataApi(self.key)
        self.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'
        self.channel_title = 'LastWeekTonight'

    #written by Megan Brown on 11/30/2018
    def test_channel_id(self):
        resp = self.yt.get_channel_id_from_user(channel_title)
        self.assertEqual(resp, self.channel_id)
        
    def test_get_channel_metadata_channel_id(self):
        resp = self.yt.get_channel_metadata(self.channel_id)
        self.assertEqual(resp['channel_id'], self.channel_id)
        self.assertEqual(resp['channel_title'])

if __name__ == '__main__':
    unittest.main()