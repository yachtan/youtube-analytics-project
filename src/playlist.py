from googleapiclient.discovery import build
import os
import isodate
from datetime import timedelta


class PlayList:
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id
        # получаем данные по плэйлисту по его id
        self.playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                           part='contentDetails,snippet',
                                                                            maxResults=50).execute()
        # получаем из данных плэйлиста id канала
        self.channel_id = self.playlist_videos['items'][0]['snippet']['channelId']
        # получаем данные по всем плэйлистам канала
        self.playlists = PlayList.get_service().playlists().list(channelId=self.channel_id,part='contentDetails,snippet',
                                                                 maxResults=50).execute()
        # получаем все видеоролики из плэйлиста
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                                   id=','.join(self.video_ids)).execute()
        # находим наименование плэйлиста по его id
        for i in self.playlists['items']:
            if i['id'] == self.playlist_id:
                self.title = i['snippet']['title']

    @property
    def total_duration(self):
        """возвращает объект класса datetime.timedelta с суммарной длительность плейлиста
        (обращение как к свойству, использовать @property"""
        self.sum_duration = timedelta(hours=0, minutes=0)
        for video in self.video_response['items']:
            self.iso_8601_duration = video['contentDetails']['duration']
            self.duration = isodate.parse_duration(self.iso_8601_duration)
            self.sum_duration += self.duration
        return self.sum_duration

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        self.like_count = 0

        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > self.like_count:
                self.like_count = int(video['statistics']['likeCount'])
                self.like_video_url = 'https://youtu.be/' + video['id']

        return self.like_video_url






