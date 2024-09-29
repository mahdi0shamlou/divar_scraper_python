from DataBase_manager import *
from POST_DATA_COMPLETER import GetToken, GetData
import time
import json
import mysql.connector





if __name__ == "__main__":
    DB_FILENAME = 'posts.db'
    objct_database = DatabaseManager(DB_FILENAME)