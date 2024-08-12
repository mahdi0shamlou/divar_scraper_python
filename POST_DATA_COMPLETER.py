from DataBase_manager import *


class GetData:
    """
        this class get all data of one token
    """
    def __init__(self, token):
        self.Token = token
        self.Data = []

    def _get_from_posts(self):
        pass

    def _get_from_posts_details(self):
        pass

    def _get_from_personal_number(self):
        pass

    def get_data(self):
        return self.Data


if __name__ == '__main__':
    get_data_obj = GetData('token')
    data = get_data_obj.get_data()
