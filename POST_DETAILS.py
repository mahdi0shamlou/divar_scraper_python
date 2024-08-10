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
                for item2 in item.get('widgets', {}):
                    if item2.get('widget_type') == 'DESCRIPTION_ROW':
                        data = item2.get('data', {})['text']
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


class Application:
    def __init__(self, url, db_filename):
        self.fetcher = DataFetcher(url)
        self.extractor = PostExtractor()
        self.db_manager = DatabaseManager(db_filename)

    def run(self):
        json_data = self.fetcher.fetch_json_data()
        posts = self.extractor.extract_post_data(json_data)
        print(posts)
        # print(f"Saved/Checked {len(posts)} posts into the database.")


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/posts-v2/web/gZ3u1tbz'
    DB_FILENAME = 'posts.db'
    app = Application(URL, DB_FILENAME)
    dbs = DatabaseManager(DB_FILENAME)
    app.run()
