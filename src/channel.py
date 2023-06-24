import json
import os
from googleapiclient.discovery import build
import isodate

FILE_NAME = 'moscowpython.json'

class Channel:
    """Класс для ютуб-канала"""


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscriberCount = None
        self.video_count = None
        self.viewCount = None


    @property
    def channel_id(self):
        return self.__channel_id


    def add_self_attr(self):

        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        channel_id = self.channel_id
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        data = channel['items']
        for i in data:
            self.title = i['snippet']['title']
            self.description = i['snippet']['description']
            self.url = i['snippet']['thumbnails']['default']['url']
            self.subscriberCount = i['statistics']['subscriberCount']
            self.video_count = i['statistics']['videoCount']
            self.viewCount = i['statistics']['viewCount']


    @classmethod
    def get_service(cls):
        "- класс-метод `get_service()`, возвращающий объект для работы с YouTube API"
        return cls.channel_id


    def to_json(self, filename):
        FILE_NAME = filename
        channel_info = {"title": self.title,
                        "channel_id": self.channel_id,
                        "description": self.description,
                        "url": self.url,
                        "count_podpishchikov": self.subscriberCount,
                        "video_count": self.video_count,
                        "count_views": self.viewCount}

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_info, file, indent=4, ensure_ascii=False)



    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        channel_id = self.channel_id
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))







