import requests
from DataBase_manager import *
import time

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
        url_for_request = self.url + token[0]
        response = requests.get(url_for_request)
        print(f'\t {response.status_code}')
        #response.raise_for_status()
        return response.json(), response.status_code


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
        tokens = self.db_manager.get_all_tokens_not_added() # this method get a token from table for getting details
        print(f'\t this is token for search and getting details : {tokens}')
        json_data, status_code = self.fetcher.fetch_json_data(tokens) # this methode send request
        if status_code == 404:
            self.db_manager.update_post_data_in_posts(((tokens[0],)))
        desck = self.extractor.extract_post_data(json_data) # this methode get desck from response of above methode
        desck_resualt = StringChecker.contains_any_first(desck[0], LIST_CHEKC) # this methode check if desck is valid or not
        print(f'\t this is reault of validtiy : {not desck_resualt}')
        post = ((tokens[0], desck[0], 0))
        if desck_resualt==False: # this conditon check desck is valid or not
            self.db_manager.save_post_data_details_personal(post) # this methode insert data into personal table
            self.db_manager.update_post_data_in_posts(((tokens[0],))) # this methode update row in posts table for dont get duplicat
        else:
            self.db_manager.save_post_data_details_moshaver(post) # this methode insert data into moshaver table
            self.db_manager.update_post_data_in_posts(((tokens[0],))) # this methode update row in posts table for dont get duplicat


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/posts-v2/web/'
    DB_FILENAME = 'posts.db'
    LIST_CHEKC = ['مشاور', 'املاک', 'مسکن'] # this list for useing for check validity
    app = Application(URL, DB_FILENAME)
    while True:
        try:
            print('Start of geting detials of service')
            app.run(LIST_CHEKC)
            print('End of geting detials of service')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            #time.sleep(3)
            pass

