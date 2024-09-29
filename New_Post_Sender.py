from DataBase_manager import *
from POST_DATA_COMPLETER import GetToken, GetData
import time
import json
import mysql.connector



class Application:
    def __init__(self, db_filename, list_category):
        self.db_manager = DatabaseManager(db_filename)
        self.list_category = list_category

    def run(self, CONNECTION_DB: sqlite3.connect):
        pass


if __name__ == "__main__":
    DB_FILENAME = 'posts.db'
    list_category = []

    CONNECTION_DB = sqlite3.connect(DB_FILENAME)
    app = Application(DB_FILENAME, list_category)
    while True:
        try:
            print('Start of sending post in service')
            app.run(CONNECTION_DB)
            print('End of sending post in of service')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            time.sleep(1)
            pass
