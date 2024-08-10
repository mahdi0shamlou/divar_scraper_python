import requests
from DataBase_manager import *
from datetime import datetime
import time


class DataFetcher:
    def __init__(self, url):
        self.url = url
        #self.data = data

    def fetch_json_data(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/posts-v2/web/'
    DB_FILENAME = 'posts.db'
    dbs = DatabaseManager(DB_FILENAME)