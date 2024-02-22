import sys

from twitter import Twitter
from db import Database
import config
import json

client = Twitter(config.twitter_key['bearer_token'])
tweets = client.get_user_tweets(config.bheem_twitter_id, max_results=100)
if client.error_flag:
    print(f'Error {client.error_msg}')
    sys.exit()

includes = tweets['includes']
media = {}
for include in includes['media']:
    if include['type'] == 'photo':
        media[include['media_key']] = include['url']

formatted_tweets = []
for item in tweets['data']:
    tweet = {'id': item['id'], 'text': item['text'], 'img':'','referenced_tweet':0}
    if 'attachments' in item:
        if item['attachments']['media_keys'][0] in media:
            tweet['img'] = media[item['attachments']['media_keys'][0]]

    if 'referenced_tweets' in item:
        tweet['referenced_tweet'] = item['referenced_tweets'][0]['id']

    formatted_tweets.append(tweet)

formatted_tweets.reverse()
print(formatted_tweets)
