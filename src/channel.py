import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API"""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале"""
        self.dict_to_print = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(self.dict_to_print, indent=2, ensure_ascii=False))
