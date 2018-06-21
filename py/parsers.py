import json
import datetime
from collections import OrderedDict
from youtube_api_utils import parse_yt_datetime     
     
    
def default(item):
    '''
    Returns the input
    '''
    return item
    
def parse_video_metadata(item):
    '''
    Parses a JSON object for relevant fields
    '''    
    video_meta = OrderedDict(
        video_id = item['id'],
        channel_title = item["snippet"].get("channelTitle"),
        channel_id =item["snippet"].get("channelId"),
        video_publish_date = parse_yt_datetime(item["snippet"].get("publishedAt")),
        video_title = item["snippet"].get("title"),
        video_description = item["snippet"].get("description"),
        video_category = item["snippet"].get("categoryId"),
        video_view_count = item["statistics"].get("viewCount"),
        video_comment_count = item["statistics"].get("commentCount"),
        video_like_count = item["statistics"].get("likeCount"),
        video_dislike_count = item["statistics"].get("dislikeCount"),
        video_thumbnail = item["snippet"]["thumbnails"]["high"]["url"],
        video_tags =  '|'.join(item["snippet"].get('tags')),
        collection_date = datetime.datetime.now()
    )
    
    return video_meta


def parse_video_url(item):
    '''
    Returns a `video_id` and a `publish_date`
    from a json object from `get_video_urls_from_playlist_id`
    '''
    publish_date = item['snippet'].get('publishedAt')
    publish_date = parse_yt_datetime(publish_date)
    video_id = item['snippet']['resourceId'].get('videoId')
    channel_id = item['snippet'].get('channelId')
    
    return OrderedDict(
        publish_date = publish_date,
        video_id = video_id,
        channel_id = channel_id,
        collection_date = datetime.datetime.now()
    )


def parse_channel_metadata(item):
    '''
    Parses a JSON object for relevant fields
    '''
    topic = item.get('topicDetails')
    if topic:
        topic =  item.get('topicIds')
    channel_meta = OrderedDict(
        id = item['id'],
        title = item["snippet"].get("title"),
        publish_date = parse_yt_datetime(item["snippet"].get("publishedAt")),
        keywords = item['brandingSettings']['channel'].get('keywords'),
        description = item["snippet"].get("description"),
        view_count = item["statistics"].get("viewCount"),
        video_count = item["statistics"].get("videoCount"),
        subscription_count = item["statistics"].get("subscriberCount"),
        playlist_id_likes = item['contentDetails']['relatedPlaylists'].get('likes'),
        playlist_id_uploads = item['contentDetails']['relatedPlaylists'].get('uploads'),
        topic_ids = json.dumps(topic),
        collection_date = datetime.datetime.now()
    )
    
    return channel_meta


def parse_subscription_descriptive(item):
    sub_meta = OrderedDict(
        subscription_title = item['snippet']['title'],
        subscription_channel_id = item['snippet']['resourceId'].get('channelId'),
        subscription_kind = item['snippet']['resourceId'].get('kind'),
        subscription_publish_date = parse_yt_datetime(item['snippet'].get('publishedAt')),  
        collection_date = datetime.datetime.now()
    )
    
    return sub_meta


def parse_featured_channels(item):
    d = {}
    d[item['id']] = item['brandingSettings']['channel'].get('featuredChannelsUrls', [])
    return d


def parse_playlist_metadata(item):
    playlist_meta = OrderedDict(
        playlist_name = item['snippet'].get('title'),
        playlist_id = item['id'],
        playlist_publish_date = parse_yt_datetime(item['snippet'].get('publishedAt')),
        playlist_n_videos = item['contentDetails'].get('itemCount'),
        channel_id = item['snippet'].get('channelId'),
        channel_name = item['snippet'].get('channelTitle'),
        collection_date = datetime.datetime.now()

    )
    
    return playlist_meta


def parse_comment_metadata(item):
    """
    Parses JSON object for comment metadata

    """

    if item['snippet'].get('topLevelComment'):
        save = item['snippet']
        item = item['snippet']['topLevelComment']
        
    comment_meta = OrderedDict(
        commenter_channel_url = item["snippet"].get("authorChannelUrl"),
        commenter_channel_display_name = item['snippet'].get('authorDisplayName'),
        comment_id = item.get("id"),
        comment_like_count = item["snippet"].get("likeCount"),
        comment_publish_date = parse_yt_datetime(item["snippet"].get("publishedAt")),
        text = item["snippet"].get("textDisplay"),
        video_id = item["snippet"].get("videoId"),
        commenter_rating = item["snippet"].get("viewerRating"),
        comment_parent_id = item["snippet"].get("parentId"),
        collection_date = datetime.datetime.now()
    )
    try:
        comment_meta['reply_count'] = save.get('totalReplyCount')
    except:
        comment_meta['reply_count'] = item.get('totalReplyCount')
        
    return comment_meta


def parse_rec_video_metadata(item):
    '''
    Parses a JSON object for relevant fields
    '''    
    video_meta = OrderedDict(
        video_id = item['id'].get('videoId'),
        channel_title = item["snippet"].get("channelTitle"),
        channel_id =item["snippet"].get("channelId"),
        video_publish_date = parse_yt_datetime(item["snippet"].get("publishedAt")),
        video_title = item["snippet"].get("title"),
        video_description = item["snippet"].get("description"),
        video_category = item["snippet"].get("categoryId"),
        video_thumbnail = item["snippet"]["thumbnails"]["high"]["url"],
        collection_date = datetime.datetime.now()
    )
    
    return video_meta

def parse_caption_track(item):
    
    caption_meta = OrderedDict(
        video_id = item['video_id'],
        caption = item['caption'],
        collection_date = item['collection_date']
    )
    
    return caption_meta
