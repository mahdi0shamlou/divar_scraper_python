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
        return posts

    def _get_from_posts_details(self):
        pass

    def _get_from_personal_number(self):
        pass

    def get_data(self):
        print(self._get_from_posts())
        return self.Data


if __name__ == '__main__':
    DATABASE = 'posts.db'
    CONNECTION_DB = sqlite3.connect(DATABASE)
    get_data_obj = GetData('gZnCrm6p', CONNECTION_DB)
    data = get_data_obj.get_data()
