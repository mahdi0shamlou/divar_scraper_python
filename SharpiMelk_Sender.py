import requests
from DataBase_manager import *
from POST_DATA_COMPLETER import GetToken, GetData
import time
import json
import mysql.connector

class InsertDataSharpiMelk:
    @staticmethod
    def inser_data_sell(posts):
        print(len(posts))
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ya mahdi',
            database='SharpiMelk',
            port=3306
        )

        param = (posts['token'],
                 posts['phone'],
                 posts['city'],
                 posts['city_text'],
                 0,
                 posts['mahal_text'],
                 posts['types'],
                 posts['title'],
                 posts['price'],
                 posts['meter'],
                 posts['desck'],
                 str(posts['map']),
                 str(posts['LIST_DATA']),
                 posts['GROUP_INFO_ROW'],
                 posts['UNEXPANDABLE_ROW'],
                 posts['GROUP_FEATURE_ROW']
                 )
        query = f"""INSERT INTO PostFileSell (token, `number`, city, city_text, mahal, mahal_text, `type`, title, price, meter, desck, `map`, details, GROUP_INFO_ROW, UNEXPANDABLE_ROW, GROUP_FEATURE_ROW) VALUES{param};"""
        cursor = connection.cursor()
        print(cursor.execute(query))
        connection.commit()


class GetDataFull:
    """
        this class get all data of one token
    """
    def __init__(self, token: str, data_base_connection: sqlite3.connect):
        self.Token = token
        self.DB_Conn = data_base_connection
        self.Data_full = {}

    def _get_from_posts(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM posts WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()

        self.Data_full['token'] = posts[0][1]
        self.Data_full['city_text'] = posts[0][4]

        if posts[0][4] == 'تهران':
            self.Data_full['city'] = 1
        elif posts[0][4] == 'کرج':
            self.Data_full['city'] = 2
        elif posts[0][4] == 'اندیشه':
            self.Data_full['city'] = 3
        elif posts[0][4] == 'فردیس':
            self.Data_full['city'] = 4
        self.Data_full['title'] = posts[0][2]
        self.Data_full['mahal_text'] = posts[0][3]

    def _get_from_personal_number(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM personal_number WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        self.Data_full['phone'] = posts[0][3]

    def _get_from_posts_details(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM posts_details_personal WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        full_data = json.loads(posts[0][3])

        self.Data_full['price'] = full_data['webengage']['price']
        self.Data_full['map'] = ''
        self.Data_full['meter'] = 0
        self.Data_full['otagh'] = 0
        self.Data_full['make'] = 0
        self.Data_full['UNEXPANDABLE_ROW'] = []
        self.Data_full['GROUP_INFO_ROW'] = []
        self.Data_full['GROUP_FEATURE_ROW'] = []
        for i in full_data['sections']:
            if i['section_name'] == 'MAP':
                self.Data_full['map'] = i
            elif i['section_name'] == 'LIST_DATA':
                self.Data_full['LIST_DATA'] = i

                for z in i['widgets']:
                    if z['widget_type'] == 'GROUP_INFO_ROW':
                        for x in z['data']['items']:
                            self.Data_full['GROUP_INFO_ROW'].append({x['title']:x['value']})
                            if x['title'] == 'متراژ':
                                self.Data_full['meter'] = int(x['value'])
                            if x['title'] == 'ساخت':
                                try:
                                    self.Data_full['make'] = int(x['value'])
                                except:
                                    self.Data_full['make'] = x['value']

                            if x['title'] == 'اتاق':
                                try:
                                    self.Data_full['otagh'] = int(x['value'])
                                except:
                                    self.Data_full['otagh'] = x['value']

                            print(x)
                    if z['widget_type'] == 'UNEXPANDABLE_ROW':

                        self.Data_full['UNEXPANDABLE_ROW'].append({z['data']['title']:z['data']['value']})

                    if z['widget_type'] == 'GROUP_FEATURE_ROW':
                        if 'action' in z['data']:
                            print(z['data']['action']['payload']['modal_page']['widget_list'])
                            datas = z['data']['action']['payload']['modal_page']['widget_list']
                            for x in datas:
                                print(x)
                                if x['widget_type'] == 'UNEXPANDABLE_ROW':
                                    self.Data_full['GROUP_FEATURE_ROW'].append({x['data']['title']: x['data']['value']})





            # print(i)
        print(self.Data_full['GROUP_INFO_ROW'])
        self.Data_full['GROUP_INFO_ROW'] = str(self.Data_full['GROUP_INFO_ROW'])
        self.Data_full['GROUP_INFO_ROW'] = self.Data_full['GROUP_INFO_ROW'].replace("'", '"')

        print(self.Data_full['UNEXPANDABLE_ROW'])
        self.Data_full['UNEXPANDABLE_ROW'] = str(self.Data_full['UNEXPANDABLE_ROW'])
        self.Data_full['UNEXPANDABLE_ROW'] = self.Data_full['UNEXPANDABLE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW'])
        self.Data_full['GROUP_FEATURE_ROW'] = str(self.Data_full['GROUP_FEATURE_ROW'])
        self.Data_full['GROUP_FEATURE_ROW'] = self.Data_full['GROUP_FEATURE_ROW'].replace("'", '"')


        self.Data_full['desck'] = posts[0][2]

    def _check(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM posts_details_personal WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        full_data = json.loads(posts[0][3])
        if full_data['analytics']['cat2'] == 'residential-sell':
            return 1
        if full_data['analytics']['cat2'] == 'residential-rent':
            return 2
        if full_data['analytics']['cat2'] == 'commercial-sell':
            return 3
        if full_data['analytics']['cat2'] == 'commercial-rent':
            return 4

        return 0

    def get_data(self):
        self.db_manager = DatabaseManager('posts.db')
        x = self._check()
        if x == 1:
            print(f'\t this a sell file')
            self.Data_full['types'] = 1
            self._get_from_posts()
            self._get_from_personal_number()
            self._get_from_posts_details()
            InsertDataSharpiMelk.inser_data_sell(self.Data_full)
            self.db_manager.update_token_for_sharpi_melk(((self.Token,)))
        elif x == 2:
            print('rent')
            self.db_manager.update_token_for_sharpi_melk(((self.Token,)))
        elif x == 3:
            print(f'\t this a sell tejaryi file')
            self.Data_full['types'] = 3
            self._get_from_posts()
            self._get_from_personal_number()
            self._get_from_posts_details()
            InsertDataSharpiMelk.inser_data_sell(self.Data_full)
            self.db_manager.update_token_for_sharpi_melk(((self.Token,)))

        elif x == 4:
            print('rent tejary')
            self.db_manager.update_token_for_sharpi_melk(((self.Token,)))
        else:
            print('none')
            self.db_manager.update_token_for_sharpi_melk(((self.Token,)))



class Application:
    def __init__(self, db_filename):
        self.db_manager = DatabaseManager(db_filename)

    def run(self, CONNECTION_DB: sqlite3.connect):
        tokens = self.db_manager.get_token_for_sharpi_melk()  # this method get a token from table for getting details
        oject_data_completer = GetDataFull(tokens[0][0], CONNECTION_DB)
        data = oject_data_completer.get_data()
        print(data)


if __name__ == "__main__":
    DB_FILENAME = 'posts.db'
    app = Application(DB_FILENAME)
    DATABASE = 'posts.db'
    CONNECTION_DB = sqlite3.connect(DATABASE)
    print('Start of geting detials of service')
    app.run(CONNECTION_DB)
    print('End of geting detials of service')
    while True:
        try:
            print('Start of geting detials of service')
            app.run(CONNECTION_DB)
            print('End of geting detials of service')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            time.sleep(1)
            pass





