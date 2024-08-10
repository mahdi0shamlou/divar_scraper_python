import sqlite3


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

    def get_all_tokens_not_added(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token FROM posts WHERE added = 0')
            tokens = cursor.fetchall()
        return [token[0] for token in tokens]

