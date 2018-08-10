import sys
sys.path.append('../youtube-data-api/youtube_api')
import unittest
import json
import datetime

from youtube_api import P

class TestParsers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('./tests/data/video_metadata.json') as f:
            cls.video_metadata = json.load(f)
        with open('./tests/data/channel_metadata.json') as f:
            cls.channel_metadata = json.load(f)
        with open('./tests/data/subscription.json') as f:
            cls.subscription = json.load(f)
        with open('./tests/data/playlist_meta.json') as f:
            cls.playlist = json.load(f)
        with open('./tests/data/comment_meta.json') as f:
            cls.comment = json.load(f)
        with open('./tests/data/caption.json') as f:
            cls.caption = json.load(f)
        with open('./tests/data/recommendation.json') as f:
            cls.rec = json.load(f)

    def test_raw_json(self):
        item = self.video_metadata.get('items')[0]
        self.assertEqual(item, P.raw_json(item))

    def test_video_metadata(self):
        item = self.video_metadata.get('items')[0]
        metadata = P.parse_video_metadata(self.video_metadata.get('items')[0])

        self.assertEqual(metadata['video_tags'], '')
        self.assertEqual(metadata['video_id'], "kNbhUWLH_yY")
        self.assertEqual(metadata['channel_title'], "CUNAAdvocacy")
        self.assertEqual(metadata['channel_id'], "UCJvIPpWSsW-EGuQjNIZbBTQ")
        self.assertEqual(metadata['video_publish_date'], datetime.datetime(2018, 3, 14, 20, 53, 14))
        self.assertEqual(metadata['video_title'], "Thank you Senator Crapo for your support on Regulatory Relief")
        self.assertEqual(metadata['video_description'], '')
        self.assertEqual(metadata['video_category'], "29")
        self.assertEqual(metadata['video_thumbnail'], "https://i.ytimg.com/vi/kNbhUWLH_yY/hqdefault.jpg")

        self.assertEqual(metadata['video_view_count'], item["statistics"].get("viewCount"))
        self.assertEqual(metadata['video_comment_count'], item["statistics"].get("commentCount"))
        self.assertEqual(metadata['video_like_count'], item["statistics"].get("likeCount"))
        self.assertEqual(metadata['video_dislike_count'], item["statistics"].get("dislikeCount"))

    @unittest.expectedFailure
    def test_video_url(self):
        metadata = P.parse_video_url(self.video_metadata_item)

        self.assertEqual(metadata['publish_date'], datetime.datetime(2018, 3, 14, 20, 53, 14))
        self.assertEqual(metadata['video_id'], "kNbhUWLH_yY")
        self.assertEqual(metadata['channel_id'], "UCJvIPpWSsW-EGuQjNIZbBTQ")

    # never called
    def test_channel_metadata(self):
        item = self.channel_metadata.get('items')[0]
        metadata = P.parse_channel_metadata(item)

        self.assertEqual(metadata['id'], "UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertEqual(metadata['title'], "Google Developers")
        self.assertEqual(metadata['publish_date'], datetime.datetime(2007, 8, 23, 0, 34, 43))
        self.assertIsNone(metadata['keywords'])
        self.assertEqual(metadata['description'], "The Google Developers channel features talks from events, educational series, best practices, tips, and the latest updates across our products and platforms.")

        self.assertEqual(metadata['view_count'], item["statistics"].get("viewCount"))
        self.assertEqual(metadata['video_count'], item["statistics"].get("videoCount"))
        self.assertEqual(metadata['subscription_count'], item["statistics"].get("subscriberCount"))
        self.assertEqual(metadata['playlist_id_likes'], item['contentDetails']['relatedPlaylists'].get('likes'))
        self.assertEqual(metadata['playlist_id_uploads'], item['contentDetails']['relatedPlaylists'].get('uploads'))
        self.assertEqual(metadata['topic_ids'], 'null')

    def test_subscription_descriptive(self):
        item = self.subscription.get('items')[0]
        metadata = P.parse_subscription_descriptive(item)

        self.assertEqual(metadata['subscription_title'], "Google Search Stories")
        self.assertEqual(metadata['subscription_channel_id'], "UCvceBgMIpKb4zK1ss-Sh90w")
        self.assertEqual(metadata['subscription_kind'], "youtube#channel")
        self.assertEqual(metadata['subscription_publish_date'], datetime.datetime(2012, 10, 3, 19, 11, 46))

    def test_featured_channels(self):
        item = self.channel_metadata.get('items')[0]
        metadata = P.parse_featured_channels(item)
        featured_urls = [
          "UCP4bf6IHJJQehibu6ai__cg",
          "UCVHFbqXqoYvEWM1Ddxl0QDg",
          "UCnUYZLuoy1rq1aVMwx4aTzw",
          "UClKO7be7O9cUGL94PHnAeOA",
          "UCdIiCSqXuybzwGwJwrpHPqw",
          "UCJS9pqu9BzkAMNTmzNMNhvg",
          "UCorTyjVGM-PV5CCKbosONow",
          "UCTspylBf8iNobZHgwUD4PXA",
          "UCeo-MamuQVFRcfQmS2N7fhw",
          "UCQqa5UIHtrnpiADC3eHFupw",
          "UCXPBsjgKKG2HqsKBhWA4uQw"
        ]

        self.assertEqual(metadata["UC_x5XG1OV2P6uZZ5FSM9Ttw"],featured_urls)

    def test_playlist_meta(self):
        item = self.playlist.get('items')[0]
        metadata = P.parse_playlist_metadata(item)

        self.assertEqual(metadata['playlist_name'], "PAIR UX Symposium 2018")
        self.assertEqual(metadata['playlist_id'], "PLOU2XLYxmsILhFpQQzS8zo8mc86IRNqMa")
        self.assertEqual(metadata['playlist_publish_date'], datetime.datetime(2018, 6, 29, 21, 24, 9))
        self.assertEqual(metadata['channel_id'], "UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertEqual(metadata['channel_name'], "Google Developers")

        self.assertEqual(metadata['playlist_n_videos'], item['contentDetails'].get('itemCount'))

    def test_comment_metadata(self):
        item = self.comment.get('items')[0]
        metadata = P.parse_comment_metadata(item)

        self.assertEqual(metadata['commenter_channel_url'], "http://www.youtube.com/channel/UCqPPexmEM4QzCq0P-yi6vNA")
        self.assertEqual(metadata['commenter_channel_display_name'], "up work")
        self.assertEqual(metadata['comment_id'], "Ugi7hPbxcLYF3HgCoAEC.7-H0Z7-0SCn8iOqY-oxrko")

        self.assertEqual(metadata['comment_like_count'], item["snippet"].get("likeCount"))

        self.assertEqual(metadata['comment_publish_date'], datetime.datetime(2018, 7, 7, 10, 31, 0))
        self.assertEqual(metadata['text'], "asddddf")
        self.assertEqual(metadata['video_id'], item["snippet"].get("videoId"))

        self.assertEqual(metadata['commenter_rating'], "none")
        self.assertEqual(metadata['comment_parent_id'], "Ugi7hPbxcLYF3HgCoAEC")

    def test_rec_video(self):
        item = self.rec.get('items')[0]
        metadata = P.parse_rec_video_metadata(item)

        self.assertEqual(metadata['video_id'], "BIg10mzhiZs")
        self.assertEqual(metadata['channel_title'], "CUNAAdvocacy")
        self.assertEqual(metadata['channel_id'], "UCJvIPpWSsW-EGuQjNIZbBTQ")
        self.assertEqual(metadata['video_publish_date'], datetime.datetime(2018, 6, 30, 11, 50, 48))
        self.assertEqual(metadata['video_title'], "Jim Nussle’s Opening Speech at CUNA’s 2018 ACUC")
        self.assertEqual(metadata['video_description'], "CUNA President/CEO Jim Nussle presented ideas meant to move the credit union system into the future of financial services at CUNA’s 2018 America’s Credit Union Conference in Boston. CUNA is on a mission, as the champion for credit unions, to harness cooperatives superpowers in order to determine the future for credit unions and our credit union members. As outlined in Nussle’s speech, CUNA’s mission includes delivering fierce, bold 360-degree advocacy offense to revolutionize the operating environment for credit unions by expanding powers and removing barriers to serving consumers and businesses; best-in-class credit union solutions to foster growth, improve operations, manage compliance and enrich member service; and awareness building consumer engagement to create and enhance consumer awareness of credit unions as their best financial partner.")
        self.assertIsNone(metadata['video_category'])
        self.assertEqual(metadata['video_thumbnail'], "https://i.ytimg.com/vi/BIg10mzhiZs/hqdefault.jpg")

if __name__ == '__main__':
    unittest.main()
