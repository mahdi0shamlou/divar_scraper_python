import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import json
from datetime import datetime
import os
from POST_ROW import DataFetcher, PostExtractor, DatabaseManager, \
    Application  # Replace 'your_module' with the actual module name


class TestDataFetcher(unittest.TestCase):
    @patch('requests.post')
    def test_fetch_json_data(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"list_widgets": []}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        url = 'https://example.com'
        data = '{"key": "value"}'
        fetcher = DataFetcher(url, data)
        result = fetcher.fetch_json_data()

        self.assertEqual(result, {"list_widgets": []})
        mock_post.assert_called_once_with(url, data=data)


class TestPostExtractor(unittest.TestCase):
    def test_extract_post_data(self):
        json_data = {
            "list_widgets": [
                {
                    "widget_type": "POST_ROW",
                    "data": {
                        "title": "Test Title",
                        "action": {"payload": {"token": "123",
                                               "web_info": {"district_persian": "District", "city_persian": "City"}}},
                        "image_url": "http://example.com/image.jpg",
                        "bottom_description_text": "Bottom description",
                        "middle_description_text": "Middle description",
                        "red_text": "Red text",
                        "image_count": 3
                    }
                }
            ]
        }
        expected_posts = [
            (
                "123", "Test Title", "District", "City", "http://example.com/image.jpg",
                "Bottom description", "Middle description", "Red text", 3,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        ]

        extractor = PostExtractor()
        extracted_posts = extractor.extract_post_data(json_data)

        self.assertEqual(extracted_posts[0][:9], expected_posts[0][:9])  # Ignore the timestamp in the comparison


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_filename = 'test_posts.db'
        self.db_manager = DatabaseManager(self.db_filename)

    def tearDown(self):
        if os.path.exists(self.db_filename):
            os.remove(self.db_filename)

    def test_initialize_database(self):
        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='posts';''')
            result = cursor.fetchone()
            self.assertIsNotNone(result)

    def test_save_post_data(self):
        posts = [
            ("123", "Test Title", "District", "City", "http://example.com/image.jpg",
             "Bottom description", "Middle description", "Red text", 3,
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0)
        ]
        self.db_manager.save_post_data(posts)

        with sqlite3.connect(self.db_filename) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM posts WHERE token = ?''', ("123",))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[1], "123")  # Check token
            self.assertEqual(result[2], "Test Title")  # Check title


class TestApplication(unittest.TestCase):
    @patch.object(DataFetcher, 'fetch_json_data')
    @patch.object(DatabaseManager, 'save_post_data')
    @patch.object(PostExtractor, 'extract_post_data')
    def test_run(self, mock_extract, mock_save, mock_fetch):
        mock_fetch.return_value = {"list_widgets": []}
        mock_extract.return_value = [
            (
                "123", "Test Title", "District", "City", "http://example.com/image.jpg",
                "Bottom description", "Middle description", "Red text", 3,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        ]

        url = 'https://api.divar.ir/v8/postlist/w/search'
        data = '{"city_ids":["1"],"source_view":"CATEGORY","search_data":{"form_data":{"data":{"category":{"str":{"value":"apartment-sell"}},"districts":{"repeated_string":{"value":["992"]}}}}}}'
        db_filename = 'test_posts.db'

        app = Application(url, data, db_filename)
        app.run()

        mock_fetch.assert_called_once()
        mock_extract.assert_called_once_with({"list_widgets": []})
        mock_save.assert_called_once_with(mock_extract.return_value)


if __name__ == '__main__':
    unittest.main()
