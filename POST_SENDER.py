import requests
from DataBase_manager import *
from POST_DATA_COMPLETER import GetToken, GetData
import time


class DataFetcher:
    def __init__(self, url):
        self.url = url
        # self.data = data

    def fetch_json_data(self, data):
        data_for_send = {
            'url' : 'https://divar.ir/v/' + data[0][0],
            'phone' : data[0][1],
            'status' : 1
        }
        headers = {
            'Cookie':'arkafile_session=eyJpdiI6Im5tNzUzWVk2Q0t5RUduS1dobFNneEE9PSIsInZhbHVlIjoicjFUZ1hRMEVyR1BHT1dMczdtWmwrdmFNUFgxSHk5SVhLSWVQaitNeTlwVTVZaTFRUGhpN2duUXF6MnYrN1Z2TzhtMjQzaHZIenduL3p2ZUxhc29MY0RjUFRwRUJZSWJZZG8wQTc5RVZMRTF3eWNpUmRxczJ5blErTnpvYmxzbVIiLCJtYWMiOiIzMDEwZDMyMjRiZDBhN2M4ZWI4ZTllNTVkZWNiNzdmZTAxNWIzNTU5ZjVjMTVjNDcxNDE2YmJmZDE2NGU0OGRhIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6Imp3V3hlRGRRNEpSZGswMlI4dzh4YWc9PSIsInZhbHVlIjoiWEZWcHZBZnN0WUk4WTgwUWxUSkcxdnNPOTB6UjB6djU3eDhBL3REM1RpOStINmF1MnR2aEI3Z2dxZlVrVXpEOHFPb0hCYWl2dWErL2xOSjQ3cjB2QTAzZDdraCsrbE8rSUUzcGc5K25sc3I0RmJQbWxGUFBtZm5NMXZJU1lmekwiLCJtYWMiOiI1NDkwMzI3Yzg0ZTRlYjUwODE0YjkwOWIwNjgxMmRhMzczZDZmYjE1ZmRlMmFmYmM1NjNiM2RjYTA3MTM3MDZjIiwidGFnIjoiIn0%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IkpvR1pNNlprNFEvVzJCcE95L2t3dkE9PSIsInZhbHVlIjoiTkNpamNzWjVzc3o5SHR4WnUxSHpXdm8zMml0WjNOa2RicWwyeFB0YnlYcG1YWjBJSTVUank1T3BpcDJvbmprajVjdlBPQXRsTGJFazJwSTJjMzhlenI3cEI2ZlJ3ZytkRzBXVVIwTjgycmpPdWZrekNscWtKSCtXRzZSNzNoN3ZRaG5pTXkrcUhkVVZrdzNIdDR1Vjh3ZExHdlI3bGpnbGJMeW5IUTdITUZLTks0N29ES2tKdmY5VkNwS3dSMDBRQkZqek1rajF6eE5wR3dGZE94Wm9tT1orS0lMZHJZZXlycE1hTkkrYzdwRT0iLCJtYWMiOiJmYjZmODUzM2Q2YzQ5OWE3M2M3YmEzYTkwMzAwODc1Y2ZjMGRlODM3YzE3Njk3ZmIxNThmNDc4MTBiNTgzM2YzIiwidGFnIjoiIn0%3D',

            'X-CSRF-TOKEN':'BbfhYC6r0oqxGQW391oJXRNYVKLe3DCrto8ip6hp'
        }
        print(f'\t {data_for_send}')
        response = requests.post(self.url, data=data_for_send, headers=headers)

        print(f'\t {response.status_code}')
        if response.status_code == 200 or response.status_code == 201:
            response_json = response.json()
            return response_json, response.status_code
        else:
            raise ValueError


class Application:
    def __init__(self, url, db_filename):
        self.fetcher = DataFetcher(url)
        self.db_manager = DatabaseManager(db_filename)

    def run(self, object_token_get_data: GetToken):
        tokens = self.db_manager.get_number_personal_for_post_sender()  # this method get a token from table for getting details
        try:

            print(f'\t this is items for post sender : {tokens}')
            response_json, status_code = self.fetcher.fetch_json_data(tokens) # this methode send request
            self.db_manager.update_number_personal_for_post_sender(((tokens[0][0],)))
            retunred_Data_for_completer_data = object_token_get_data.Data_of_token(tokens[0][0]) # this line make data for save in db
            self.db_manager.save_post_data_compelete(retunred_Data_for_completer_data) # this line insert into table data_completer

        except ValueError:
            print('\t we have response is not 200 and 201')
            self.db_manager.update_number_personal_for_post_sender(((tokens[0][0],)))
            time.sleep(3) # this is using for after response is not 200 or 201
        except Exception as e:
            print(f'\t this is error {e}')
            self.db_manager.update_number_personal_for_post_sender(((tokens[0][0],)))
            time.sleep(3) # this is run when a error happend in try block



if __name__ == "__main__":
    URL = 'https://arkafile.org/admin/file/store_divar_ads'
    DB_FILENAME = 'posts.db'
    app = Application(URL, DB_FILENAME)
    object_data_compeleter = GetToken('just_verifiy')
    while True:
        try:
            print('Start of geting detials of service')
            app.run(object_data_compeleter)
            print('End of geting detials of service')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            time.sleep(4)
            pass
