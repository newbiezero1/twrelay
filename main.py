import sys
import json
import time

from twitter import Twitter
from db import Database
from notifyer import Notifyer
import config


def find_parent_tg_msg_id(parent_twitter_id: int, user_id: int) -> int:
    res = db.execute_query(f'select * from tweets where tweet_id = {parent_twitter_id} and user_id = {user_id}')
    if res:
        return res[0][3]
    return 0


def save_msg(user_id: int, msg_id: int, tweet_id: int, parrent_id: int) -> None:
    db.execute_query(f'''INSERT INTO tweets (tweet_id, parent_id, tg_msg_id, user_id) 
    VALUES ({tweet_id}, {parrent_id}, {msg_id}, {user_id})''')
    with open(config.last_tweet_file, 'w') as f:
        f.write(json.dumps({'tweet_id': tweet_id, 'time': int(time.time())}))


def get_last_tweet_id() -> int:
    last_tweet_result = db.execute_query('SELECT * FROM tweets ORDER BY id DESC LIMIT 1')
    tweet_id = 0
    if last_tweet_result:
        tweet_id = last_tweet_result[0][1]
    return tweet_id


db = Database(config.db_name)
db.connect()

last_tweet_id = get_last_tweet_id()

client = Twitter(config.twitter_key['bearer_token'])
tweets = client.get_user_tweets(config.bheem_twitter_id, max_results=100, last_tweet_id=last_tweet_id)
if client.error_flag:
    print(f'Error {client.error_msg}')
    sys.exit()
formatted_tweets = []
for item in tweets['data']:
    tweet = {'id': item['id'], 'text': item['text'], 'referenced_tweet': 0}

    if 'referenced_tweets' in item:
        tweet['referenced_tweet'] = item['referenced_tweets'][0]['id']

    formatted_tweets.append(tweet)
formatted_tweets.reverse()

for user in config.users.values():
    notifyer = Notifyer(user['tg_chat_id'])
    for tweet in formatted_tweets:
        parent_msg_tg_id = 0
        if tweet['referenced_tweet']:
            parent_msg_tg_id = find_parent_tg_msg_id(tweet['referenced_tweet'], user['tg_chat_id'])

        message_id = notifyer.send_message(tweet['text'], parrent_id=parent_msg_tg_id)
        save_msg(user['tg_chat_id'], message_id, tweet['id'], tweet['referenced_tweet'])

db.disconnect()
