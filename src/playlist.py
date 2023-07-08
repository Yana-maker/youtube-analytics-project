import os
from googleapiclient.discovery import build
import isodate
import datetime
from datetime import timedelta


class PlayList:
    ''' инициализируется _id_ плейлиста и имеет следующие публичные атрибуты:
    название плейлиста и ссылку на плейлист + id видео для функции'''
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        data = playlist['items']
        for i in data:
            title = i['snippet']['title']
            self.title = title.split('.'' ')[0]

        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist['items']]


    @property
    def total_duration(self):
        '''возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста'''
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(self.video_ids)
                                               ).execute()
        result = []
        total = 0
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            result.append(str(duration))

        for i in result:
            h, m, s = map(int, i.split(":"))
            total += 3600*h + 60*m + s
        s = "%02d:%02d:%02d" % (total/3600, total / 60 % 60, total % 60)
        t = datetime.datetime.strptime(s,"%H:%M:%S")
        delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
        return delta


    def show_best_video(self):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_ids
                                                       ).execute()

        popular_video = {}
        for i in video_response['items']:
            i = {
                i['id']: i['statistics']['viewCount']
            }
            popular_video = i

        return f"https://youtu.be/{max(popular_video, key=popular_video.get)}"





