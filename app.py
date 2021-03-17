from flask import Flask, request, redirect, url_for, \
    session, g, flash, render_template
from flask_oauthlib.client import OAuth
import config

SECRET_KEY='ajsa3fae841asdryh1adaf4f'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

twitter = oauth.remote_app('twitter',
        base_url='https://api.twitter.com/1/',
        request_token_url='https://api.twitter.com/aouth/request_token',
        access_token='https://api.twitter.com/aouth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
        consumer_key=config.CONSUMER_KEY,
        consumer_secret=config.CONSUMER_SECRET,
        access_token_method = 'GET')

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    return render_template('index.html')

@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash(u'You were signed out')
    return redirect(request.referrer or url_for('index'))

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']

    session['twitter_token'] = (
    resp['oauth_token'],
    resp['oauth_token_secret']
    )

    return redirect(url_for('index'))

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/tos')
def tos():
    return render_template('tos.html')

if __name__=='__main__':
    app.run()