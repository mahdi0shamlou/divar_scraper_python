import requests
from DataBase_manager import *


class PostExtractor:
    @staticmethod
    def extract_post_data(json_data):
        """
        this methode extract only descriptions
        :param json_data:
        :return:
        """
        posts = []
        for item in json_data.get('sections', []):
            if item.get('section_name') == 'DESCRIPTION':
                data = item.get('widgets', {})
                posts.append(data)
        return posts


class DataFetcher:
    def __init__(self, url):
        self.url = url
        # self.data = data

    def fetch_json_data(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/posts-v2/web/'
    DB_FILENAME = 'posts.db'
    dbs = DatabaseManager(DB_FILENAME)
