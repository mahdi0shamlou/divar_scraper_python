import sqlite3


class DatabaseManager:
    def __init__(self, db_filename):
        self.db_filename = db_filename
        self._initialize_database()

    def _initialize_database(self):
        """
        this mehtode create table we need
        :return:
        """
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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts_details_personal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token TEXT UNIQUE,
                    desc TEXT,
                    all_data TEXT,
                    added INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS posts_details_moshaver (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token TEXT UNIQUE,
                    desc TEXT,
                    all_data TEXT,
                    added INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS personal_number (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token TEXT UNIQUE,
                    all_data TEXT,
                    number TEXT,
                    added INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_compeleted (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token TEXT UNIQUE,
                    city TEXT,
                    title TEXT,
                    addres TEXT,
                    image TEXT,
                    time_inserted TEXT,
                    price TEXT,
                    desck TEXT,
                    number TEXT,
                    added INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tokens_divar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jwt_token_divar TEXT UNIQUE,
                    number TEXT UNIQUE,
                    counte TEXT,
                    lats_counter TEXT
                )
            ''')
            cursor.execute('''
                
                -- Create table if it doesn't exist
                CREATE TABLE IF NOT EXISTS moshaver_numbers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    number TEXT,
                    type TEXT,
                    creator_id INTEGER,
                    editor_id INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );       
            ''')
            cursor.execute('''
                -- Create index on the 'number' column
                CREATE INDEX IF NOT EXISTS idx_number ON moshaver_numbers (number);              
            ''')

            cursor.execute('''
                        
                          CREATE TABLE IF NOT EXISTS mahal_tehran (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              name TEXT,
                              number INTEGER,
                              city INTEGER
                            );       
                      ''')

            conn.commit()

    def save_post_data(self, posts):
        """
        this methode insert data to posts table and this is main methode for post_row service
        :param posts:
        :return:
        """
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

    def save_post_data_details_personal(self, posts):
        """
        this methode insert into table posts_details_personal
        :param posts:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO posts_details_personal (token, desc, all_data, added) 
                    VALUES (?, ?, ?, ?)
                ''', posts)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token {posts[0]} already exists in the database.")
            conn.commit()

    def update_post_data_in_posts(self, token):
        """
        this methode update a row in table posts find row from input token
        this mehtode use for update that we dont get duplicate token for get details resault
        :param token:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE posts SET added = 1 WHERE token = ?', token)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token token already exists in the database.")
            conn.commit()
    # -----------------------------
    # this section for get number service
    # -----------------------------

    def update_post_personal_details(self, token):
        """
        this methode update a row in table posts find row from input token
        this mehtode use for update that we dont get duplicate token for get number resault
        :param token:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE posts_details_personal SET added = 1 WHERE token = ?', token)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token token already exists in the database.")
            conn.commit()

    def get_one_token_from_personal_details(self):
        """
        this methode use for get a token for onther service for get details like personal_number service
        :return: Tokens that not added yet
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token FROM posts_details_personal WHERE added = 0 ORDER BY id DESC limit 1')
            tokens = cursor.fetchall()
        return [token[0] for token in tokens]

    def save_number_of_personal(self, posts):
        """
        this methode insert into table personal number
        :param posts:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO personal_number (token, all_data, number, added) 
                    VALUES (?, ?, ?, ?)
                ''', posts)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token {posts[0]} already exists in the database.")
            conn.commit()

    # -----------------------------
    # -----------------------------

    def save_post_data_details_moshaver(self, posts):
        """
        this methode insert into table posts_details_personal
        :param posts:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO posts_details_moshaver (token, desc, all_data, added) 
                    VALUES (?, ?, ?, ?)
                ''', posts)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token {posts[0]} already exists in the database.")
            conn.commit()

    def get_all_tokens(self):
        """
        this methode get all token this methode use for get len of table posts
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token FROM posts')
            tokens = cursor.fetchall()
        return [token[0] for token in tokens]

    def get_all_tokens_not_added(self):
        """
        this methode use for get a token for onther service for get details like post_details service
        :return: Tokens that not added yet
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token FROM posts WHERE added = 0 limit 1')
            tokens = cursor.fetchall()
        return [token[0] for token in tokens]

    # -----------------------------
    # this section for get Post_sender service
    # -----------------------------
    def get_number_personal_for_post_sender(self):
        """
        this methode use for get a token and phone number for onther service for send post like post_sender service
        :return: Tokens that not added yet
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token,number FROM personal_number WHERE added = 0 limit 1')
            items = cursor.fetchall()
        return [item for item in items]

    def update_number_personal_for_post_sender(self, token):
        """
        this methode update a row in table posts find row from input token
        this mehtode use for update that we dont get duplicate token for get number resault
        :param token:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE personal_number SET added = 1 WHERE token = ?', token)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token token already exists in the database.")
            conn.commit()

    # -----------------------------
    # -----------------------------

    # -----------------------------
    # this section for datacompelet
    # -----------------------------

    def save_post_data_compelete(self, posts):
        """
        this methode insert into table data_compeleter
        :param posts:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO data_compeleted (token, city, title, addres, image, time_inserted, price, desck, number, added) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                ''', posts)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token {posts[0]} already exists in the database.")
            conn.commit()

    # -----------------------------
    # -----------------------------

    # -----------------------------
    # this section for Token divar
    # -----------------------------

    def get_token_of_divar_for_personal_number(self):
        """
        this methode use for get all token for verification of divar
        :return: Tokens that not added yet
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT jwt_token_divar,counte FROM tokens_divar')
            tokens = cursor.fetchall()
        return [[token[0], token[1]]for token in tokens]

    def save_token_of_divar_for_personal_number(self, posts):
        """
        this methode insert into table tokens_divar
        :param posts:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO tokens_divar (jwt_token_divar, number, counte) 
                    VALUES (?, ?, 0)
                ''', posts)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token {posts[0]} already exists in the database.")
            conn.commit()

    def update_token_counter_of_divar_for_personal_number(self, posts):
        """
        this methode update into table tokens_divar becuase counter added
        :param posts:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE tokens_divar SET counte = ? WHERE jwt_token_divar = ?', posts)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token token already exists in the database.")
            conn.commit()

    def update_token_counter_of_divar_for_personal_number_where_blocked(self, posts):
        """
        this methode update into table tokens_divar becuase counter added
        :param posts:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE tokens_divar SET last_counter = ? WHERE jwt_token_divar = ?', posts)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token token already exists in the database.")
            conn.commit()
    # -----------------------------
    # -----------------------------


    # -----------------------------
    # this section for Moshaver numbers
    # -----------------------------
    def get_number_from_moshaver_number_table(self, number):
        """
        this methode use for get a number for personal number service
        :return: Tokens that not added yet
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM moshaver_numbers WHERE number = ?', number)
            tokens = cursor.fetchall()
        return [token[0] for token in tokens]

    # -----------------------------
    # -----------------------------

    # -----------------------------
    # this section for SharpitMelk sneder
    # -----------------------------
    def get_token_for_sharpi_melk(self):
        """
        this methode use for get a token and phone number for onther service for send post like SharpiSender service
        :return: Tokens that not added yet
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token,number FROM personal_number WHERE added = 1 order by id DESC limit 1')
            items = cursor.fetchall()
        return [item for item in items]

    def update_token_for_sharpi_melk(self, token):
        """
        this methode update a row in table posts find row from input token
        this mehtode use for update that we dont get duplicate token for get number resault
        :param token:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE personal_number SET added = 8 WHERE token = ?', token)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token token already exists in the database.")
            conn.commit()
    # -----------------------------
    # -----------------------------
    def select_all_mahal_name(self):
        """
        this methode use for get a token and phone number for onther service for send post like SharpiSender service
        :return: Tokens that not added yet
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM mahal_tehran')
            items = cursor.fetchall()
        return [item for item in items]


    def save_mahal_tehran_to_db(self, posts):
        """
        this methode insert into table mahal
        :param posts:
        :return:
        """
        print(posts)
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO mahal_tehran (name, number, city) 
                    VALUES (?, ?, ?)
                ''', posts)
            except sqlite3.IntegrityError:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token {posts[0]} already exists in the database.")
            conn.commit()

    # -----------------------------
    # this section for new way sneder
    # -----------------------------
    def get_token_for_new_post_sender(self):
        """
        this methode use for get a token and phone number for onther service for send post like SharpiSender service
        :return: Tokens that not added yet
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT token,number FROM personal_number WHERE added = 0 limit 1')
            items = cursor.fetchall()
        return [item for item in items]

    def update_token_for_new_post_sender(self, token):
        """
        this methode update a row in table posts find row from input token
        this mehtode use for update that we dont get duplicate token for get number resault
        :param token:
        :return:
        """
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('UPDATE personal_number SET added = 1 WHERE token = ?', token)
            except sqlite3.IntegrityError as e:
                # Handle the case where the token already exists (do nothing or log if necessary)
                print(f"Token did not update. We have this error {e}")
            conn.commit()