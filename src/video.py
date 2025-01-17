import os
from googleapiclient.discovery import build
from src.channel import Channel

class Video:
    def __init__(self, video_id):
        try:
            self.video_id = video_id
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

        except IndexError:
            self.title: str = None
            self.view_count: int = None
            self.url: str = None
            self.like_count: int = None
            self.comment_count: int = None


    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, pl):
        super().__init__(video_id)
        self.pl = pl


