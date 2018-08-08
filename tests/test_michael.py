import sys
sys.path.append('../youtube-data-api/youtube_api')
import unittest
from unittest.mock import patch
import requests
from youtube_api import YoutubeDataApi
from youtube_api_utils import *
from .config import key

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = key
        cls.yt = YoutubeDataApi(cls.key)

    def test_init(self):
        self.wrong_key = self.key[:-1]

        with self.assertRaises(ValueError) as cm:
            yt = YoutubeDataApi('')

        with self.assertRaises(ValueError) as cm:
            yt = YoutubeDataApi(self.wrong_key)

    @patch('requests.get')
    def test_verify(self, mock_request):
        mock_resp = requests.models.Response()
        mock_resp.status_code = 404
        mock_request.return_value = mock_resp

        self.assertEqual(self.yt.verify_key(), False)

if __name__ == '__main__':
    unittest.main()
