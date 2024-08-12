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
            'Cookie':'arkafile_session=eyJpdiI6IlQrSnNNNHlLQVRQZ1FaZ3d1ODNSV0E9PSIsInZhbHVlIjoianlXK0l6OXFhUE41ODZTTTRNYXlkM2FKOVZlc1ZKenk1aHA2SStQZ3A1cFFtZG94eCtMVWs2VHN0eEdTODJWL0FBcXFTWGRuald0czAzZXFRY1VncE0zUVNnRjloenZpZi85dCtFZXdTNk9WYk5wcFdLK0JwTVRiTmE3WG0ySGQiLCJtYWMiOiIxM2JjNDJjYmJkODgwMmMyOWIwMzg5NmIyNGU3ZTg2MTEyZDlkNTIzMzRkNmU5Zjc3Y2U3YTEzYTc3MzkzNjUzIiwidGFnIjoiIn0%3D; XSRF-TOKEN=eyJpdiI6Im44dHN2dlBqNTBPRHU4amMzRllSdVE9PSIsInZhbHVlIjoiYmJ4dXM5MFJXSExUTFE1KzdubE5yUFJkWWRQT2ZVSU43TjdZVis2eVFKNzZ2UUZHSjZsY3htMlkveTZzNXRVc250K00zQjhuRXEzTVE5dWFFUDNZUy9uZGE2ZHQvdlZYUndrS2VFMjVvMmFtY0YvVlJjNTVITFA4bGNBQUsvZXEiLCJtYWMiOiI3NGQ3YjQxYjUxYTA5MTgzZDUyNzE5MmMyMzIzNWZhZDYxNDBjYzIwZmMzMjQ2YmExMGRlZmM0MGI4NWFkNGU2IiwidGFnIjoiIn0%3D; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6InpaRExHL280Tm9kVUpFT0s4aWtQdVE9PSIsInZhbHVlIjoiMUJ2cUlCbm5hTDdmNU4wRmFmMHVKMllHUEpFckpiUURua0Q5V2pMaU5DRmh5MHQ3TUQ2MlpXVWd6SXRINnA4UnlQOUJ1UmRDU2x1dXIvMG9wZ1RzSEdYMkd0eDRGUU5QeFpXdS9EZWFIeEN2TUhaRGhBcUc5TzIvZTRULzd4a1ViOS95L3lQNlFzblBoS29QVkU1V01wcUtYVEJ4SHJCR243N2FYbVdtY3hTOFBaQ2FCbTdlTXlJNWZWcklQSzk1cmI4d1lGdngyTXFrdkdhYkM3MHZFLzlueEhNcVZVWGUwV3FuMm9FT2pOVT0iLCJtYWMiOiIzNmI2NmQ0NDVmMjJiNTgxMWFhM2VlYjEyOGUyYmQ5ZjI2ZTJiZGM2OGEzMDNjNDAwMTFmNzJjNWMzOThlNWI0IiwidGFnIjoiIn0%3D',
            'X-CSRF-TOKEN':'c55QsPf2uTcOEFI2kiEGFx3iYYk5XSu76L43tCAJ'
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

    def run(self):
        try:
            tokens = self.db_manager.get_number_personal_for_post_sender() # this method get a token from table for getting details
            print(f'\t this is items for post sender : {tokens}')
            response_json, status_code = self.fetcher.fetch_json_data(tokens) # this methode send request
            self.db_manager.update_number_personal_for_post_sender(((tokens[0][0],)))
        except ValueError:
            print('\t we have response is not 200 and 201')
            time.sleep(3) # this is using for after response is not 200 or 201
        except Exception as e:
            print(f'\t this is error {e}')
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
