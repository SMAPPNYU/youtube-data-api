import sys
import os
sys.path.append('../youtube-data-api/youtube_api')
import unittest
import requests
import datetime
from collections import OrderedDict
from youtube_api import YoutubeDataApi

'''
def search(self, q=None, channel_id=None,
               max_results=5, order_by="relevance", next_page_token=None,
               published_after=datetime.datetime(2000,1,1),
               published_before=datetime.datetime(3000,1,1),
               location=None, location_radius='1km', region_code=None,
               safe_search=None, relevance_language=None, event_type=None,
               topic_id=None, video_duration=None, search_type="video",
               parser=P.parse_rec_video_metadata, part=['snippet'],
               **kwargs):
'''

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.search_term = 'John Oliver'
        cls.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.max_results = 10
        cls.published_after = datetime.datetime(2018,12,1)
        cls.published_before = datetime.datetime(2018,12,1)
        cls.topic_id = 23
        
        '''
        TO BE TESTED
        ============
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
        '''
        
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
            

        

if __name__ == '__main__':
    unittest.main()
    