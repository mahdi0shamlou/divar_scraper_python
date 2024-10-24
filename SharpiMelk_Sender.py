from DataBase_manager import *
import time
import json
import mysql.connector
import jdatetime

class InsertDataSharpiMelk:
    @staticmethod
    def inser_data_sell(posts):
        print(len(posts))
        connection = mysql.connector.connect(
            host='185.19.201.97',
            user='root_sharpi_melk_gelobal',
            password='ya mahdi',
            database='SharpiMelk',
            port=3306
        )
        persian_date = jdatetime.date.today().strftime("%Y/%m/%d %H:%M:%S")
        param = (posts['token'],
                 posts['phone'],
                 posts['city'],
                 posts['city_text'],
                 posts['mahal'],
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
                 posts['GROUP_FEATURE_ROW'],
                 posts['GROUP_FEATURE_ROW_items'],
                 posts['GROUP_FEATURE_ROW_more_details'],
                 posts['Images'],
                 posts['Otagh'],
                 posts['make'],
                posts['PARKING'],
                posts['ELEVATOR'],
                posts['CABINET'],
                 persian_date
                 )
        query = f"""INSERT INTO PostFileSell (token, `number`, city, city_text, mahal, mahal_text, `type`, title, price, meter, desck, `map`, details, GROUP_INFO_ROW, UNEXPANDABLE_ROW, GROUP_FEATURE_ROW, GROUP_FEATURE_ROW_items, GROUP_FEATURE_ROW_more_details, Images, Otagh, Make_years, PARKING, ELEVATOR, CABINET, date_created_persian) VALUES{param};"""
        cursor = connection.cursor()
        print(cursor.execute(query))
        connection.commit()
    @staticmethod
    def inser_data_rent(posts):
        print(len(posts))
        connection = mysql.connector.connect(
            host='185.19.201.97',
            user='root_sharpi_melk_gelobal',
            password='ya mahdi',
            database='SharpiMelk',
            port=3306
        )
        persian_date = jdatetime.date.today().strftime("%Y/%m/%d %H:%M:%S")
        param = (posts['token'],
                 posts['phone'],
                 posts['city'],
                 posts['city_text'],
                 posts['mahal'],
                 posts['mahal_text'],
                 posts['types'],
                 posts['title'],
                 posts['credit'],
                 posts['rent'],
                 posts['meter'],
                 posts['desck'],
                 str(posts['map']),
                 str(posts['LIST_DATA']),
                 posts['GROUP_INFO_ROW'],
                 posts['UNEXPANDABLE_ROW'],
                 posts['GROUP_FEATURE_ROW'],
                 posts['GROUP_FEATURE_ROW_items'],
                 posts['GROUP_FEATURE_ROW_more_details'],
                 posts['Images'],
                 posts['Otagh'],
                 posts['make'],
                 posts['PARKING'],
                 posts['ELEVATOR'],
                 posts['CABINET'],
                 persian_date
                 )
        query = f"""INSERT INTO PostFileRent (token, `number`, city, city_text, mahal, mahal_text, `type`, title, price, rent, meter, desck, `map`, details, GROUP_INFO_ROW, UNEXPANDABLE_ROW, GROUP_FEATURE_ROW, GROUP_FEATURE_ROW_items, GROUP_FEATURE_ROW_more_details, Images, Otagh, Make_years, PARKING, ELEVATOR, CABINET, date_created_persian) VALUES{param};"""
        cursor = connection.cursor()
        print(cursor.execute(query))
        connection.commit()


class GetDataFull:
    """
        this class get all data of one token
    """
    def __init__(self, token: str, data_base_connection: sqlite3.connect, list_mahal):
        self.Token = token
        self.DB_Conn = data_base_connection
        self.Data_full = {}
        self.list_mahal = list_mahal

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
        self.Data_full['title'] = posts[0][2].replace('\u200c', ' ')
        self.Data_full['mahal_text'] = posts[0][3].replace('\u200c', ' ')

        self.Data_full['mahal'] = 0

        if self.Data_full['city'] == 1:
            for i in self.list_mahal:
                if self.Data_full['mahal_text'] == i[1] and i[3] == 1:
                    print(f'\t this mahal {i}')
                    self.Data_full['mahal'] = i[2]
        elif self.Data_full['city'] == 2:
            for i in self.list_mahal:
                if self.Data_full['mahal_text'] == i[1] and i[3] == 2:
                    print(f'\t this mahal {i}')
                    self.Data_full['mahal'] = i[2]

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
        self.Data_full['Otagh'] = 0
        self.Data_full['make'] = 0
        self.Data_full['UNEXPANDABLE_ROW'] = []
        self.Data_full['GROUP_INFO_ROW'] = []
        self.Data_full['GROUP_FEATURE_ROW'] = []
        self.Data_full['GROUP_FEATURE_ROW_items'] = []
        self.Data_full['GROUP_FEATURE_ROW_more_details'] = []
        self.Data_full['Images'] = []
        for i in full_data['sections']:
            if i['section_name'] == 'MAP':
                self.Data_full['map'] = i
            #---------------------------------------------------
            elif i['section_name'] == 'IMAGE':
                for z in i['widgets']:
                    if z['widget_type'] == 'IMAGE_CAROUSEL':
                        for x in z['data']['items']:
                            self.Data_full['Images'].append(x['image']['url'])
            # ---------------------------------------------------
            elif i['section_name'] == 'LIST_DATA':
                self.Data_full['LIST_DATA'] = i
                for z in i['widgets']:
                    if z['widget_type'] == 'GROUP_INFO_ROW':
                        for x in z['data']['items']:
                            self.Data_full['GROUP_INFO_ROW'].append({x['title']:x['value']})
                            if x['title'] == 'متراژ':
                                try:
                                    self.Data_full['meter'] = int(x['value'])
                                except:
                                    if "متر" in x['value']:
                                        self.Data_full['meter'] = int(x['value'][:-3])
                            if x['title'] == 'ساخت':
                                try:
                                    self.Data_full['make'] = int(x['value'])
                                except:
                                    if x['value'] == "قبل از ۱۳۷۰":
                                        self.Data_full['make'] = 1370

                            if x['title'] == 'اتاق':
                                try:
                                    self.Data_full['Otagh'] = int(x['value'])
                                except:
                                    if x['value'] == 'بدون اتاق':
                                        self.Data_full['Otagh'] = 0
                                    else:
                                        self.Data_full['Otagh'] = 4

                            print(x)
                    if z['widget_type'] == 'UNEXPANDABLE_ROW':
                        self.Data_full['UNEXPANDABLE_ROW'].append({z['data']['title'].replace('\u200c', ' '):z['data']['value'].replace('\u200c', ' ')})
                        if z['data']['title'] == 'متراژ':
                            try:
                                self.Data_full['meter'] = int(z['data']['value'])
                            except Exception as e:
                                if "متر" in z['data']['value']:
                                    meter_vales = z['data']['value'].replace("٬", '')
                                    self.Data_full['meter'] = int(meter_vales[:-3])
                    if z['widget_type'] == 'GROUP_FEATURE_ROW':
                        if 'items' in z['data']:
                            for i in z['data']['items']:
                                if 'available' in i:

                                    self.Data_full['GROUP_FEATURE_ROW_items'].append({i['icon']['icon_name']: i['available']})
                        if 'action' in z['data']:
                            print(z['data']['action']['payload']['modal_page']['widget_list'])
                            datas = z['data']['action']['payload']['modal_page']['widget_list']
                            for x in datas:
                                print(x)
                                if x['widget_type'] == 'UNEXPANDABLE_ROW':
                                    self.Data_full['GROUP_FEATURE_ROW'].append({x['data']['title'].replace('\u200c', ' '): x['data']['value'].replace('\u200c', ' ')})
                                if x['widget_type'] == 'FEATURE_ROW':
                                    self.Data_full['GROUP_FEATURE_ROW_more_details'].append(x['data']['title'].replace('\u200c', ' '))
        print(self.Data_full['GROUP_INFO_ROW'])
        self.Data_full['GROUP_INFO_ROW'] = str(self.Data_full['GROUP_INFO_ROW'])
        self.Data_full['GROUP_INFO_ROW'] = self.Data_full['GROUP_INFO_ROW'].replace("'", '"')
        print(self.Data_full['UNEXPANDABLE_ROW'])
        self.Data_full['UNEXPANDABLE_ROW'] = str(self.Data_full['UNEXPANDABLE_ROW'])
        self.Data_full['UNEXPANDABLE_ROW'] = self.Data_full['UNEXPANDABLE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW'])
        self.Data_full['GROUP_FEATURE_ROW'] = str(self.Data_full['GROUP_FEATURE_ROW'])
        self.Data_full['GROUP_FEATURE_ROW'] = self.Data_full['GROUP_FEATURE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW_items'])
        self.Data_full['PARKING'] = 0
        self.Data_full['ELEVATOR'] = 0
        self.Data_full['CABINET'] = 0
        for i in self.Data_full['GROUP_FEATURE_ROW_items']:
            for (key, value) in i.items():
                self.Data_full[key] = value

        self.Data_full['GROUP_FEATURE_ROW_items'] = str(self.Data_full['GROUP_FEATURE_ROW_items'])
        self.Data_full['GROUP_FEATURE_ROW_items'] = self.Data_full['GROUP_FEATURE_ROW_items'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW_more_details'])
        self.Data_full['GROUP_FEATURE_ROW_more_details'] = str(self.Data_full['GROUP_FEATURE_ROW_more_details'])
        self.Data_full['GROUP_FEATURE_ROW_more_details'] = self.Data_full['GROUP_FEATURE_ROW_more_details'].replace("'", '"')
        print(self.Data_full['Images'])
        self.Data_full['Images'] = str(self.Data_full['Images'])
        self.Data_full['Images'] = self.Data_full['Images'].replace("'",'"')

        self.Data_full['desck'] = posts[0][2]


    def _get_from_posts_details_rent(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM posts_details_personal WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        full_data = json.loads(posts[0][3])
        self.Data_full['credit'] = full_data['webengage']['credit']
        self.Data_full['rent'] = full_data['webengage']['rent']
        self.Data_full['map'] = ''
        self.Data_full['meter'] = 0
        self.Data_full['Otagh'] = 0
        self.Data_full['make'] = 0
        self.Data_full['UNEXPANDABLE_ROW'] = []
        self.Data_full['GROUP_INFO_ROW'] = []
        self.Data_full['GROUP_FEATURE_ROW'] = []
        self.Data_full['GROUP_FEATURE_ROW_items'] = []
        self.Data_full['GROUP_FEATURE_ROW_more_details'] = []
        self.Data_full['Images'] = []
        for i in full_data['sections']:
            if i['section_name'] == 'MAP':
                self.Data_full['map'] = i
            #---------------------------------------------------
            elif i['section_name'] == 'IMAGE':
                for z in i['widgets']:
                    if z['widget_type'] == 'IMAGE_CAROUSEL':
                        for x in z['data']['items']:
                            self.Data_full['Images'].append(x['image']['url'])
            # ---------------------------------------------------
            elif i['section_name'] == 'LIST_DATA':
                self.Data_full['LIST_DATA'] = i
                for z in i['widgets']:
                    if z['widget_type'] == 'GROUP_INFO_ROW':
                        for x in z['data']['items']:
                            self.Data_full['GROUP_INFO_ROW'].append({x['title']:x['value']})
                            if x['title'] == 'متراژ':
                                try:
                                    self.Data_full['meter'] = int(x['value'])
                                except:
                                    if "متر" in x['value']:
                                        self.Data_full['meter'] = int(x['value'][:-3])

                            if x['title'] == 'ساخت':
                                try:
                                    self.Data_full['make'] = int(x['value'])
                                except:
                                    if x['value'] == "قبل از ۱۳۷۰":
                                        self.Data_full['make'] = 1370
                            if x['title'] == 'اتاق':
                                try:
                                    self.Data_full['Otagh'] = int(x['value'])
                                except:
                                    if x['value'] == 'بدون اتاق':
                                        self.Data_full['Otagh'] = 0
                                    else:
                                        self.Data_full['Otagh'] = 4

                            print(x)
                    if z['widget_type'] == 'UNEXPANDABLE_ROW':
                        self.Data_full['UNEXPANDABLE_ROW'].append({z['data']['title'].replace('\u200c', ' '):z['data']['value'].replace('\u200c', ' ')})
                        if z['data']['title'] == 'متراژ':
                            try:
                                self.Data_full['meter'] = int(z['data']['value'])
                            except Exception as e:
                                if "متر" in z['data']['value']:
                                    meter_vales = z['data']['value'].replace("٬", '')
                                    self.Data_full['meter'] = int(meter_vales[:-3])
                    if z['widget_type'] == 'GROUP_FEATURE_ROW':
                        if 'items' in z['data']:
                            for i in z['data']['items']:
                                if 'available' in i:
                                    self.Data_full['GROUP_FEATURE_ROW_items'].append({i['icon']['icon_name']: i['available']})
                        if 'action' in z['data']:
                            print(z['data']['action']['payload']['modal_page']['widget_list'])
                            datas = z['data']['action']['payload']['modal_page']['widget_list']
                            for x in datas:
                                print(x)
                                if x['widget_type'] == 'UNEXPANDABLE_ROW':
                                    self.Data_full['GROUP_FEATURE_ROW'].append({x['data']['title'].replace('\u200c', ' '): x['data']['value'].replace('\u200c', ' ')})
                                if x['widget_type'] == 'FEATURE_ROW':
                                    self.Data_full['GROUP_FEATURE_ROW_more_details'].append(x['data']['title'].replace('\u200c', ' '))

        print(self.Data_full['GROUP_INFO_ROW'])
        self.Data_full['GROUP_INFO_ROW'] = str(self.Data_full['GROUP_INFO_ROW'])
        self.Data_full['GROUP_INFO_ROW'] = self.Data_full['GROUP_INFO_ROW'].replace("'", '"')
        print(self.Data_full['UNEXPANDABLE_ROW'])
        self.Data_full['UNEXPANDABLE_ROW'] = str(self.Data_full['UNEXPANDABLE_ROW'])
        self.Data_full['UNEXPANDABLE_ROW'] = self.Data_full['UNEXPANDABLE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW'])
        self.Data_full['GROUP_FEATURE_ROW'] = str(self.Data_full['GROUP_FEATURE_ROW'])
        self.Data_full['GROUP_FEATURE_ROW'] = self.Data_full['GROUP_FEATURE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW_items'])
        self.Data_full['PARKING'] = 0
        self.Data_full['ELEVATOR'] = 0
        self.Data_full['CABINET'] = 0
        for i in self.Data_full['GROUP_FEATURE_ROW_items']:
            for (key, value) in i.items():
                self.Data_full[key] = value
        self.Data_full['GROUP_FEATURE_ROW_items'] = str(self.Data_full['GROUP_FEATURE_ROW_items'])
        self.Data_full['GROUP_FEATURE_ROW_items'] = self.Data_full['GROUP_FEATURE_ROW_items'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW_more_details'])
        self.Data_full['GROUP_FEATURE_ROW_more_details'] = str(self.Data_full['GROUP_FEATURE_ROW_more_details'])
        self.Data_full['GROUP_FEATURE_ROW_more_details'] = self.Data_full['GROUP_FEATURE_ROW_more_details'].replace("'", '"')
        print(self.Data_full['Images'])
        self.Data_full['Images'] = str(self.Data_full['Images'])
        self.Data_full['Images'] = self.Data_full['Images'].replace("'",'"')

        self.Data_full['desck'] = posts[0][2]
    def _check(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM posts_details_personal WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        full_data = json.loads(posts[0][3])
        z = 0
        if full_data['analytics']['cat2'] == 'residential-sell':
            if full_data['analytics']['cat3'] == 'apartment-sell':
                z = 1
            elif full_data['analytics']['cat3'] == 'house-villa-sell':
                z = 2
            elif full_data['analytics']['cat3'] == 'plot-old':
                z = 3
            return 1, z

        if full_data['analytics']['cat2'] == 'residential-rent':
            if full_data['analytics']['cat3'] == 'apartment-rent':
                z = 1
            elif full_data['analytics']['cat3'] == 'house-villa-rent':
                z = 2
            return 2, z

        if full_data['analytics']['cat2'] == 'commercial-sell':
            if full_data['analytics']['cat3'] == 'office-sell':
                z = 1
            elif full_data['analytics']['cat3'] == 'shop-sell':
                z = 2
            elif full_data['analytics']['cat3'] == 'industry-agriculture-business-sell':
                z = 3
            return 3, z
        if full_data['analytics']['cat2'] == 'commercial-rent':
            if full_data['analytics']['cat3'] == 'office-rent':
                z = 1
            elif full_data['analytics']['cat3'] == 'shop-rent':
                z = 2
            elif full_data['analytics']['cat3'] == 'industry-agriculture-business-rent':
                z = 3
            return 4, z

        if full_data['analytics']['cat2'] == 'real-estate-services':
            if full_data['analytics']['cat3'] == 'partnership':
                z = 1
            elif full_data['analytics']['cat3'] == 'presell':
                z = 2
            return 5, z

        return 0, z

    def get_data(self):
        self.db_manager = DatabaseManager('posts.db')
        print(self.Token)
        x, z = self._check()
        try:
            if x == 1:
                print(f'\t this a sell file')
                self.Data_full['types'] = int(str(x)+str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details()
                InsertDataSharpiMelk.inser_data_sell(self.Data_full)
                self.db_manager.update_token_for_sharpi_melk(((self.Token,)))
            elif x == 2:
                print(f'\t this a rent file')
                self.Data_full['types'] = int(str(x)+str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details_rent()
                InsertDataSharpiMelk.inser_data_rent(self.Data_full)
                self.db_manager.update_token_for_sharpi_melk(((self.Token,)))



            elif x == 3:
                print(f'\t this a sell tejaryi file')
                self.Data_full['types'] = int(str(x)+str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details()
                InsertDataSharpiMelk.inser_data_sell(self.Data_full)
                self.db_manager.update_token_for_sharpi_melk(((self.Token,)))

            elif x == 4:
                print(f'\t this a rent tejary file')
                self.Data_full['types'] = int(str(x)+str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details_rent()
                InsertDataSharpiMelk.inser_data_rent(self.Data_full)
                self.db_manager.update_token_for_sharpi_melk(((self.Token,)))

            elif x == 5:
                print(f'\t this a real-estate-services file')
                self.Data_full['types'] = int(str(x) + str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details()
                InsertDataSharpiMelk.inser_data_sell(self.Data_full)
                self.db_manager.update_token_for_sharpi_melk(((self.Token,)))
            else:
                print('none')
                self.db_manager.update_token_for_sharpi_melk(((self.Token,)))


        except ValueError as e:
            print('Errrrrrrrrrrrrrrrrrrrrrrrrorrrrrrrrrrrrrrrrrrrrrr')
            print(e)
            time.sleep(20)
        except Exception as e:
            print('Errrrrrrrrrrrrrrrrrrrrrrrrorrrrrrrrrrrrrrrrrrrrrr')
            print(e)
            self.db_manager.update_token_for_sharpi_melk(((self.Token,)))




class Application:
    def __init__(self, db_filename, list_mahal):
        self.db_manager = DatabaseManager(db_filename)
        self.list_mahal = list_mahal

    def run(self, CONNECTION_DB: sqlite3.connect):
        tokens = self.db_manager.get_token_for_sharpi_melk()  # this method get a token from table for getting details
        oject_data_completer = GetDataFull(tokens[0][0], CONNECTION_DB, self.list_mahal)
        data = oject_data_completer.get_data()
        print(data)


if __name__ == "__main__":
    DB_FILENAME = 'posts.db'
    objct_database = DatabaseManager(DB_FILENAME)
    list_mahal = objct_database.select_all_mahal_name()
    app = Application(DB_FILENAME, list_mahal)
    DATABASE = 'posts.db'
    CONNECTION_DB = sqlite3.connect(DATABASE)
    """
    print('Start of geting detials of service')
    app.run(CONNECTION_DB)
    print('End of geting detials of service')
    """
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





