from googleapiclient.discovery import build
import os

class Video:
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    def __init__(self, video_id):
        self.video_id = video_id
        self.youtube = build('youtube', 'v3', developerKey=Video.api_key)
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=self.video_id).execute()
        #название видео
        self.video_title = self.video_response['items'][0]['snippet']['title']
        #ссылка на видео
        self.url = 'https://www.youtube.com/watch?v=' + self.video_id
        #количество просмотров
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        #количество лайков
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.video_title}'

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
