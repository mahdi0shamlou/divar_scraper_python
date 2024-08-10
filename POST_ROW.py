import requests
import sqlite3
import json
from datetime import datetime
import time


class DataFetcher:
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def fetch_json_data(self):
        response = requests.post(self.url, data=self.data)
        response.raise_for_status()
        return response.json()


class PostExtractor:
    @staticmethod
    def extract_post_data(json_data):
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

                posts.append((token, title, district, city, image_url, bottom_description, middle_description, red_text,
                              image_count, timestamp, 0))

        return posts


class DatabaseManager:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token TEXT UNIQUE,
                    title TEXT,
                    district TEXT,
                    city TEXT,
                    image_url TEXT,
                    bottom_description TEXT,
                    middle_description TEXT,
                    red_text TEXT,
                    image_count INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    added INTEGER
                )
            ''')
            conn.commit()

    def save_post_data(self, posts):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            for post in posts:
                try:
                    cursor.execute('''
                        INSERT INTO posts (token, title, district, city, image_url, bottom_description, middle_description, red_text, image_count, timestamp, added) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', post)
                except sqlite3.IntegrityError:
                    # Handle the case where the token already exists (do nothing or log if necessary)
                    print(f"Token {post[0]} already exists in the database.")
            conn.commit()

    def get_all_tokens(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token FROM posts')
            tokens = cursor.fetchall()
        return [token[0] for token in tokens]


class Application:
    def __init__(self, url, data, db_filename):
        self.fetcher = DataFetcher(url, data)
        self.extractor = PostExtractor()
        self.db_manager = DatabaseManager(db_filename)

    def run(self):
        json_data = self.fetcher.fetch_json_data()
        posts = self.extractor.extract_post_data(json_data)
        self.db_manager.save_post_data(posts)
        print(f"Saved/Checked {len(posts)} posts into the database.")


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/postlist/w/search'
    DATA = '{"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"residential-sell"}}}}}}'
    DB_FILENAME = 'posts.db'
    app = Application(URL, DATA, DB_FILENAME)
    dbs = DatabaseManager(DB_FILENAME)
    while True:
        try:
            app.run()
            print(f'this is len of db : {len(dbs.get_all_tokens())}')
        except Exception as e:
            print(f'this is Eception : {e}')
        finally:
            time.sleep(3)
