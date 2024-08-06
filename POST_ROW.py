import requests
import sqlite3
import json


class PostRow:
    def __init__(self, url: str, data: str):
        self.URL = url
        self.DATA = data

    def get_post_rows(self):
        return


# Define the URL to scrape
URL = 'https://api.divar.ir/v8/postlist/w/search'
DATA = '{"city_ids":["1"],"source_view":"CATEGORY","search_data":{"form_data":{"data":{"category":{"str":{"value":"apartment-sell"}},"districts":{"repeated_string":{"value":["992"]}}}}}}'


def fetch_json_data(url, data):
    response = requests.post(url, data=data)
    print(response.text)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def main():
    json_data = fetch_json_data(URL, DATA)
    # Extract post_token from each POST_ROW
    post_tokens = [
        item['data']['action']['payload']['token']
        for item in json_data.get('list_widgets', [])
        if item.get('widget_type') == 'POST_ROW'
    ]
    print(post_tokens)
    #Save to database
    #save_to_db(DB_FILENAME, post_tokens)
    #print(f"Saved {len(post_tokens)} post tokens to the database.")

if __name__ == '__main__':
    main()