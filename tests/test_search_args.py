'''
Last Updated: 11/30/2018

Tests the parameters for the `search` method in the YoutubeDataApi

TO DO
=====
* order_by
* next_page_token
* location
* location_radius
* region_code
* safe_search
* relevance_language
* event_type
* video_duration
* search_type
* parser
* part


Function Tested
================
def search(self, q=None, channel_id=None,
               max_results=5, order_by="relevance", next_page_token=None,
               published_after=datetime.datetime(2000,1,1),
               published_before=datetime.datetime(3000,1,1),
               location=None, location_radius='1km', region_code=None,
               safe_search=None, relevance_language=None, event_type=None,
               topic_id=None, video_duration=None, search_type="video",
               parser=P.parse_rec_video_metadata, part=['snippet'],
               **kwargs)
               
DONE
====
* q
* channel_id
* max_results
* published_after
* published_before
* topic_id

'''

import sys
import os
sys.path.append('../youtube-data-api/')
import unittest
import requests
import datetime
from collections import OrderedDict
from youtube_api import YoutubeDataApi

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.search_term = 'John Oliver'
        cls.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.max_results = 10
        cls.published_after = datetime.datetime(2018,11,30)
        cls.published_before = datetime.datetime(2018,12,1)
        cls.topic_search = 'ted talks'
        cls.topic_id = 22

        
    #written by Megan Brown on 11/30/2018
    def test_search_param_q(self):
        resp = self.yt.search(self.search_term)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
    
    #written by Megan Brown on 11/30/2018
    def test_search_param_channel_id(self):
        resp = self.yt.search(self.search_term, channel_id=self.channel_id)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            self.assertEqual(item['channel_id'], self.channel_id)
            
            
    #written by Megan Brown on 11/30/2018
    def test_search_param_max_results(self):
        resp = self.yt.search(self.search_term, max_results = self.max_results)
        
        self.assertTrue(len(resp) == self.max_results)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            
    #written by Megan Brown on 11/30/2018
    def test_search_param_published_after(self):
        resp = self.yt.search(self.search_term, published_after = self.published_after)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            
            self.assertTrue(item['video_publish_date'] > self.published_after)
     
    #written by Megan Brown on 11/30/2018
    def test_search_param_published_before(self):
        resp = self.yt.search(self.search_term, published_before = self.published_before)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            
            self.assertTrue(item['video_publish_date'] < self.published_before)
            
    #written by Megan Brown on 11/30/2018
    def test_search_param_topic_id(self):
        resp = self.yt.search(self.topic_search, topic_id=self.topic_id, max_results=2)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            
            video_id = item['video_id']
            video_meta = self.yt.get_video_metadata(video_id)
            
            self.assertTrue(video_meta['video_category'] == str(self.topic_id))

if __name__ == '__main__':
    unittest.main()
    