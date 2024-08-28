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
            'Cookie':'arkafile_session=eyJpdiI6InU0YnlqUlBuS0pHYzgzR1VZaUxDbGc9PSIsInZhbHVlIjoibURQN0hZejBpM1lQU01JeW1DTm1NQzRzNytnd1ZtelFoQWExbWsraWF6TldIWm9wRzFZZlNVaHdIZStMOVBJSDBqNzUwNEtGQjROSmV4b1FjTGtxeUpkMU0wSlQxKy90NnZVdTZNQlpwM1grRU1zNXVpWlNPUkI4TjdzWWxBSzkiLCJtYWMiOiI0ZTU0MDQ2Y2NkZTJmZTAwZGRjNjkwYTgzNzkyNmRkNWNlNmNkZDFmODk3ZGRjY2QwOWQxMmM0ZWVmYWI4YTMwIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6IlBOWGVubEw5emlrL0k5SVFPWUZOaFE9PSIsInZhbHVlIjoiQWNNd3VORVFWbTRxeWhMQW1iREZVT28yUG5QQ0JkUWY3RkRXM1M0RWJzaElnblc1UHZOSTR2WW5ySEczRC9reVc4TWdiSG4vTFdtQXV6dWhmMm5PODFiUWJ1clpFK0IzNXVhYXlzcnR2OXcxK29qWWNRWDZBY2U2T0hjVDRQUmMiLCJtYWMiOiJlZTUyMmVlNWQ0MzhhYjg1MzZlOGEyNzYyMWE0ZDcyNGZhYmY3MDg0ODcwMGExMWQ2NGIzM2QxNDBjNzc4YjI5IiwidGFnIjoiIn0%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InlESElMUG14enhTUVlSNnFscVlyMHc9PSIsInZhbHVlIjoiMkZOUnk2RnZuQk9EMTBKdnFUeWxONkpKR2NFK1FaRjM4Y2F0c0RmRXBOUzJHNkVZblhpVG04cU5pQVBtK0VpaElHNWx3OGRHbHB1a3YvRUdtT0JBVmRUUWtOM1RDcXBWeUVMNkQ0OW0rSWpXN3B5T1B5aUZmLzRpRVRKUVVSSGJobnhQRFVTd2d5b2VYNERXeHpENTlxMmJ1enZhclQ1V2MxVWNlRGl0YitucThWaTNDQlZOZmVnNFVoODByL3RSS1drcVJtdEV5VHVpdHNtN3gxU2pyU0Y4Vmh4aVVSZlBCZmtEOEJyc1QzMD0iLCJtYWMiOiIyNWEzNDhkODE0ZmNjOTdhZGJlYTM4YmZmYjQ5Nzk0YjQ0NWYxODZlZTQwNmJmMmZmNmMyNjM5NjU5MjJjM2MzIiwidGFnIjoiIn0%3D',
            'X-CSRF-TOKEN':'nslJU6xoh46WpSuQndtcsjZgSUzv2ojdJXahpuWN'
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
