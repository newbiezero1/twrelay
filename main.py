import twitter

import config

api = twitter.Api(consumer_key=config.twitter_key['consumer_key'],
                  consumer_secret=config.twitter_key['consumer_secret'],
                  access_token_key=config.twitter_key['access_token_key'],
                  access_token_secret=config.twitter_key['access_token_secret'])
