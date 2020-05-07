import os
import sys
sys.path.append('../')
import unittest
import json
import datetime

from youtube_api import parsers as P

class TestParsers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname,'data','video_metadata.json')) as f:
            cls.video_metadata = json.load(f)
        with open(os.path.join(dirname, 'data', 'channel_metadata.json')) as f:
            cls.channel_metadata = json.load(f)
        with open(os.path.join(dirname, 'data', 'subscription.json')) as f:
            cls.subscription = json.load(f)
        with open(os.path.join(dirname, 'data', 'playlist_meta.json')) as f:
            cls.playlist = json.load(f)
        with open(os.path.join(dirname, 'data', 'comment_meta.json')) as f:
            cls.comment = json.load(f)
        with open(os.path.join(dirname, 'data','caption.json')) as f:
            cls.caption = json.load(f)
        with open(os.path.join(dirname, 'data', 'recommendation.json')) as f:
            cls.rec = json.load(f)

    
    def test_raw_json(self):
        '''Verified by Megan Brown on 11/30/2018'''
        item = self.video_metadata.get('items')[0]
        self.assertEqual(item, P.raw_json(item))

    def test_video_metadata(self):
        '''Verified by Megan Brown on 11/30/2018'''
        item = self.video_metadata.get('items')[0]
        metadata = P.parse_video_metadata(self.video_metadata.get('items')[0])

        self.assertEqual(metadata['video_tags'], '')
        self.assertEqual(metadata['video_id'], "kNbhUWLH_yY")
        self.assertEqual(metadata['channel_title'], "CUNAAdvocacy")
        self.assertEqual(metadata['channel_id'], "UCJvIPpWSsW-EGuQjNIZbBTQ")
        self.assertEqual(metadata['video_publish_date'], datetime.datetime.timestamp(datetime.datetime(2018, 3, 14, 20, 53, 14)))
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
        '''Verified by Megan Brown on 11/30/2018'''
        metadata = P.parse_video_url(self.video_metadata_item)

        self.assertEqual(metadata['publish_date'], datetime.datetime.timestamp(datetime.datetime(2018, 3, 14, 20, 53, 14)))
        self.assertEqual(metadata['video_id'], "kNbhUWLH_yY")
        self.assertEqual(metadata['channel_id'], "UCJvIPpWSsW-EGuQjNIZbBTQ")

    
    def test_channel_metadata(self):
        '''Verified by Megan Brown on 11/30/2018'''
        item = self.channel_metadata.get('items')[0]
        metadata = P.parse_channel_metadata(item)

        self.assertEqual(metadata['channel_id'], "UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertEqual(metadata['title'], "Google Developers")
        #self.assertEqual(metadata['publish_date'], datetime.datetime(2007, 8, 23, 0, 34, 43))
        self.assertIsNone(metadata['keywords'])
        self.assertEqual(metadata['description'], "The Google Developers channel features talks from events, educational series, best practices, tips, and the latest updates across our products and platforms.")

        self.assertEqual(metadata['view_count'], item["statistics"].get("viewCount"))
        self.assertEqual(metadata['video_count'], item["statistics"].get("videoCount"))
        self.assertEqual(metadata['subscription_count'], item["statistics"].get("subscriberCount"))
        self.assertEqual(metadata['playlist_id_likes'], item['contentDetails']['relatedPlaylists'].get('likes'))
        self.assertEqual(metadata['playlist_id_uploads'], item['contentDetails']['relatedPlaylists'].get('uploads'))
        self.assertEqual(metadata['topic_ids'], None)
        
    
    def test_subscription_descriptive(self):
        '''#Verified by Megan Brown on 11/30/2018'''
        item = self.subscription.get('items')[0]
        metadata = P.parse_subscription_descriptive(item)

        self.assertEqual(metadata['subscription_title'], "Google Search Stories")
        self.assertEqual(metadata['subscription_channel_id'], "UCvceBgMIpKb4zK1ss-Sh90w")
        self.assertEqual(metadata['subscription_kind'], "youtube#channel")
        self.assertEqual(metadata['subscription_publish_date'], datetime.datetime.time
                         stamp(datetime.datetime(2012, 10, 3, 19, 11, 46)))

    
    def test_featured_channels(self):
        '''#Verified by Megan Brown on 11/30/2018'''
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
        '''#Verified by Megan Brown on 11/30/2018'''
        item = self.playlist.get('items')[0]
        metadata = P.parse_playlist_metadata(item)

        self.assertEqual(metadata['playlist_name'], "PAIR UX Symposium 2018")
        self.assertEqual(metadata['playlist_id'], "PLOU2XLYxmsILhFpQQzS8zo8mc86IRNqMa")
        self.assertEqual(metadata['playlist_publish_date'], datetime.datetime.timestamp(datetime.datetime(2018, 6, 29, 21, 24, 9)))
        self.assertEqual(metadata['channel_id'], "UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertEqual(metadata['channel_name'], "Google Developers")

        self.assertEqual(metadata['playlist_n_videos'], item['contentDetails'].get('itemCount'))

    
    def test_comment_metadata(self):
        '''#Verified by Megan Brown on 11/30/2018'''
        item = self.comment.get('items')[0]
        metadata = P.parse_comment_metadata(item)

        self.assertEqual(metadata['commenter_channel_url'], "http://www.youtube.com/channel/UCqPPexmEM4QzCq0P-yi6vNA")
        self.assertEqual(metadata['commenter_channel_display_name'], "up work")
        self.assertEqual(metadata['comment_id'], "Ugi7hPbxcLYF3HgCoAEC.7-H0Z7-0SCn8iOqY-oxrko")

        self.assertEqual(metadata['comment_like_count'], item["snippet"].get("likeCount"))

        self.assertEqual(metadata['comment_publish_date'], datetime.datetime.timestamp(datetime.datetime(2018, 7, 7, 10, 31, 0)))
        self.assertEqual(metadata['text'], "asddddf")
        self.assertEqual(metadata['video_id'], item["snippet"].get("videoId"))

        self.assertEqual(metadata['commenter_rating'], "none")
        self.assertEqual(metadata['comment_parent_id'], "Ugi7hPbxcLYF3HgCoAEC")

    
    def test_rec_video(self):
        '''#Verified by Megan Brown on 11/30/2018'''
        item = self.rec.get('items')[0]
        metadata = P.parse_rec_video_metadata(item)

        self.assertEqual(metadata['video_id'], "w-HYZv6HzAs")
        self.assertEqual(metadata['channel_title'], "TEDx Talks")
        self.assertEqual(metadata['channel_id'], "UCsT0YIqwnpJCM-mx7-gSA4Q")
        self.assertEqual(metadata['video_publish_date'], datetime.datetime.timestamp(datetime.datetime(2012, 1, 13, 19, 42, 36)))
        self.assertEqual(metadata['video_title'], "The skill of self confidence | Dr. Ivan Joseph | TEDxRyersonU")
        self.assertEqual(metadata['video_description'], "Never miss a talk! SUBSCRIBE to the TEDx channel: http://bit.ly/1FAg8hB\n\nAs the Athletic Director and head coach of the Varsity Soccer team at Ryerson University, Dr. Joseph is often asked what skills he is searching for as a recruiter: is it speed? Strength? Agility? In Dr. Joseph's TEDx Talk, he explores self confidence and how it is not just the most important skill in athletics, but in our lives.\n \nIn the spirit of ideas worth spreading, TEDx is a program of local, self-organized events that bring people together to share a TED-like experience. At a TEDx event, TEDTalks video and live speakers combine to spark deep discussion and connection in a small group. These local, self-organized events are branded TEDx, where x = independently organized TED event. The TED Conference provides general guidance for the TEDx program, but individual TEDx events are self-organized.* (*Subject to certain rules and regulations)")
        self.assertIsNone(metadata['video_category'])
        self.assertEqual(metadata['video_thumbnail'], "https://i.ytimg.com/vi/w-HYZv6HzAs/hqdefault.jpg")

if __name__ == '__main__':
    unittest.main()
