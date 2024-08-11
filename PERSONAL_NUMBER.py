import requests
from DataBase_manager import *
import time
import json

class PostExtractor:
    @staticmethod
    def extract_post_data(json_data):
        """
        this methode extract only number
        :param json_data:
        :return:
        """
        number = ''
        for item in json_data.get('widget_list', []):
            if item.get('widget_type') == 'UNEXPANDABLE_ROW':
                # print(item.get('data'))
                if item.get('data')['action']['type'] == 'CALL_SUPPORT':
                    number = item.get('data')['action']['payload']['phone_number']
        return number

class DataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_json_data(self, token, jwt_token):
        headers = {
                    'Authorization': f'Basic {jwt_token}'
                }
        url_for_request = self.url + token[0]
        response = requests.get(url_for_request, headers=headers)
        print(f'\t {response.status_code}')
        response_json = response.json()
        return response_json, response.status_code, json.dumps(response_json)

class Application:
    def __init__(self, url, db_filename):
        self.fetcher = DataFetcher(url)
        self.extractor = PostExtractor()
        self.db_manager = DatabaseManager(db_filename)

    def run(self, JWT_TOKEN):
        tokens = self.db_manager.get_one_token_from_personal_details() # this method get a token from table for getting details
        print(f'\t this is token for search and getting number : {tokens}')
        json_data, status_code, all_data = self.fetcher.fetch_json_data(tokens, JWT_TOKEN) # this methode send request
        if status_code == 404:
            self.db_manager.update_post_data_in_posts(((tokens[0],)))
        number = self.extractor.extract_post_data(json_data) # this methode get number from response of above methode
        print(f'\t this is number of this post : {number}')
        post = ((tokens[0], all_data, number, 0))
        self.db_manager.save_number_of_personal(post)
        self.db_manager.update_post_personal_details(((tokens[0],)))



if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/postcontact/web/contact_info/'
    JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI1NzNjNzVkZi1mZmI3LTRiNzQtYjg3MS0zZGE3OGI5ZGVhN2QiLCJ1c2VyLXR5cGUiOiJwZXJzb25hbCIsInVzZXItdHlwZS1mYSI6Ilx1MDY3ZVx1MDY0Nlx1MDY0NCBcdTA2MzRcdTA2MmVcdTA2MzVcdTA2Y2MiLCJ1aWQiOiJmYTdkY2VmOS04YmYwLTQ5NWItYmQyNi0yYzIwNzQyODQyNzIiLCJ1c2VyIjoiMDkyMDU1MDY5NDgiLCJpc3MiOiJhdXRoIiwidmVyaWZpZWRfdGltZSI6MTcyMzM4OTkzNSwiaWF0IjoxNzIzMzg5OTM1LCJleHAiOjE3Mjg1NzM5MzV9.ppouOeYBlbb2VDyBGl-084VKDtLybr5RkImSHhbQgTY'
    DB_FILENAME = 'posts.db'
    app = Application(URL, DB_FILENAME)
    while True:
        try:
            print('Start of geting number of service')
            app.run(JWT_TOKEN)
            print('End of geting number of service')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            time.sleep(30)
            pass

