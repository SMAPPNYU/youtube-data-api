import sys
sys.path.append('../youtube-data-api/youtube_api')
import unittest
import json
import datetime

from youtube_api import P

class TestParsers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('./tests/data/video_metadata_item.json') as f:
            cls.video_metadata_item = json.load(f)

    def test_raw_json(self):
        self.assertEqual(self.video_metadata_item, P.raw_json(self.video_metadata_item))

    def test_vidoe_metadata(self):
        metadata = P.parse_video_metadata(self.video_metadata_item)

        self.assertEqual(metadata['video_tags'], '')
        self.assertEqual(metadata['video_id'], "kNbhUWLH_yY")
        self.assertEqual(metadata['channel_title'], "CUNAAdvocacy")
        self.assertEqual(metadata['channel_id'], "UCJvIPpWSsW-EGuQjNIZbBTQ")
        self.assertEqual(metadata['video_publish_date'], datetime.datetime(2018, 3, 14, 20, 53, 14))
        self.assertEqual(metadata['video_title'], "Thank you Senator Crapo for your support on Regulatory Relief")
        self.assertEqual(metadata['video_description'], '')
        self.assertEqual(metadata['video_category'], "29")
        self.assertEqual(metadata['video_thumbnail'], "https://i.ytimg.com/vi/kNbhUWLH_yY/hqdefault.jpg")

        self.assertEqual(metadata['video_view_count'], self.video_metadata_item["statistics"].get("viewCount"))
        self.assertEqual(metadata['video_comment_count'], self.video_metadata_item["statistics"].get("commentCount"))
        self.assertEqual(metadata['video_like_count'], self.video_metadata_item["statistics"].get("likeCount"))
        self.assertEqual(metadata['video_dislike_count'], self.video_metadata_item["statistics"].get("dislikeCount"))





if __name__ == '__main__':
    unittest.main()
