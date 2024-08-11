import requests
from DataBase_manager import *
import time


class DataFetcher:
    def __init__(self, url):
        self.url = url
        # self.data = data

    def fetch_json_data(self, data):
        response = requests.post(self.url, data=data)
        print(f'\t {response.status_code}')
        response_json = response.json()
        return response_json



if __name__ == "__main__":

    pass