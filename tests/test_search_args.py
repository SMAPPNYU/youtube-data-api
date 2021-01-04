import sys
import os
sys.path.append('../youtube-data-api/')
import unittest
import requests
import datetime
from collections import OrderedDict
from youtube_api import YouTubeDataAPI

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YouTubeDataAPI(cls.key)
        cls.search_term = 'John Oliver'
        cls.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.max_results = 10
        cls.published_after = datetime.datetime.timestamp(datetime.datetime(2018,11,30))
        cls.published_before = datetime.datetime.timestamp(datetime.datetime(2018,12,1))
        cls.topic_search = 'ted talks'
        cls.topic_id = 22

        
    
    def test_search_param_q(self):
        '''#written by Megan Brown on 11/30/2018'''
        resp = self.yt.search(self.search_term)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
    
    def test_search_param_channel_id(self):
        ''' #written by Megan Brown on 11/30/2018'''
        resp = self.yt.search(self.search_term, channel_id=self.channel_id)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            self.assertEqual(item['channel_id'], self.channel_id)
            
            
    
    def test_search_param_max_results(self):
        '''#written by Megan Brown on 11/30/2018'''
        resp = self.yt.search(self.search_term, max_results = self.max_results)
        
        self.assertTrue(len(resp) == self.max_results)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            
    
    def test_search_param_published_after(self):
        '''#written by Megan Brown on 11/30/2018'''
        resp = self.yt.search(self.search_term, published_after = self.published_after)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            
            
            self.assertTrue(item['video_publish_date'] > self.published_after)
            
            
    def test_search_param_published_before(self):
        '''#written by Megan Brown on 11/30/2018'''
        resp = self.yt.search(self.search_term, published_before = self.published_before)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            
            self.assertTrue(item['video_publish_date'] < self.published_before)
            
    
    def test_search_param_topic_id(self):
        '''
        written by Megan Brown on 11/30/2018
        '''
        resp = self.yt.search(self.topic_search, topic_id=self.topic_id, max_results=2)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
            
            video_id = item['video_id']
            video_meta = self.yt.get_video_metadata(video_id)
            self.assertTrue(isinstance(int(video_meta['video_category']), int))

if __name__ == '__main__':
    unittest.main()
    