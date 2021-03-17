from flask import Flask, request, redirect, url_for, \
    session, g, flash, render_template
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
import config

SECRET_KEY='ajsa3fae841asdryh1adaf4f'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY

twitter_blueprint = make_twitter_blueprint(
    api_key=config.CONSUMER_KEY,
    api_secret=config.CONSUMER_SECRET
)
app.register_blueprint(twitter_blueprint, url_prefix='/login')

@app.route('/')
def index():
    if not twitter.authorized:
        return redirect(url_for('twitter.login'))
    resp = twitter.get("account/verify_credentials.json")
    assert resp.ok
    return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/tos')
def tos():
    return render_template('tos.html')

if __name__=='__main__':
    app.run()