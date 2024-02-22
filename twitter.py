"""Twitter API wrapper"""
import requests
import json


class Twitter:
    def __init__(self, bearer_token):
        self.endpoint = 'https://api.twitter.com/2/'
        self.headers = {'Authorization': f'Bearer {bearer_token}'}
        self.error_flag = False
        self.error_msg = ''

    def connect_to_endpoint(self, url: str) -> dict:
        try:
            response = requests.request("GET", self.endpoint + url, headers=self.headers, )
        except Exception as e:
            self.error_flag = True
            self.error_msg = e
            return {}
        if response.status_code != 200:
            self.error_flag = True
            self.error_msg = response.json()['title'] + response.json()['detail']
            return {}
        return response.json()

    def get_user_tweets(self, user_id: int, max_results=50):
        url  = f'users/{user_id}/tweets?max_results={max_results}&expansions=attachments.media_keys,referenced_tweets.id&tweet.fields=attachments&media.fields=url'
        data = self.connect_to_endpoint(url)
        return data
