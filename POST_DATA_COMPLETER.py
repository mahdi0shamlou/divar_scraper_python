import sqlite3


class GetData:
    """
        this class get all data of one token
    """
    def __init__(self, token: str, data_base_connection: sqlite3.connect):
        self.Token = token
        self.DB_Conn = data_base_connection
        self.Data = []

    def _get_from_posts(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM posts WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        self.Data.append(posts[0][1]) # Token
        self.Data.append(posts[0][2]) # City
        self.Data.append(posts[0][3]) # titile
        self.Data.append(posts[0][4]) # addres
        self.Data.append(posts[0][5]) # image
        self.Data.append(posts[0][6]) # time inserted
        self.Data.append(posts[0][7]) # price
        return posts

    def _get_from_posts_details(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM posts_details_personal WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        self.Data.append(posts[0][2])  # desck

    def _get_from_personal_number(self):
        cursor = self.DB_Conn.cursor()
        cursor.execute('SELECT * FROM personal_number WHERE token = ?', (self.Token,))
        posts = cursor.fetchall()
        self.Data.append(posts[0][3])  # phone number

    def get_data(self):
        self._get_from_posts()
        self._get_from_posts_details()
        self._get_from_personal_number()
        print(self.Data)
        return self.Data

class GetToken:
    def __init__(self, data_base_connection: sqlite3.connect):
        self.DB_Conn = data_base_connection
        self.Token = []
if __name__ == '__main__':
    DATABASE = 'posts.db'
    CONNECTION_DB = sqlite3.connect(DATABASE)
    get_data_obj = GetData('gZnCrm6p', CONNECTION_DB)
    data = get_data_obj.get_data()
