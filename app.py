import json
from flask import Flask, flash, render_template, request, \
    url_for, redirect, jsonify
from models.twitter import KecilinTwitter
from database.db import DB
import tweepy
import config

app = Flask(__name__)
app.debug = False

# request_token_url = 'https://api.twitter.com/oauth/request_token'
# access_token_url = 'https://api.twitter.com/oauth/access_token'
# authorize_url = 'https://api.twitter.com/oauth/authorize'
# show_user_url = 'https://api.twitter.com/1.1/users/show.json'
# app.config.from_pyfile('config.cfg', silent=True)

twit = KecilinTwitter()
mongo = DB('kecilin-twitter')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/tos')
def tos():
    return render_template('tos.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='uncaught exception'), 500


@app.route('/app2/start', methods=['POST', 'GET'])
def start_app2():
    if request.method =='POST':
        app_id = request.form['app_id']
        
        if app_id == 2:
            access_token = request.form['access_token']
            access_token_secret = request.form['access_token_secret']     
            user_info = twit.get_user_info(app_id, access_token, access_token_secret)
            
            return jsonify(user_info)
        
        if app_id != 2:
            return jsonify({'error': 'use a correct application id.'})
        
    if request.method == 'GET':
        callback_url = 'https://kecilin-twitter.herokuapp.com/app2/callback'
        auth = tweepy.OAuthHandler(
                        config.APP2_CONSUMER_KEY,
                        config.APP2_CONSUMER_SECRET,  
                        callback_url)
        try:
            url = auth.get_authorization_url()
            # print(url)
            return redirect(url)
        except tweepy.TweepError:
            print('Error! Failed to get request token.')
            return jsonify({'error': 'Failed to request token.'})


@app.route('/app3/start', methods=['POST', 'GET'])
def start_app3():
    if request.method =='POST':
        app_id = request.form['app_id']
        if app_id == 3:
            access_token = request.form['access_token']
            access_token_secret = request.form['access_token_secret']
            user_info = twit.get_user_info(app_id, access_token, access_token_secret)
            
            return jsonify(user_info)
        
        if app_id != 3:
            return jsonify({'error': 'use a correct application cluster.'})
        
    if request.method == 'GET':
        callback_url = 'https://kecilin-twitter.herokuapp.com/app3/callback'
        auth = tweepy.OAuthHandler(
                        config.APP3_CONSUMER_KEY, 
                        config.APP3_CONSUMER_SECRET,  
                        callback_url)
        try:
            url = auth.get_authorization_url()
            print(url)
            return redirect(url)
        except tweepy.TweepError:
            print('Error! Failed to get request token.')


@app.route('/app2/callback', methods=['GET'])
def callback_app2():
    if request.method == 'GET':
        app_id = 2
        auth = twit.set_oauth(app_id)

        auth.request_token = {
            'oauth_token': request.args.get('oauth_token'),
            'oauth_token_secret': request.args.get('oauth_verifier')}

        try:
            auth.get_access_token(request.args.get('oauth_verifier'))

        except tweepy.TweepError as e:
            error_message = 'Invalid response, {message}'.format(message=e)
            return render_template('error.html', error_message=error_message)

        response = twit.get_user_info(app_id, 
                                auth.access_token,
                                auth.access_token_secret)
        
        if response['user_id']:
            response['app_id'] = app_id
            response['credentials'] = {'access_token': auth.access_token,
                            'access_token_secret': auth.access_token_secret}
            
            return jsonify(response)
        
        return jsonify(response)

@app.route('/app3/callback', methods=['GET'])
def callback_app3():
    if request.method == 'GET':
        app_id = 3
        auth = twit.set_oauth(app_id)

        auth.request_token = {
            'oauth_token': request.args.get('oauth_token'),
            'oauth_token_secret': request.args.get('oauth_verifier')}

        try:
            auth.get_access_token(request.args.get('oauth_verifier'))

        except tweepy.TweepError as e:
            error_message = 'Invalid response, {message}'.format(message=e)
            return render_template('error.html', error_message=error_message)

        response = twit.get_user_info(app_id,
                                    auth.access_token,
                                    auth.access_token_secret)
        
        if response['user_id']:
            response['app_id'] = app_id
            response['credentials'] = {'access_token': auth.access_token,
                            'access_token_secret': auth.access_token_secret}
            
            return jsonify(response)
        
        return jsonify(response)


@app.route('/app2/tweet', methods=['POST'])
def post_app2():
    if request.method=='POST':
        app_id = request.form['app_id']
        status = request.form['status']
        access_token = request.form['access_token']
        access_token_secret = request.form['access_token_secret']
        img = request.form['imgs']

        tweeted = twit.post_tweet(app_id, access_token, 
                                access_token_secret, 
                                img=img, text=status)

        return jsonify(tweeted)


@app.route('/app3/tweet', methods=['POST'])
def post_app3():
    if request.method=='POST':
        app_id = request.form['app_id']
        status = request.form['status']
        access_token = request.form['access_token']
        access_token_secret = request.form['access_token_secret']
        img = request.form['imgs']

        tweeted = twit.post_tweet(app_id, access_token, 
                                access_token_secret, 
                                img=img, text=status)

        return jsonify(tweeted)      

  
if __name__ == '__main__':
    app.run()
