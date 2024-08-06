import requests
import sqlite3


class DataFetcher:
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def fetch_json_data(self):
        response = requests.post(self.url, data=self.data)
        response.raise_for_status()
        return response.json()


class PostTokenExtractor:
    @staticmethod
    def extract_post_tokens(json_data):
        return [
            item['data']['action']['payload']['token']
            for item in json_data.get('list_widgets', [])
            if item.get('widget_type') == 'POST_ROW'
        ]


class DatabaseManager:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS posts 
                              (token TEXT PRIMARY KEY)''')
            conn.commit()

    def save_post_tokens(self, post_tokens):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            for token in post_tokens:
                try:
                    cursor.execute('INSERT INTO posts (token) VALUES (?)', (token,))
                except sqlite3.IntegrityError:
                    # Handle the case where the token already exists (do nothing or log if necessary)
                    print(f"Token {token} already exists in the database.")
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
        self.extractor = PostTokenExtractor()
        self.db_manager = DatabaseManager(db_filename)

    def run(self):
        json_data = self.fetcher.fetch_json_data()
        post_tokens = self.extractor.extract_post_tokens(json_data)
        self.db_manager.save_post_tokens(post_tokens)
        print(f"Saved/Checked {len(post_tokens)} post tokens into the database.")


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/postlist/w/search'
    DATA = '{"city_ids":["1"],"source_view":"CATEGORY","search_data":{"form_data":{"data":{"category":{"str":{"value":"apartment-sell"}},"districts":{"repeated_string":{"value":["992"]}}}}}}'
    DB_FILENAME = 'posts.db'

    app = Application(URL, DATA, DB_FILENAME)
    app.run()
    
