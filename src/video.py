from googleapiclient.discovery import build
import os


class Video:
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, video_id):
        self.video_id = video_id
        # ссылка на видео
        self.url = 'https://www.youtube.com/watch?v=' + self.video_id

        self.video_response = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                id=self.video_id).execute()

        try:
            # название видео
            self.title = self.video_response['items'][0]['snippet']['title']
        except IndexError:
            self.title = None
            self.view_count = None
            self.like_count = None
        else:
            self.title = self.video_response['items'][0]['snippet']['title']
            # количество просмотров
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            # количество лайков
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
