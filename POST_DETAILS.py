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

    def fetch_json_data(self, token):
        self.url = self.url + token[0]
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()


class StringChecker:
    @staticmethod
    def contains_any_first(mainstring, substrings):
        """
        Check if the main string contains any of the provided substrings.
        Stops as soon as a match is found.
        :param mainstring: A string check for.
        :param substrings: A list of substrings to check for.
        :return: True if the main string contains any of the substrings, False otherwise.
        """
        for substring in substrings:
            if substring in mainstring:
                return True
        return False


class Application:
    def __init__(self, url, db_filename):
        self.fetcher = DataFetcher(url)
        self.extractor = PostExtractor()
        self.db_manager = DatabaseManager(db_filename)

    def run(self, LIST_CHEKC):
        tokens = self.db_manager.get_all_tokens_not_added()
        json_data = self.fetcher.fetch_json_data(tokens)
        desck = self.extractor.extract_post_data(json_data)
        desck_resualt = StringChecker.contains_any_first(desck[0], LIST_CHEKC)
        print(desck)
        print(desck_resualt)


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/posts-v2/web/'
    DB_FILENAME = 'posts.db'
    LIST_CHEKC = ['مشاور']
    app = Application(URL, DB_FILENAME)
    app.run(LIST_CHEKC)
