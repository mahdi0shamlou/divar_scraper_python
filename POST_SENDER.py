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
            'Cookie':'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InpaRExHL280Tm9kVUpFT0s4aWtQdVE9PSIsInZhbHVlIjoiMUJ2cUlCbm5hTDdmNU4wRmFmMHVKMllHUEpFckpiUURua0Q5V2pMaU5DRmh5MHQ3TUQ2MlpXVWd6SXRINnA4UnlQOUJ1UmRDU2x1dXIvMG9wZ1RzSEdYMkd0eDRGUU5QeFpXdS9EZWFIeEN2TUhaRGhBcUc5TzIvZTRULzd4a1ViOS95L3lQNlFzblBoS29QVkU1V01wcUtYVEJ4SHJCR243N2FYbVdtY3hTOFBaQ2FCbTdlTXlJNWZWcklQSzk1cmI4d1lGdngyTXFrdkdhYkM3MHZFLzlueEhNcVZVWGUwV3FuMm9FT2pOVT0iLCJtYWMiOiIzNmI2NmQ0NDVmMjJiNTgxMWFhM2VlYjEyOGUyYmQ5ZjI2ZTJiZGM2OGEzMDNjNDAwMTFmNzJjNWMzOThlNWI0IiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6IjdORDZxS1p5enRIR3RtS0ZhZWR2eUE9PSIsInZhbHVlIjoiRXRlZkYxQU8za0crQk83VWUyV0pYYStzcnpkZGRMZFg5RU5Qd1hVMEtqQXRlWWwwQi9hYWt2ZXpDeU9QTkhkNEQ0NnhVZXdxN0h1NkpBK1NWcFg3My9td2FjM0gyTDRnM0dBeWR1anVCZ3BsbzBWcjJMdlVNUHhudmJ6R1VDZ2IiLCJtYWMiOiIwNTQ4ZjZjMzBmMzgzYTY2MTcyOWEyNmE5ZWUwNDVjZWY1YjY2MTZjZGJjZDRlZTJmY2IzYzg0YzdlZjQ1OGZmIiwidGFnIjoiIn0%3D; arkafile_session=eyJpdiI6IjlsUWJqb01vQTZ6R0M3Nkk0blI1RkE9PSIsInZhbHVlIjoiZFFSUmRwNVJZUnpkTGs1dDg1aFZ2M0MrSW1xZk5MQnB4S3I1NzVkNEpxa3BLZzR1VHFwa3lIc1BESll5V3dwM09SYjc1MkpFZWsrdWNhVzhRVW9WSC9oV0ZtMHcrVUtmNUo3WlA5ckc2cnQ3ajFERWJQcTZRL0Vqc2M4cWhSZm4iLCJtYWMiOiJjMTJkY2NkNTQ0MWM1YTRhNTAxYTU0ZWMyZWE4MDZkMGE2Y2QzN2ZjMzI1NWQyMDY4N2I2YWUxZGZjMjkxYTVlIiwidGFnIjoiIn0%3D',
            'X-CSRF-TOKEN':'5zmmYAxA60ueoiEVMewG6xnsCFJ9hiqj7UysUG7Y'
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
