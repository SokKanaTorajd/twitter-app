from flask import Flask, flash, render_template, request, \
    url_for, redirect, session
from database.db import DB
import tweepy

app = Flask(__name__)
app.debug = False

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authorize'
show_user_url = 'https://api.twitter.com/1.1/users/show.json'

app.config.from_pyfile('config.cfg', silent=True)

db = DB()


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/start')
def start():
    callback_url = 'https://kecilin-twitter.herokuapp.com/callback'
    auth = tweepy.OAuthHandler(
                    app.config['APP_CONSUMER_KEY'], 
                    app.config['APP_CONSUMER_SECRET'], 
                    callback_url)
    try:
        url = auth.get_authorization_url()
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
            #print('Token is Authorized!')
        except tweepy.TweepError as e:
            error_message = 'Invalid response, {message}'.format(message=e)
            return render_template('error.html', error_message=error_message)
        
        api = tweepy.API(auth)
        user_verified = api.verify_credentials()
        if user_verified:
            tokens = {
                'token': auth.access_token, 
                'token_secret': auth.access_token_secret}
            screen_name = user_verified.screen_name
            user_id = user_verified.id_str
            name = user_verified.name
            friends_count = user_verified.friends_count
            statuses_count = user_verified.statuses_count
            followers_count = user_verified.followers_count
            data = {
                'user_id': user_verified.id,
                'access': tokens
            }
            db.insertAuthorizedUser(data)

            return render_template('callback-success.html', 
                                    screen_name=screen_name, 
                                    user_id=user_id, name=name,
                                    friends_count=friends_count, 
                                    statuses_count=statuses_count, 
                                    followers_count=followers_count, 
                                    access_token_url=access_token_url)


@app.route('/post-tweet/', methods=['GET', 'POST'])
def post_tweet():

    if request.method == 'POST':
        user_access = db.getUserAccess()
        auth = tweepy.OAuthHandler(
                app.config['APP_CONSUMER_KEY'],
                app.config['APP_CONSUMER_SECRET'])
        auth.set_access_token(user_access['token'], user_access['token_secret'])
        api = tweepy.API(auth)
        text = request.form['tweet']
        api.update_status(text)
        flash('Your Tweet has been posted! Check your timeline.')
        return redirect(url_for('post_tweet'))


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
