import requests
import json


class DataFetcher:
    def __init__(self, url, data):
        # Initialize with URL and data payload for requests
        self.url = url
        self.data = data

    def fetch_json_data(self):
        # Send POST request and fetch JSON response
        response = requests.post(self.url, data=self.data)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json()  # Return JSON data


class PostTokenExtractor:
    @staticmethod
    def extract_post_tokens(json_data):
        # Extract post tokens from the JSON response
        return [
            item['data']['action']['payload']['token']
            for item in json_data.get('list_widgets', [])
            if item.get('widget_type') == 'POST_ROW'
        ]


class Application:
    def __init__(self, url, data):
        # Initialize DataFetcher and PostTokenExtractor
        self.fetcher = DataFetcher(url, data)
        self.extractor = PostTokenExtractor()

    def run(self):
        # Fetch JSON data and extract post tokens
        json_data = self.fetcher.fetch_json_data()
        post_tokens = self.extractor.extract_post_tokens(json_data)
        print(post_tokens)  # Print the extracted post tokens


if __name__ == '__main__':
    URL = 'https://api.divar.ir/v8/postlist/w/search'
    DATA = '{"city_ids":["1"],"source_view":"CATEGORY","search_data":{"form_data":{"data":{"category":{"str":{"value":"apartment-sell"}},"districts":{"repeated_string":{"value":["992"]}}}}}}'

    app = Application(URL, DATA)
    app.run()