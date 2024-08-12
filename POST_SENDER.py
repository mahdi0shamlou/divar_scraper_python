import requests
from DataBase_manager import *
import time


class DataFetcher:
    def __init__(self, url):
        self.url = url
        # self.data = data

    def fetch_json_data(self, data):
        data_for_send = {
            'url' : 'https://divar.ir/v/' + data[0][0],
            'phone' : data[0][1],
            'status' : 0
        }
        headers = {
            'Cookie':'XSRF-TOKEN=eyJpdiI6IldIVS9XOEZlTFNmYXc4SFdpeXo1K3c9PSIsInZhbHVlIjoibFV5S1BZY3Z3ekVialp6MFdHM0c5TGd1UmsyYmUwQ2RRTGJyMGR3ODlPZ0QxMk5YNDRJVG00bVRxQVovditwVnFuUWc2WFlkWUcxNmtSVkE2b2tIOE9od2xVb1U1SFpjZ1A2QUIzai9iRXE1UDh2R2E3TmVyRXVBd2gxUHpza0kiLCJtYWMiOiJmYzYwZGU4ZmEwZjEzN2EwOGU0MzIwZTVhMjhjYzkxYWJlNGZmYzZiMzFjMWJmMGI2NDUyYjVhYmQxZmI1NDk3IiwidGFnIjoiIn0%3D; arkafile_session=eyJpdiI6IllxNkplaTA5amxVUUMvV1lmTng3VFE9PSIsInZhbHVlIjoidktZMEpITTlDODdJZUNvWktMWmtucUtGRmtpSGJmRXlmeVRBRUVkK0RwdEJ2R3E1ZnZ5eFpaZlgvaEVobk1OdU5MQWczNG0weDNidlVqWWkzTHdLMXQrTlpMMjhyWWpqajRuVjBoTHNWdG1GN1Faazh5WW9XakprT3A0TmNxOXMiLCJtYWMiOiIyNGM3MWI1NzI1NWUwOWYwZWJjMjY4NWYyNDc0OTBiNjcwYThiNjAwZTA5ZDU4NTVhYzQyMTYyNWQ3MjQxMTk1IiwidGFnIjoiIn0%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IldXR1BhOFV6b1pqYU1uWHIzQ0J0WFE9PSIsInZhbHVlIjoiV3hWV0YrUm9CMThZLzhsQWQvVHZTTU5iN2t1aVlEdUFQcFNwaTI3cXJQbUF4SkZsWXlZOFUxOFNEVGVSSWlwbS9vdnJYYmRFM3hLVlMzU3U0N0ZoYnVMOEdsM3B0cm56d2hiR3R6ckZFLzhWbXdyZFJtakF4eEluVElmUE1qeWhrSkIxMFpHMTlMeFl2MHZJYStMZGJnekZjODlycGJyQ1FOZmVIL2o2OTV6ODZxSkVyM1RVSFFRV3VZdnZ3bUF5aTNJb01NdDY5TmRmQ1FTZWNTNTVWRzZSWTFZRytzNUIwaHFkSEUrSmRCWT0iLCJtYWMiOiI4MDYxMzNmMjJmNjE3MTBhNGY1OThkMzNmMTg2ZDQxMjQwMjU0NWEzNmFjZWRhY2E1NzAwYTI0NTU2ZDE2MDE4IiwidGFnIjoiIn0%3D',
            'X-CSRF-TOKEN':'aA4luo7oobq1s5zCFZQpMObY3u0UfgkA1lEK889c'
        }
        print(f'\t {data_for_send}')
        response = requests.post(self.url, data=data_for_send, headers=headers)
        print(f'\t {response.status_code}')
        if status_code == 200 or status_code == 201:
            response_json = response.json()
            return response_json, response.status_code
        else:
            raise ValueError


class Application:
    def __init__(self, url, db_filename):
        self.fetcher = DataFetcher(url)
        self.db_manager = DatabaseManager(db_filename)

    def run(self):
        try:
            tokens = self.db_manager.get_number_personal_for_post_sender() # this method get a token from table for getting details
            print(f'\t this is items for post sender : {tokens}')
            response_json, status_code = self.fetcher.fetch_json_data(tokens) # this methode send request
            self.db_manager.update_number_personal_for_post_sender(((tokens[0][0],)))
        except ValueError:
            print('\t we have response is not 200 and 201')
            time.sleep(300) # this is using for after response is not 200 or 201
        except Exception as e:
            print(e)
            time.sleep(300) # this is run when a error happend in try block


if __name__ == "__main__":
    URL = 'https://arkafile.org/admin/file/store_divar_ads'
    DB_FILENAME = 'posts.db'
    app = Application(URL, DB_FILENAME)
    while True:
        try:
            print('Start of geting detials of service')
            app.run()
            print('End of geting detials of service')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            time.sleep(10)
            pass
