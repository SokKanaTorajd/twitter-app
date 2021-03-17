from crawlers import config
from database.db import DB
import tweepy


def tweet_crawler(keyword, start_date, n=10):

    # twitter authentication
    consumer_key = config.CONSUMER_KEY
    consumer_secret = config.CONSUMER_SECRET
    access_token = config.ACCESS_TOKEN
    access_token_secret = config.ACCESS_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # acquire data
    tweets = tweepy.Cursor(api.search, 
                            q=keyword, lang='id', 
                            since=start_date).items(n)

    for tweet in tweets:
        data_tweet = {
            "tweet_created_at" : tweet.created_at,
            "tweet_id" : tweet.id,
            "tweet_id_str": tweet.id_str,
            "tweet_full_text": tweet.text,
            "tweet_truncated": tweet.truncated,
            "tweet_entities": tweet.entities,
            "tweet_metadata": tweet.metadata,
            "tweet_source": tweet.source,
            "tweet_rep_status_id": tweet.in_reply_to_status_id,
            "tweet_rep_status_id_str": tweet.in_reply_to_status_id_str,
            "tweet_rep_user_id": tweet.in_reply_to_user_id,
            "tweet_rep_user_id_str": tweet.in_reply_to_user_id_str,
            "tweet_rep_screen_name": tweet.in_reply_to_screen_name,
            "tweet_geo": tweet.geo,
            "tweet_coordinates": tweet.coordinates,
            "tweet_place": tweet.place,
            "tweet_contributors": tweet.contributors,
            "tweet_is_quote_status": tweet.is_quote_status,
            "tweet_retweet_count": tweet.retweet_count,
            "tweet_favorite_count": tweet.favorite_count,
            "tweet_favorited": tweet.favorited,
            "tweet_retweeted": tweet.retweeted,
            "tweet_lang": tweet.lang,
            "user_id": tweet.user.id,
            "user_id_str": tweet.user.id_str,
            "user_name": tweet.user.name,
            "user_screen_name": tweet.user.screen_name,
            "user_location": tweet.user.location,
            "user_description": tweet.user.description,
            "user_url": tweet.user.url,
            "user_entities": tweet.user.entities,
            "user_protected": tweet.user.protected,
            "user_followers_count": tweet.user.followers_count,
            "user_friends_count": tweet.user.friends_count,
            "user_listed_count": tweet.user.listed_count,
            "user_created_at": tweet.user.created_at,
            "user_favourites_count": tweet.user.favourites_count,
            "user_utc_offset": tweet.user.utc_offset,
            "user_time_zone":tweet.user.time_zone,
            "user_geo_enabled": tweet.user.geo_enabled,
            "user_verified": tweet.user.verified,
            "user_statuses_count": tweet.user.statuses_count,
            "user_lang": tweet.user.lang,
            "user_contributors_enabled": tweet.user.contributors_enabled,
            "user_is_translator": tweet.user.is_translator,
            "user_is_translation_enabled": tweet.user.is_translation_enabled,
            "user_profile_background_color": tweet.user.profile_background_color,
            "user_profile_background_image_url": tweet.user.profile_background_image_url,
            "user_profile_background_tile": tweet.user.profile_background_tile,
            "user_profile_image_url": tweet.user.profile_image_url,
            "user_profile_image_url_https": tweet.user.profile_image_url_https,
            "user_profile_banner_url": tweet.user.profile_banner_url,
            "user_profile_link_color": tweet.user.profile_link_color,
            "user_profile_sidebar_border_color": tweet.user.profile_sidebar_border_color,
            "user_profile_sidebar_fill_color": tweet.user.profile_sidebar_fill_color,
            "user_profile_text_color": tweet.user.profile_text_color,
            "user_profile_use_background_image": tweet.user.profile_use_background_image,
            "user_has_extended_profile": tweet.user.has_extended_profile,
            "user_default_profile": tweet.user.default_profile,
            "user_default_profile_image": tweet.user.default_profile_image,
            "user_following": tweet.user.following,
            "user_follow_request_sent": tweet.user.follow_request_sent,
            "user_notifications": tweet.user.notifications,
            "user_translator_type": tweet.user.translator_type
        }

        # insert tweet into database
        db = DB()
        db.insertDB(data_tweet)

