import requests
from DataBase_manager import *
import time
import json
import csv

class Erro400fromdivar(Exception):
    pass


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
                    'Host':'api.divar.ir',
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br, zstd',
                    'Referer': 'https://divar.ir/',
                    'Origin': 'https://divar.ir/',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-site',
                    'Authorization': f'Basic {jwt_token}',
                    'Connection':'keep-alive'
                }
        url_for_request = self.url + token[0]
        response = requests.get(url_for_request, headers=headers)
        print(f'\t {response.status_code}')
        if response.status_code == 200:
            response_json = response.json()
            return response_json, response.status_code, json.dumps(response_json)
        elif response.status_code == 400 or response.status_code == 403 or response.status_code == 402 or response.status_code == 401:
            print(response.json())
            raise Erro400fromdivar
        elif response.status_code == 404:
            print(response.json())
            raise ValueError
        else:
            print(f'\t this token removed {token[0]}')
            print(response.json())
            raise Erro400fromdivar # raise a exception for handel response

class Application:
    def __init__(self, url, db_filename):
        self.fetcher = DataFetcher(url)
        self.extractor = PostExtractor()
        self.db_manager = DatabaseManager(db_filename)

    def run(self, JWT_TOKEN, counter):
        try:
            tokens = self.db_manager.get_one_token_from_personal_details() # this method get a token from table for getting details
            print(f'\t this is token for search and getting number : {tokens}')
            json_data, status_code, all_data = self.fetcher.fetch_json_data(tokens, JWT_TOKEN) # this methode send request
            number = self.extractor.extract_post_data(json_data) # this methode get number from response of above methode
            print(f'\t this is number of this post : {number}')
            number_data_from_moshaver_number_table = self.db_manager.get_number_from_moshaver_number_table(((number,)))
            if len(number_data_from_moshaver_number_table) == 0:
                print(f'\t this number is not one of the moshavers :) : {number}')
                print(f'\t this is resault of selectin from moshaver number : {number_data_from_moshaver_number_table}')
                post = ((tokens[0], all_data, number, 0))
                self.db_manager.save_number_of_personal(post)
                self.db_manager.update_post_personal_details(((tokens[0],)))
                print('update counter ')
                self.db_manager.update_token_counter_of_divar_for_personal_number(((str(int(counter)+1), JWT_TOKEN)))
                print('end counter ')
            else:
                print(f'\t this number is in table of moshaver number : {number_data_from_moshaver_number_table}')
                self.db_manager.update_post_personal_details(((tokens[0],)))
                self.db_manager.update_token_counter_of_divar_for_personal_number(((str(int(counter)+1), JWT_TOKEN)))
                print(f'\t Update this number as moshaver :( ')
        except Erro400fromdivar:
            print(f'\t thispost return not 200 and like it is 403 400 and nothing else')
            self.db_manager.update_token_counter_of_divar_for_personal_number_where_blocked(((counter, JWT_TOKEN)))
            time.sleep(10)
        except ValueError:
            print(f'\t response of divar is not 200')
            print(f'\t this token update for dont get agian {tokens[0]}')
            self.db_manager.update_token_counter_of_divar_for_personal_number(((str(int(counter) + 1), JWT_TOKEN)))
            self.db_manager.update_post_personal_details(((tokens[0],))) # this is using for after response is not 200
        except Exception as e:
            print(f'\t we have a error in try block')
            print(e)
            self.db_manager.update_token_counter_of_divar_for_personal_number(((str(int(counter) + 1), JWT_TOKEN)))
            self.db_manager.update_post_personal_details(((tokens[0],))) # this is run when a error happend in try block

class JWTTokenReader:
    def __init__(self, filename):
        self.filename = filename
        self.tokens = []

    def read_tokens(self):
        try:
            with open(self.filename, mode='r', newline='') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    # Assuming the JWT token is the first element in each row
                    token = row[0]
                    self.tokens.append(token)
            print("Tokens read successfully!")
        except FileNotFoundError:
            print(f"Error: The file {self.filename} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_tokens(self):
        return self.tokens


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/postcontact/web/contact_info/'
    JWT_TOKEN_FILE = 'Files/JWT_tokens.csv'
    DB_FILENAME = 'posts.db'
    # --------
    # jwt token reader
    # --------
    ''' OLD version
    JWT_object = JWTTokenReader(JWT_TOKEN_FILE)
    JWT_object.read_tokens()
    JWT_TOKEN_LIST = JWT_object.get_tokens()
    '''
    '''NEW version'''
    obj_db_jwt_tokens = DatabaseManager(DB_FILENAME)
    JWT_TOKEN_LIST = obj_db_jwt_tokens.get_token_of_divar_for_personal_number()
    print(f'this is len of jwttoeknnuumber : {len(JWT_TOKEN_LIST)}')
    # --------
    # --------
    app = Application(URL, DB_FILENAME)
    i = 0
    while True:
        try:
            JWT_TOKEN = JWT_TOKEN_LIST[i][0]
            print(JWT_TOKEN)
            print('Start of geting number of service')
            app.run(JWT_TOKEN, JWT_TOKEN_LIST[i][1])
            print('End of geting number of service')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            i = i + 1
            i = i % len(JWT_TOKEN_LIST)
            time.sleep(90)


