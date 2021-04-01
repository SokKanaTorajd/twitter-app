import tweepy
import requests

app.config.from_pyfile('config.cfg', silent=True)

class KecilinTwitter():

    def __init__(self):
        self.consumer_key = app.config['APP_CONSUMER_KEY']
        self.consumer_secret = app.config['APP_CONSUMER_SECRET']

    def set_oauth(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        return auth

    def get_user_info(self, access_token, access_token_secret):
        auth = self.set_oauth()
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        user_verified = api.verify_credentials()
        if user_verified:
            user_info = {
                'user_id' : user_verified.id_str,
                'screen_name' : user_verified.screen_name,
                'name' : user_verified.name,
                'description' : user_verified.description,
                'statuses_count' : user_verified.statuses_count,
                'friends_count' : user_verified.friends_count,
                'followers_count' : user_verified.followers_count,
                'favourites_count': user_verified.favourites_count,
                'profile_image' : user_verified.profile_image_url}
            return user_info
            
        else:
            error_msg = {"error": "access unauthorized"}
            return error_msg
        
        