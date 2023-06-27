import os
from googleapiclient.discovery import build
from src.channel import Channel


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.title = None
        self.url = None
        self.view_count = None
        self.like_count = None
        self.comment_count = None

    def __str__(self):
        return f'{self.title}'

    def add_attr(self):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()

        self.title: str = video_response['items'][0]['snippet']['title']
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.url: str = video_response['items'][0]['snippet']['thumbnails']['default']['url']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']


class PLVideo(Video):
    def __init__(self, video_id, pl):
        super().__init__(video_id)
        self.pl = pl
