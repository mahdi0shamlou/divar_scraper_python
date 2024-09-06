import requests
from DataBase_manager import *
from datetime import datetime
import time
import mysql.connector

#x={"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"districts":{"repeated_string":{"value":}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"apartment-sell"}}}}}}
#z = ["992","907","40","654","198","87","301","925","951","273","291","173","191","979","1020","1019","990","68","943","131","160","53","195","112","256","283","249","48","167","143","85","953","1021","45","1014","360","91","276","277","993","156","115","57","991","298","927","264","1022","217","930","920","197","208","1007","938","154","92","297","917","254","1015","206","67","280","965","922","959","82","292","966","302","235","61","956","934","203","916","109","108","178","123","201","1028","86","971","44","1013","204","94","148","145","146","265","947","231","933","196","657","251","306","63","952","99","216","1025","130","942","919","121","931","985","937","948","255","989","1017","253","188","286","958","47","209","928","116","127","940","54","118","58","285","71","929","1031","200","66","1029","290","272","233","918","962","161","81","228","964","955","84","56","1009","1001","268","162","122","157","158","950","926","205","970","914","984","946","311","75","913","999","284","1005","279","52","95","996","983","189","656","972","957","1008","147","1004","1034","637","969","125","915","106","240","977","202","152","151","155","169","164","180","259","175","190","113","271","166","910","159","236","1033","1032","179","165","138","308","257","260","1030","163","187","78","307","185","911","140","241","50","51","193","49","921","932","194","982","963","1023","1003","263","103","281","1035","968","973","172","1026","289","288","978","171","1011","1016","72","227","220","300","1027","974","210","912","120","59","994","64","199","182","988","961","941","211","293","248","998","70","105","995","639","65","93","287","245","128","43","62","945","219","299","153","997","909","168","923","170","174","944","184","96","960","46","1012","275","88","104","949","214","110","126","60","1000","117","141","139","246","976","1010","243","234","232","278","266","186","655","282","658","74","975","1018","399","954","252","936","967","935","132","262","312","42","134","939","133","269","374","55","315","270","1002","1024","924","1006","119","908","250","192"]



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
        posts = []
        for item in json_data.get('list_widgets', []):
            if item.get('widget_type') == 'POST_ROW':
                data = item.get('data', {})
                action_payload = data.get('action', {}).get('payload', {})
                web_info = action_payload.get('web_info', {})
                title = data.get('title', 'No Title')
                token = action_payload.get('token', 'No Token')
                district = web_info.get('district_persian', 'No District')
                return district
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



class InsertDataSharpiMelk:
    @staticmethod
    def inser_data_sell(posts):

        connection = mysql.connector.connect(
            host='185.19.201.97',
            user='root_sharpi_melk_gelobal',
            password='ya mahdi',
            database='SharpiMelk',
            port=3306
        )

        param = (posts[1], posts[2], posts[3])
        query = f"""INSERT INTO Mahals (name, number, city) VALUES{param};"""
        cursor = connection.cursor()
        print(cursor.execute(query))
        connection.commit()

class Application:
    def __init__(self, url, data, db_filename):
        self.fetcher = DataFetcher(url, data)
        self.extractor = PostExtractor()
        self.db_manager = DatabaseManager(db_filename)

    def run(self, data):
        json_data = self.fetcher.fetch_json_data(data)
        mahal = self.extractor.extract_post_data(json_data)
        print(mahal)
        return mahal



if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/postlist/w/search'
    mahal_text = []

    z = ["992", "907", "40", "654", "198", "87", "301", "925", "951", "273", "291", "173", "191", "979", "1020", "1019",
         "990", "68", "943", "131", "160", "53", "195", "112", "256", "283", "249", "48", "167", "143", "85", "953",
         "1021", "45", "1014", "360", "91", "276", "277", "993", "156", "115", "57", "991", "298", "927", "264", "1022",
         "217", "930", "920", "197", "208", "1007", "938", "154", "92", "297", "917", "254", "1015", "206", "67", "280",
         "965", "922", "959", "82", "292", "966", "61", "956", "934", "203", "916", "109", "108", "178", "123", "201",
         "971", "86", "1028", "1013", "44", "204", "94", "148", "145", "146", "265", "947", "231", "933", "196", "657",
         "251", "306", "63", "952", "99", "216", "1025", "130", "942", "919", "931", "121", "985", "937", "948", "255",
         "989", "1017", "253", "188", "286", "958", "47", "209", "928", "116", "127", "940", "54", "118", "58", "285",
         "71", "929", "1031", "200", "66", "1029", "290", "272", "233", "918", "962", "161", "81", "228", "964", "955",
         "84", "56", "1009", "1001", "268", "162", "122", "157", "158", "950", "926", "205", "970", "914", "984", "946",
         "311", "75", "913", "999", "284", "1005", "279", "52", "302", "95", "996", "983", "189", "656", "957", "1008",
         "972", "147", "1004", "1034", "637", "969", "125", "915", "106", "240", "977", "202", "152", "151", "155",
         "169", "164", "180", "259", "175", "190", "113", "271", "166", "910", "159", "236", "1033", "1032", "179",
         "165", "138", "308", "257", "260", "1030", "163", "187", "78", "307", "185", "911", "140", "241", "50", "51",
         "193", "49", "921", "932", "194", "982", "963", "1023", "1003", "263", "103", "281", "1035", "968", "973",
         "172", "1026", "289", "288", "978", "171", "1011", "1016", "72", "227", "974", "300", "1027", "220", "235",
         "210", "912", "120", "59", "994", "64", "182", "199", "988", "961", "941", "211", "293", "248", "998", "70",
         "105", "995", "639", "65", "287", "93", "245", "43", "128", "62", "945", "219", "299", "153", "997", "909",
         "168", "923", "170", "174", "944", "184", "96", "960", "46", "1012", "275", "88", "949", "104", "214", "110",
         "126", "60", "1000", "117", "141", "139", "246", "976", "243", "1010", "234", "232", "278", "266", "186",
         "655", "282", "658", "74", "975", "1018", "399", "954", "252", "967", "936", "935", "132", "262", "312", "42",
         "134", "939", "133", "374", "269", "55", "315", "270", "1002", "1024", "924", "1006", "119", "908", "250",
         "192", "90"]
    for i in z:

        DATA_residential_sell = '{"city_ids":["1"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"districts":{"repeated_string":{"value":["'+i+'"]}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"residential-sell"}}}}}}'
        print(DATA_residential_sell)
        DB_FILENAME = 'posts.db'
        app = Application(URL, DATA_residential_sell, DB_FILENAME)
        dbs = DatabaseManager(DB_FILENAME)
        mahal = app.run(DATA_residential_sell)
        try:
            mahal_text.append([mahal[0].replace('\u200c', ' '),i,1])
        except:
            continue
        if len(mahal) != 0:
            dbs.save_mahal_tehran_to_db([mahal[0].replace('\u200c', ' '),int(i),1])
    print(mahal_text)

    z = ["1058","1041","1078","1045","1049","1051","1042","1101","1081","1056","573","1105","1104","1091","572","1099","1083","1044","579","588","1070","598","1080","591","1043","597","1111","570","1047","576","1072","1040","1066","1096","1089","596","590","1094","1073","1052","1050","1064","1075","1084","1059","1053","594","1057","584","586","569","589","1067","1093","1095","1071","581","1055","1038","1046","1088","1069","1076","1086","1039","582","1092","1054","568","1077","566","577","1074","593","580","592","1048","587","1114","1112","1113","567","1097","571","1079","585"]
    for i in z:
        DATA_residential_sell = '{"city_ids":["2"],"source_view":"FILTER","search_data":{"form_data":{"data":{"business-type":{"str":{"value":"personal"}},"districts":{"repeated_string":{"value":["'+i+'"]}},"sort":{"str":{"value":"sort_date"}},"category":{"str":{"value":"residential-sell"}}}}}}'
        print(DATA_residential_sell)
        DB_FILENAME = 'posts.db'
        app = Application(URL, DATA_residential_sell, DB_FILENAME)
        dbs = DatabaseManager(DB_FILENAME)
        mahal = app.run(DATA_residential_sell)
        try:
            mahal_text.append([mahal[0].replace('\u200c', ' '), i, 2])
        except:
            continue
        if len(mahal) != 0:
            dbs.save_mahal_tehran_to_db([mahal[0].replace('\u200c', ' '),int(i),2])
    print(mahal_text)
    '''
    DB_FILENAME = 'posts.db'
    dbs = DatabaseManager(DB_FILENAME)
    mahals = dbs.select_all_mahal_name()
    for i in mahals:
        InsertDataSharpiMelk.inser_data_sell(i)
    print(mahals)
    '''