import sys
import os
sys.path.append('../')
import unittest
from unittest.mock import patch
import requests

from youtube_api import YouTubeDataAPI

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.wrong_key = 'xxxxxxxxx'
        cls.yt = YouTubeDataAPI(cls.key, timeout=10)


    def test_init(self):
        '''#Verified by Megan Brown on 11/30/2018'''
        with self.assertRaisesRegex(ValueError, 'No API key used to initate the class.'):
            yt = YouTubeDataAPI('')

        with self.assertRaisesRegex(ValueError, 'The API Key is invalid'):
            yt = YouTubeDataAPI(self.wrong_key)


    @patch('requests.get')
    def test_verify(self, mock_request):
        '''#verified by Megan Brown on 11/30/2018'''
        mock_resp = requests.models.Response()
        mock_resp.status_code = 404
        mock_request.return_value = mock_resp

        self.assertEqual(self.yt.verify_key(), False)

if __name__ == '__main__':
    unittest.main()
