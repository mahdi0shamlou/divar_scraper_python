from DataBase_manager import *
import datetime
import time
import json
import mysql.connector
import pymysql
import traceback
import pytz

class InsertDataSharpiMelk:
    @staticmethod
    def inser_data(posts, file_category_id):
        print(posts['PARKING'])
        print(posts['ELEVATOR'])
        print(posts['CABINET'])

        if posts['PARKING'] == True:
            posts['PARKING'] = '1'

        if posts['ELEVATOR'] == True:
            posts['ELEVATOR'] = '1'

        if posts['CABINET'] == True:
            posts['CABINET'] = '1'

        print(posts['PARKING'])
        print(posts['ELEVATOR'])
        print(posts['CABINET'])
        print(len(posts))
        connection = mysql.connector.connect(
            host='45.149.79.52',
            user='admin_arkafile',
            port=3306,
            password='eZtO7SOV',
            database='admin_arkafile_duplicate'
        )
        # زمان فعلی
        now = datetime.datetime.now()
        # تنظیم منطقه زمانی به تهران
        tehran_tz = pytz.timezone('Asia/Tehran')
        now_tehran = now.astimezone(tehran_tz)
        # فرمت دهی زمان
        now = now_tehran.strftime('%Y-%m-%d %H:%M:%S')
        print('-------------------------------------------')
        print(now)
        param = (posts['title'],
                 '',
                 posts['desck'],
                 posts['floors'],
                 posts['phone'],
                 '0',
                 '0',
                 file_category_id,
                 '1',
                 posts['mahal_text'],
                 now,
                 now,
                 posts['Otagh'],
                 posts['make'],
                 posts['meter'],
                 posts['PARKING'],
                 posts['ELEVATOR'],
                 posts['CABINET'],
                 posts['post_balcony'],
                 round(posts['price'], -3),
                 round(posts['price_meter'], -3),
                 round(posts['credit'], -3),
                 round(posts['rent'], -3),
                 f'https://divar.ir/v/{posts["token"]}',
                 posts['type'],
                 posts['floor_material'],
                 posts['post_wc'],
                 posts['post_cooling'],
                 posts['post_heating'],
                 posts['post_ab_garm_kon'],
                 posts['building_direction'],
                 posts['dwelling_units_per_floor'],
                 posts['dwelling_unit_floor']


                 )
        query = f"""INSERT INTO admin_arkafile_duplicate.files (title, image, body, floors, phone, file_content_status, quality_control_status,file_category_id, status, location, created_at, updated_at, bedroom, year, dimension, parking, elevator, warehouse, balcony, price, price_per_meter, deposit, rent, url, type, floor_material, wc, cooling, heating, hot_water_supplier, building_direction, dwelling_units_per_floor, dwelling_unit_floor) VALUES{param};"""

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
        self.Data_full['title'] = posts[0][2].replace('\u200c', ' ')
        self.Data_full['mahal_text'] = posts[0][3].replace('\u200c', ' ')
        #self.Data_full['mahal_text'] = posts[0][3]
        self.Data_full['mahal'] = 0



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
        self.Data_full['type'] = '0'
        self.Data_full['price_meter'] = 0
        self.Data_full['credit'] = 0
        self.Data_full['rent'] = 0
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
        """
            find some more details
        """
        self.Data_full['dwelling_unit_floor'] = ''
        self.Data_full['floors'] = ''

        for i in self.Data_full['UNEXPANDABLE_ROW']:
            for (z, k) in i.items():
                if z == 'طبقه':
                    self.Data_full['dwelling_unit_floor'] = k[0]
                    if 'از' in k:
                        self.Data_full['floors'] = k[-1]



        """
            end of find some details
        """
        self.Data_full['UNEXPANDABLE_ROW'] = str(self.Data_full['UNEXPANDABLE_ROW'])
        self.Data_full['UNEXPANDABLE_ROW'] = self.Data_full['UNEXPANDABLE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW'])

        """
            find some more details
        """
        self.Data_full['building_direction'] = ''
        self.Data_full['dwelling_units_per_floor'] = ''
        for i in self.Data_full['GROUP_FEATURE_ROW']:
            print('sssssssssssssssssssssssssssss')
            print(i)
            for (z,k) in i.items():
                if z == 'جهت ساختمان':
                    self.Data_full['building_direction'] = k

                elif z == "تعداد واحد در طبقه":
                    self.Data_full['dwelling_units_per_floor'] = k

        """
            end of find some details
        """
        self.Data_full['GROUP_FEATURE_ROW'] = str(self.Data_full['GROUP_FEATURE_ROW'])
        self.Data_full['GROUP_FEATURE_ROW'] = self.Data_full['GROUP_FEATURE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW_items'])
        self.Data_full['PARKING'] = 'none'
        self.Data_full['ELEVATOR'] = 'none'
        self.Data_full['CABINET'] = 'none'
        for i in self.Data_full['GROUP_FEATURE_ROW_items']:
            for (key, value) in i.items():
                self.Data_full[key] = value
        self.Data_full['GROUP_FEATURE_ROW_items'] = str(self.Data_full['GROUP_FEATURE_ROW_items'])
        self.Data_full['GROUP_FEATURE_ROW_items'] = self.Data_full['GROUP_FEATURE_ROW_items'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW_more_details'])
        """
        find some more details
        """
        self.Data_full['floor_material'] = ''
        self.Data_full['post_wc'] = ''
        self.Data_full['post_cooling'] = ''
        self.Data_full['post_heating'] = ''
        self.Data_full['post_balcony'] = 'none'
        self.Data_full['post_ab_garm_kon'] = ''

        if "پارکینگ ندارد" in self.Data_full['GROUP_FEATURE_ROW_more_details']:
            self.Data_full['PARKING'] = '0'
        if "آسانسور ندارد" in self.Data_full['GROUP_FEATURE_ROW_more_details']:
            self.Data_full['ELEVATOR'] = '0'
        if "انباری ندارد" in self.Data_full['GROUP_FEATURE_ROW_more_details']:
            self.Data_full['CABINET'] = '0'
        for i in self.Data_full['GROUP_FEATURE_ROW_more_details']:
            if "جنس کف" in i:
                self.Data_full['floor_material'] = i[6:]
            elif "سرویس بهداشتی" in i:
                self.Data_full['post_wc'] = i[13:]
            elif "سرمایش" in i:
                self.Data_full['post_cooling'] = i[6:]
            elif "گرمایش" in i:
                self.Data_full['post_heating'] = i[6:]
            elif "تأمین کننده آب" in i:
                self.Data_full['post_ab_garm_kon'] = i[19:]
            elif "بالکن" in i:
                if "بالکن" == i:
                    self.Data_full['post_balcony'] = '0' # becuase we have a error in arkafile we save this reverse
                else:
                    self.Data_full['post_balcony'] = '1' # becuase we have a error in arkafile we save this reverse
        """
        end of find some details
        """
        self.Data_full['GROUP_FEATURE_ROW_more_details'] = str(self.Data_full['GROUP_FEATURE_ROW_more_details'])
        self.Data_full['GROUP_FEATURE_ROW_more_details'] = self.Data_full['GROUP_FEATURE_ROW_more_details'].replace("'", '"')
        print(self.Data_full['Images'])
        self.Data_full['Images'] = str(self.Data_full['Images'])
        self.Data_full['Images'] = self.Data_full['Images'].replace("'",'"')
        try:
            self.Data_full['price_meter'] = self.Data_full['price'] / self.Data_full['meter']
        except Exception as e:
            print('we can not find price meter so send it 0')

        self.Data_full['desck'] = posts[0][2]

    def _get_from_posts_details_rent(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM posts_details_personal WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        full_data = json.loads(posts[0][3])
        self.Data_full['type'] = '1'
        self.Data_full['price'] = 0
        self.Data_full['price_meter'] = 0
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
        """
            find some more details
        """
        self.Data_full['dwelling_unit_floor'] = ''
        self.Data_full['floors'] = ''

        for i in self.Data_full['UNEXPANDABLE_ROW']:
            for (z, k) in i.items():
                if z == 'طبقه':
                    self.Data_full['dwelling_unit_floor'] = k[0]
                    if 'از' in k:
                        self.Data_full['floors'] = k[-1]



        """
            end of find some details
        """
        self.Data_full['UNEXPANDABLE_ROW'] = str(self.Data_full['UNEXPANDABLE_ROW'])
        self.Data_full['UNEXPANDABLE_ROW'] = self.Data_full['UNEXPANDABLE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW'])
        """
            find some more details
        """
        self.Data_full['building_direction'] = ''
        self.Data_full['dwelling_units_per_floor'] = ''
        for i in self.Data_full['GROUP_FEATURE_ROW']:
            print('sssssssssssssssssssssssssssss')
            print(i)
            for (z,k) in i.items():
                if z == 'جهت ساختمان':
                    self.Data_full['building_direction'] = k
                elif z == "تعداد واحد در طبقه":
                    self.Data_full['dwelling_units_per_floor'] = k
        """
            end of find some details
        """

        self.Data_full['GROUP_FEATURE_ROW'] = str(self.Data_full['GROUP_FEATURE_ROW'])
        self.Data_full['GROUP_FEATURE_ROW'] = self.Data_full['GROUP_FEATURE_ROW'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW_items'])
        self.Data_full['PARKING'] = 'none'
        self.Data_full['ELEVATOR'] = 'none'
        self.Data_full['CABINET'] = 'none'
        for i in self.Data_full['GROUP_FEATURE_ROW_items']:
            for (key, value) in i.items():
                self.Data_full[key] = value
        self.Data_full['GROUP_FEATURE_ROW_items'] = str(self.Data_full['GROUP_FEATURE_ROW_items'])
        self.Data_full['GROUP_FEATURE_ROW_items'] = self.Data_full['GROUP_FEATURE_ROW_items'].replace("'", '"')
        print(self.Data_full['GROUP_FEATURE_ROW_more_details'])
        """
        find some more details
        """
        self.Data_full['floor_material'] = ''
        self.Data_full['post_wc'] = ''
        self.Data_full['post_cooling'] = ''
        self.Data_full['post_heating'] = ''
        self.Data_full['post_balcony'] = 'none'
        self.Data_full['post_ab_garm_kon'] = ''

        if "پارکینگ ندارد" in self.Data_full['GROUP_FEATURE_ROW_more_details']:
            self.Data_full['PARKING'] = '0'
        if "آسانسور ندارد" in self.Data_full['GROUP_FEATURE_ROW_more_details']:
            self.Data_full['ELEVATOR'] = '0'
        if "انباری ندارد" in self.Data_full['GROUP_FEATURE_ROW_more_details']:
            self.Data_full['CABINET'] = '0'
        for i in self.Data_full['GROUP_FEATURE_ROW_more_details']:
            if "جنس کف" in i:
                self.Data_full['floor_material'] = i[6:]
            elif "سرویس بهداشتی" in i:
                self.Data_full['post_wc'] = i[13:]
            elif "سرمایش" in i:
                self.Data_full['post_cooling'] = i[6:]
            elif "گرمایش" in i:
                self.Data_full['post_heating'] = i[6:]
            elif "تأمین کننده آب" in i:
                self.Data_full['post_ab_garm_kon'] = i[19:]
            elif "بالکن" in i:
                if "بالکن" == i:
                    self.Data_full['post_balcony'] = '0'# becuase we have a error in arkafile we save this reverse
                else:
                    self.Data_full['post_balcony'] = '1'# becuase we have a error in arkafile we save this reverse
        """
        end of find some details
        """
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
                file_categor_id = GetFileCategory.Get_category(x, self.Data_full['mahal_text'], z)
                print(file_categor_id)
                InsertDataSharpiMelk.inser_data(self.Data_full, file_categor_id)
                self.db_manager.update_token_for_new_post_sender(((self.Token,)))
            elif x == 2:
                print(f'\t this a rent file')
                self.Data_full['types'] = int(str(x)+str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details_rent()
                file_categor_id = GetFileCategory.Get_category(x, self.Data_full['mahal_text'], z)
                print(file_categor_id)
                InsertDataSharpiMelk.inser_data(self.Data_full, file_categor_id)
                self.db_manager.update_token_for_new_post_sender(((self.Token,)))
                print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

            elif x == 3:
                print(f'\t this a sell tejaryi file')
                self.Data_full['types'] = int(str(x)+str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details()
                file_categor_id = GetFileCategory.Get_category(x, self.Data_full['mahal_text'], z)
                print(file_categor_id)
                InsertDataSharpiMelk.inser_data(self.Data_full, file_categor_id)
                self.db_manager.update_token_for_new_post_sender(((self.Token,)))

            elif x == 4:
                print(f'\t this a rent tejary file')
                self.Data_full['types'] = int(str(x)+str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details_rent()
                file_categor_id = GetFileCategory.Get_category(x, self.Data_full['mahal_text'], z)
                print(file_categor_id)
                InsertDataSharpiMelk.inser_data(self.Data_full, file_categor_id)
                self.db_manager.update_token_for_new_post_sender(((self.Token,)))
                print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

            elif x == 5 and z == 2:
                print(f'\t this a pre sell file')
                self.Data_full['types'] = int(str(x)+str(z))
                self._get_from_posts()
                self._get_from_personal_number()
                self._get_from_posts_details()
                file_categor_id = GetFileCategory.Get_category(x, self.Data_full['mahal_text'], z)
                print(file_categor_id)
                InsertDataSharpiMelk.inser_data(self.Data_full, file_categor_id)
                self.db_manager.update_token_for_new_post_sender(((self.Token,)))
            else:
                print('none')
                self.db_manager.update_token_for_new_post_sender(((self.Token,)))


        except ValueError as e:
            print('Errrrrrrrrrrrrrrrrrrrrrrrrorrrrrrrrrrrrrrrrrrrrrr')
            print(e)
            print(traceback.format_exc())
            time.sleep(20)

        except Exception as e:
            print('Errrrrrrrrrrrrrrrrrrrrrrrrorrrrrrrrrrrrrrrrrrrrrr')
            print(e)
            print(traceback.format_exc())
            self.db_manager.update_token_for_new_post_sender(((self.Token,)))

class GetFileCategory:
    @staticmethod
    def Get_category(type_post, mahal_text, type_post_details):
        mysql_connection = pymysql.connect(
            host='45.149.79.52',
            user='admin_arkafile',
            port=3306,
            password='eZtO7SOV',
            database='admin_arkafile_duplicate'
        )
        with mysql_connection.cursor() as mysql_cursor:
            mysql_cursor.execute(f"SELECT * FROM crawler_locations WHERE label = '{mahal_text}'")
            rows = mysql_cursor.fetchall()
            area_id = rows[0][5]
            print(area_id)
            mysql_cursor.execute(f"SELECT * FROM area_file_category JOIN file_categories ON area_file_category.file_category_id = file_categories.id WHERE file_categories.status = '1' AND area_file_category.area_id = {area_id}")
            rows = mysql_cursor.fetchall()
            if type_post == 1:
                for i in rows:
                    if 'فروش' in i[5] and 'مسکونی' in i[5]:
                        category_id = i[1]
                if type_post_details == 3:
                    for i in rows:
                        if 'کلنگی' in i[5]:
                            category_id = i[1]
            elif type_post == 2:
                for i in rows:
                    if 'اجاره' in i[5] and 'مسکونی' in i[5]:
                        category_id = i[1]
            elif type_post == 3:
                for i in rows:
                    if 'فروش' in i[5] and 'اداری' in i[5]:
                        category_id = i[1]
            elif type_post == 4:
                for i in rows:
                    if 'اجاره' in i[5] and 'اداری' in i[5]:
                        category_id = i[1]
            elif type_post == 5:
                for i in rows:
                    if 'پیش' in i[5] and 'فروش' in i[5]:
                        category_id = i[1]

            return category_id

class Application:
    def __init__(self, db_filename):
        self.db_manager = DatabaseManager(db_filename)

    def run(self, CONNECTION_DB: sqlite3.connect):
        tokens = self.db_manager.get_token_for_new_post_sender() # this method get a token from table for getting details
        oject_data_completer = GetDataFull(tokens[0][0], CONNECTION_DB)
        data = oject_data_completer.get_data()
        print(data)


if __name__ == "__main__":
    DB_FILENAME = 'posts.db'
    CONNECTION_DB = sqlite3.connect(DB_FILENAME)
    app = Application(DB_FILENAME)
    while True:
        try:
            print('Start of sending post in service')
            app.run(CONNECTION_DB)
            #file_categor_id = Get_File_category.Get_category(4, 'پاسداران')
            #print(file_categor_id)
            print('End of sending post in of service')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            time.sleep(1)
            pass
