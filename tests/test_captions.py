'''
Last Updated: 11/30/2018

Tests the parameters for the `get_captions` method in the YoutubeDataApi

TO DO
=====
* parser
* LIST OF VALID VIDEO IDS DOES NOT WORK AND I HAVE NO IDEA WHY

Functions Tested
================
def get_captions(self, video_id, lang_code='en', parser=P.parse_caption_track, **kwargs)

DONE
====
* video_id
* lang_code

'''
import sys
import os
sys.path.append('../')
import unittest
import requests

from youtube_api import YoutubeDataApi

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.key = os.environ.get('YT_KEY')
        self.yt = YoutubeDataApi(self.key)
        self.video_id = 'wmxDZeh8W34'
        self.video_id_list = ['wmxDZeh8W34', 'PIXQdfiRZNk', 'nvEFb_dWJdQ']
        self.fake_vid = '12345'
        
    #Verified by Megan Brown on 11/30/2018
    def test_valid_caption(self):
        resp = self.yt.get_captions(self.video_id)

        self.assertEqual(type(resp), dict)
        self.assertEqual(type(resp['video_id']), str)

    #Written by Megan Brown on 11/30/2018
    def test_valid_list_of_captions(self):
        print(self.video_id_list)
        resp = self.yt.get_captions(self.video_id_list)

        self.assertEqual(type(resp), list)
        self.assertEqual(type(resp[0]['video_id']), str)

    #Written by Megan Brown on 11/30/2018
    def test_invalid_short_caption(self):
        with self.assertRaises(Exception):
            resp = self.yt.get_captions(self.fake_vid)

    #Written by Megan Brown on 11/30/2018
    def test_list_of_captions_with_invalid_string(self):
        error_list = self.video_id_list.copy()
        error_list.append(self.fake_vid)
        
        with self.assertRaises(Exception):
            resp = self.yt.get_captions(error_list)

if __name__ == '__main__':
    unittest.main()
