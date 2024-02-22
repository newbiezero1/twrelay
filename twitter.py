"""Twitter API wrapper"""
import requests
import json


class Twitter:
    def __init__(self, bearer_token):
        self.endpoint = 'https://api.twitter.com/2/'
        self.headers = {'Authorization': f'Bearer {bearer_token}'}

    def connect_to_endpoint(self, url):
        response = requests.request("GET", self.endpoint + url, headers=self.headers, )
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()
