import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API"""
        self.__channel_id = channel_id
        self.dict_info = Channel.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        #название канала
        self.title = self.dict_info["items"][0]["snippet"]["title"]
        #описание канала
        self.description = self.dict_info["items"][0]["snippet"]["description"]
        #ссылка на канал
        self.url = 'https://www.youtube.com/channel/' + self.channel_id
        #количество подписчиков
        self.subscriber_count = self.dict_info["items"][0]["statistics"]["subscriberCount"]
        #количество видео
        self.video_count = self.dict_info["items"][0]["statistics"]["videoCount"]
        #общее количество просмотров
        self.view_count = self.dict_info["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале"""
        self.dict_to_print = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(self.dict_to_print, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, json_name):
        """Сохраняет в файл json значения атрибутов экземпляра данного класса"""
        data = {"channel_id": self.channel_id, "title": self.title, "description": self.description,
                "url": self.url, "subscriber_count": self.subscriber_count, "video_count": self.video_count,
                "view_count": self.view_count}
        with open(json_name, 'w', encoding='utf-8') as file:
            json.dump(data, file)
