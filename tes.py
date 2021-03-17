from crawlers import config
import tweepy

consumer_key = config.CONSUMER_KEY
consumer_secret = config.CONSUMER_SECRET
access_token = config.ACCESS_TOKEN
access_token_secret = config.ACCESS_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

keyword = 'bankbri_id'
start_date = '2021-03-07'
# end_date = '2021-03-08'

tweets = tweepy.Cursor(api.search, 
                        q=keyword, 
                        lang='id', 
                        since=start_date).items(1) 
                        # until=end_date).items(2)

for tweet in tweets:
    print(tweet)
    print()