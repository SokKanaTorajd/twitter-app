from flask import Flask, flash, render_template, request, \
    url_for, redirect, jsonify
from models.twitter import KecilinTwitter

# from database.db import DB
# from flask_restplus import Api, Resource, fields
import tweepy

app = Flask(__name__)
app.debug = False
# app_api = Api(app, version='1.0', title='Integrated Media - Twitter API',
#     description='Kecilin Integrated Media API v1.0')

# twitter_user = api.namespace('user', description='Socmed Twitter API')
# user_model = twitter_user.model('IMTwitter', {
#     'user_id' : fields.String(required=True, description='User id'),
#     'screen_name' : fields.String(required=True, description='Twitter Username'),
#     'name' : fields.String(required=True, description='Twitter name'),
#     'description' : fields.String(required=True, description='User bio description'),
#     'statuses_count' : fields.Integer(required=True, description='User Statuses Count'),
#     'friends_count' : fields.Integer(required=True, description='User Followings Count'),
#     'followers_count' : fields.Integer(required=True, description='User Followers Count'),
#     'favourites_count': fields.Integer(required=True, description='User Likes Count'),
#     'profile_image' : fields.String(required=True, description='User profile image link')
# }) 

# users = [
#     {
#         'user_id': '1117409047261540353', 
#         'screen_name': 'radiputra49', 
#         'name': 'radiputra49', 
#         'description': 'Just for fun', 
#         'statuses_count': 14, 
#         'friends_count': 7, 
#         'followers_count': 0, 
#         'favourites_count': 3, 
#         'profile_image': 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
#     },
#     {
#         'user_id': '2880366295', 
#         'screen_name': 'devtorajd', 
#         'name': 'helios', 
#         'description': 
#         'Master of None - Jack of All Trades', 
#         'statuses_count': 5413, 
#         'friends_count': 235, 
#         'followers_count': 151, 
#         'favourites_count': 6599, 
#         'profile_image': 'http://pbs.twimg.com/profile_images/1377249145316990982/ECR_CkiK_normal.jpg'
#         }]

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'
show_user_url = 'https://api.twitter.com/1.1/users/show.json'

app.config.from_pyfile('config.cfg', silent=True)

# db = DB()
twit = KecilinTwitter()

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    if request.method =='POST':
        access_token = request.form['access_token']
        access_token_secret = request.form['access_token_secret']
        user_info = twit.get_user_info(access_token, access_token_secret)
        
        return jsonify(user_info)
        
    else:
        callback_url = 'https://kecilin-twitter.herokuapp.com/callback'
        auth = tweepy.OAuthHandler(
                        app.config['APP_CONSUMER_KEY'], 
                        app.config['APP_CONSUMER_SECRET'], 
                        callback_url)
        try:
            url = auth.get_authorization_url()
            print(url)
            return redirect(url)
        except tweepy.TweepError:
            print('Error! Failed to get request token.')



@app.route('/callback', methods=['GET'])
def callback():
    if request.method == 'GET':
        auth = tweepy.OAuthHandler(
                app.config['APP_CONSUMER_KEY'],
                app.config['APP_CONSUMER_SECRET'])

        auth.request_token = {
            'oauth_token': request.args.get('oauth_token'),
            'oauth_token_secret': request.args.get('oauth_verifier')}

        try:
            auth.get_access_token(request.args.get('oauth_verifier'))

        except tweepy.TweepError as e:
            error_message = 'Invalid response, {message}'.format(message=e)
            return render_template('error.html', error_message=error_message)

        auth.set_access_token(auth.access_token, auth.access_token_secret)
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

            return jsonify(user_info)

        return jsoniy({"error": "access unauthorized"})

# @twitter_user.route('/user-twitter')
# class UserData(Resource):
#     @twitter_user.doc('get_user_model')
#     @twitter_user.marshal_with(user_model)
#     def get(self):
#         return users

            # db.insertAuthorizedUser(data)

            # return render_template('callback-success.html', 
            #                         screen_name=screen_name, 
            #                         user_id=user_id, name=name,
            #                         friends_count=friends_count, 
            #                         statuses_count=statuses_count, 
            #                         followers_count=followers_count, 
            #                         access_token_url=access_token_url)


# @app.route('/post-tweet/', methods=['GET', 'POST'])
# def post_tweet():

#     if request.method == 'POST':
#         user_access = db.getUserAccess(2880366295)
#         auth = tweepy.OAuthHandler(
#                 app.config['APP_CONSUMER_KEY'],
#                 app.config['APP_CONSUMER_SECRET'])
#         auth.set_access_token(user_access['token'], user_access['token_secret'])
#         api = tweepy.API(auth)
#         text = request.form['tweet']
#         api.update_status(text)
#         flash('Your Tweet has been posted! Check your timeline.')
#         return redirect(url_for('post_tweet'))


@app.route('/policy')
def policy():
    return render_template('policy.html')


@app.route('/tos')
def tos():
    return render_template('tos.html')


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='uncaught exception'), 500

  
if __name__ == '__main__':
    app.run()
