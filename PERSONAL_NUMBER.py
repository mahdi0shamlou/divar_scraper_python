import requests
from DataBase_manager import *
import time
import json


class DataFetcher:
    def __init__(self, url):
        self.url = url
        # self.data = data

    def fetch_json_data(self, token, jwt_token):
        headers = {
                    'Authorization': f'Basic {jwt_token}'
                }
        url_for_request = self.url + token[0]
        response = requests.get(url_for_request, headers=headers)
        print(f'\t {response.status_code}')
        response_json = response.json()
        return response_json, response.status_code, json.dumps(response_json)


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/postcontact/web/contact_info/'
    JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiI1NzNjNzVkZi1mZmI3LTRiNzQtYjg3MS0zZGE3OGI5ZGVhN2QiLCJ1c2VyLXR5cGUiOiJwZXJzb25hbCIsInVzZXItdHlwZS1mYSI6Ilx1MDY3ZVx1MDY0Nlx1MDY0NCBcdTA2MzRcdTA2MmVcdTA2MzVcdTA2Y2MiLCJ1aWQiOiJmYTdkY2VmOS04YmYwLTQ5NWItYmQyNi0yYzIwNzQyODQyNzIiLCJ1c2VyIjoiMDkyMDU1MDY5NDgiLCJpc3MiOiJhdXRoIiwidmVyaWZpZWRfdGltZSI6MTcyMzM4OTkzNSwiaWF0IjoxNzIzMzg5OTM1LCJleHAiOjE3Mjg1NzM5MzV9.ppouOeYBlbb2VDyBGl-084VKDtLybr5RkImSHhbQgTY'
    DB_FILENAME = 'posts.db'

