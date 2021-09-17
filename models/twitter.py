import tweepy
import config

class KecilinTwitter():

    def __init__(self):
        # self.app1_consumer_key = config.APP1_CONSUMER_KEY
        # self.app1_consumer_secret = config.APP1_CONSUMER_SECRET
        self.app2_consumer_key = config.APP2_CONSUMER_KEY
        self.app2_consumer_secret = config.APP2_CONSUMER_SECRET
        self.app3_consumer_key = config.APP3_CONSUMER_KEY
        self.app3_consumer_secret = config.APP3_CONSUMER_SECRET

    def set_oauth(self, app_id:int):
        # if app_id == 1:
        #     auth = tweepy.OAuthHandler(self.app1_consumer_key, self.app1_consumer_secret)
        #     return auth

        if app_id == 2:
            auth = tweepy.OAuthHandler(self.app2_consumer_key, self.app2_consumer_secret)
            return auth

        if app_id == 3:
            auth = tweepy.OAuthHandler(self.app3_consumer_key, self.app3_consumer_secret)
            return auth

    def get_user_info(self, app_id, access_token, access_token_secret):
        auth = self.set_oauth(app_id)
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
        
    def post_tweet(self, app_id, access_token, access_token_secret, img:list, text:str):
        auth = self.set_oauth(app_id, access_token, access_token_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        if img:
            img_ids = []
            for photo in img:
                imgs = api.media_upload(photo)
                img_ids.append(imgs.media_id)
            return api.update_status(status=text, media_ids=img_ids)
                
        return api.update_status(status=text)