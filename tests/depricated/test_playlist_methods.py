import os
import sys
import requests
import unittest
import datetime
import collections

sys.path.append(os.path.abspath('../')) 
from youtube_api import YoutubeDataApi
import youtube_api.parsers as P
import config
from test_utils import get_all_keys

class TestSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key = config.key
        cls.yt = YoutubeDataApi(config.key)
        cls.defunct_playlist_id = 'UUvsye7V9psc-APX6wV1twLg' #alex jones
        cls.playlist_id = 'UU3XTzVzaHQEd30rQbuvCtTQ'         #lastweektonight
        cls.future_date = datetime.datetime(2200, 1, 1)
        cls.cutoff_date = datetime.datetime(2018, 1, 1)
        
        cls.default_parser_output_keys = [
            'channel_id', 'collection_date', 'publish_date', 'video_id'
        ]
        
        cls.raw_json_output_keys = [
            'snippet.thumbnails.medium.width',
            'snippet.thumbnails.maxres.height',
            'snippet.channelId',
            'snippet.thumbnails.standard.height',
            'snippet.thumbnails.high.url',
            'collection_date',
            'snippet.playlistId',
            'snippet.publishedAt',
            'snippet.thumbnails.default.height',
            'kind',
            'channel_id',
            'snippet.thumbnails.maxres.url',
            'etag',
            'snippet.description',
            'snippet.resourceId.kind',
            'snippet.thumbnails.high.width',
            'snippet.title',
            'snippet.thumbnails.medium.height',
            'publish_date',
            'snippet.thumbnails.standard.width',
            'snippet.channelTitle',
            'snippet.position',
            'video_id',
            'snippet.thumbnails.default.width',
            'snippet.thumbnails.medium.url',
            'snippet.thumbnails.standard.url',
            'id',
            'snippet.thumbnails.high.height',
            'snippet.thumbnails.default.url',
            'snippet.thumbnails.maxres.width',
            'snippet.resourceId.videoId'
        ]
        
    def test_default_parser_dict_keys(self):
        '''Make sure the default keys are the same'''
        videos = self.yt.get_videos_from_playlist_id(self.playlist_id,
                                                     cutoff_date=self.cutoff_date)
        first_video = videos[0]
        keys_of_first_video = get_all_keys(first_video)
        
        self.assertEqual(collections.Counter(keys_of_first_video),
                         collections.Counter(self.default_parser_output_keys))
        
    def test_raw_json_output_dict_keys(self):
        '''Make sure the raw json keys are the same'''
        videos = self.yt.get_videos_from_playlist_id(self.playlist_id, 
                                                     parser=P.raw_json,
                                                     cutoff_date=self.cutoff_date)
        first_video = videos[0]
        keys_of_first_video = get_all_keys(first_video)
        
        self.assertEqual(collections.Counter(keys_of_first_video), 
                         collections.Counter(self.raw_json_output_keys))
    
    def test_future_cutoff_date(self):
        '''When the cutoffdate is the future, the result should be an empty list.'''
        videos = self.yt.get_videos_from_playlist_id(self.playlist_id, 
                                                     parser=P.raw_json,
                                                     cutoff_date=self.future_date)
        self.assertEqual(videos, [])

        
    def test_next_page_token(self):
        '''Test net page token returns input, and that it is different from without it'''
        videos = self.yt.get_videos_from_playlist_id(self.playlist_id, 
                                                     parser=P.raw_json, 
                                                     cutoff_date=datetime.datetime(2017,2,2),
                                                     next_page_token='CBkQAA')
        first_video = videos[0]
        self.assertEqual(type(first_video), dict)
        
        videos_ = self.yt.get_videos_from_playlist_id(self.playlist_id, 
                                                     parser=P.raw_json, 
                                                     cutoff_date=datetime.datetime(2017,2,2))
        self.assertEqual(len(videos) == len(videos_), False)
   
    
    def test_error_cutoff_date_as_string(self):
        '''Checks the error when cutoffdate is a string'''
        with self.assertRaises(TypeError):
            videos = self.yt.get_videos_from_playlist_id(self.playlist_id, 
                                                         parser=P.raw_json, 
                                                         cutoff_date='2018-01-03')  
    def test_error_from_defunct_channel_id(self):
        '''What happens when we try to input a defunct or invalid channel'''
        with self.assertRaises(requests.exceptions.HTTPError): 
            self.yt.get_videos_from_playlist_id(self.defunct_playlist_id)

            
if __name__ == '__main__':
    unittest.main()