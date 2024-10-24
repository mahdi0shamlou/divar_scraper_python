import requests
from DataBase_manager import *
from datetime import datetime
import time


class DataFetcher:
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def fetch_json_data(self, data):
        response = requests.post(self.url, data=data)
        response.raise_for_status()
        return response.json()


class PostExtractor:
    @staticmethod
    def extract_post_data(json_data):
        last_post_time_out = json_data['pagination']['data']['last_post_date']
        posts = []
        for item in json_data.get('list_widgets', []):
            if item.get('widget_type') == 'POST_ROW':
                data = item.get('data', {})
                action_payload = data.get('action', {}).get('payload', {})
                web_info = action_payload.get('web_info', {})
                title = data.get('title', 'No Title')
                token = action_payload.get('token', 'No Token')
                district = web_info.get('district_persian', 'No District')
                city = web_info.get('city_persian', 'No City')
                image_url = data.get('image_url', 'No Image URL')
                bottom_description = data.get('bottom_description_text', 'No Bottom Description')
                middle_description = data.get('middle_description_text', 'No Middle Description')
                red_text = data.get('red_text', 'No Red Text')
                image_count = data.get('image_count', 0)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if "نردبان" in red_text:
                    # dont add post if has red text
                    print(f'find nardeboon into posts --> : {token}')
                else:
                    posts.append((token, title, district, city, image_url, bottom_description, middle_description,
                                  red_text, image_count, timestamp, 0))

        return posts, last_post_time_out


class Application:
    def __init__(self, url, data, db_filename):
        self.fetcher = DataFetcher(url, data)
        self.extractor = PostExtractor()
        self.db_manager = DatabaseManager(db_filename)

    def run(self, data: str):
        json_data = self.fetcher.fetch_json_data(data)
        posts, last_post_time_out = self.extractor.extract_post_data(json_data)
        self.db_manager.save_post_data(posts)
        print(f"Saved/Checked {len(posts)} posts into the database.")

        new_data = data[:35] + ',"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":"'+last_post_time_out+'","page":10,"layer_page":10}'+data[35:]
        json_data = self.fetcher.fetch_json_data(new_data)
        posts, last_post_time_out = self.extractor.extract_post_data(json_data)
        self.db_manager.save_post_data(posts)
        print(f"Saved/Checked {len(posts)} posts into the database.")

        new_data = data[:35] + ',"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":"'+last_post_time_out+'","page":10,"layer_page":10}'+data[35:]
        json_data = self.fetcher.fetch_json_data(new_data)
        posts, last_post_time_out = self.extractor.extract_post_data(json_data)
        self.db_manager.save_post_data(posts)
        print(f"Saved/Checked {len(posts)} posts into the database.")

        new_data = data[:35] + ',"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":"'+last_post_time_out+'","page":10,"layer_page":10}'+data[35:]
        json_data = self.fetcher.fetch_json_data(new_data)
        posts, last_post_time_out = self.extractor.extract_post_data(json_data)
        self.db_manager.save_post_data(posts)
        print(f"Saved/Checked {len(posts)} posts into the database.")

        new_data = data[:35] + ',"pagination_data":{"@type":"type.googleapis.com/post_list.PaginationData","last_post_date":"'+last_post_time_out+'","page":10,"layer_page":10}'+data[35:]
        json_data = self.fetcher.fetch_json_data(new_data)
        posts, last_post_time_out = self.extractor.extract_post_data(json_data)
        self.db_manager.save_post_data(posts)
        print(f"Saved/Checked {len(posts)} posts into the database.")
        print('--------------------------------------------------------')
        return last_post_time_out


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/postlist/w/search'
    DATA_residential_sell = '{"city_ids":["1","1764","1751","2"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"residential-sell"}}}}}}'
    DATA_residential_rent = '{"city_ids":["1","1764","1751","2"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"residential-rent"}}}}}}'
    DATA_commercial_sell = '{"city_ids":["1","1764","1751","2"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"commercial-sell"}}}}}}'
    DATA_commercial_rent = '{"city_ids":["1","1764","1751","2"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"commercial-rent"}}}}}}'
    DATA_temporary_rent = '{"city_ids":["1","1764","1751","2"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"temporary-rent"}}}}}}'
    DATA_real_estate_services = '{"city_ids":["1","1764","1751","2"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"real-estate-services"}}}}}}'
    '''
    DATA_residential_sell = '{"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"residential-sell"}}}}}}'
    DATA_residential_rent = '{"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"residential-rent"}}}}}}'
    DATA_commercial_sell = '{"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"commercial-sell"}}}}}}'
    DATA_commercial_rent = '{"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"commercial-rent"}}}}}}'
    DATA_temporary_rent = '{"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"temporary-rent"}}}}}}'
    DATA_real_estate_services = '{"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"real-estate-services"}}}}}}'
    '''
    '''
    List_Post_Row_Data = []
    List_Post_Row_Data.append(DATA_residential_sell) # add tehran data to Post Row Data
    List_Post_Row_Data.append(DATA_residential_rent)
    List_Post_Row_Data.append(DATA_commercial_sell)
    List_Post_Row_Data.append(DATA_commercial_rent)
    '''
    # FOR citys ids ['1', '2', '1764'] tehran and karaj and andishe
    # DATA we can change category for sell in these type -> all of them (residential-sell) , apartment-sell , house-villa-sell , plot-old : فروش مسکونی
    # DATA we can change categort for rent in these type -> all of them (residential-rent) , apartment-rent , house-villa-rent : اجاره مسکونی
    # DATA we can change categort for rent in these type -> all of them(commercial-sell) , office-sell , shop-sell , industry-agriculture-business-sell : فروش اداری
    # DATA we can change categort for rent in these type -> all of them(commercial-rent) , office-rent , shop-rent , industry-agriculture-business-rent : اجاره اداری
    # DATA we can change category for sell in these type -> all of them(temporary-rent) , suite-apartment , villa , workspace : اجاره کوتاه مدت
    # DATA we can change category for sell in these type -> all of them(real-estate-services) , partnership , presell : پروژه ساخت و ساز
    DB_FILENAME = 'posts.db'
    app = Application(URL, DATA_residential_sell, DB_FILENAME)
    dbs = DatabaseManager(DB_FILENAME)
    while True:
        try:
            app.run(DATA_residential_sell)
            app.run(DATA_residential_rent)
            app.run(DATA_commercial_sell)
            app.run(DATA_commercial_rent)
            #app.run(DATA_temporary_rent)
            app.run(DATA_real_estate_services)
            print(f'this is len of db : {len(dbs.get_all_tokens())}')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            time.sleep(1)
