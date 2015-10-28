import flask
import json
import providers
import notifications
from google.appengine.api import urlfetch
from flask import Flask
from flask.ext.api import FlaskAPI
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import JSONRenderer
from google.appengine.api.channel import channel
from google.appengine.ext import deferred
from random import randint



app = FlaskAPI(__name__)
app.debug = True
app.config['DEFAULT_RENDERERS'] = [
    'flask.ext.api.renderers.JSONRenderer',
    'flask.ext.api.renderers.BrowsableAPIRenderer',
]

@app.route("/hello")
def hello():
    return "Hello World"

@app.route("/login/<app_id>")
@set_renderers(JSONRenderer)
def login(app_id):
    return ask_permission(app_id)

apps = {
    'github': providers.Github('joaobearch', 'Unseen2015'),
    'facebook': providers.Facebook('lisardo.kist@getunseen.com', 'Unseen2015'),
    'twitter': providers.Twitter('testuseen', 'bearch12'),
}

@app.route("/permission/approve/<app_id>", methods=['POST'])
@set_renderers(JSONRenderer)
def approve(app_id,):

    data = flask.request.get_json(True)
    print(data)
    cookies = data['cookies']
    print(cookies)
    data = { 'cookies': cookies, 'provider_home': apps[app_id].home, 'provider_domain': apps[app_id].domain }
    notification = {'title':'Permission', 'body':'I need permission to see nudes'}
    response = notifications.send(notification, notifications.browser, data)

    return {
        "response": response.status_code,
        "system": app_id,
        "cookies": cookies
    }

@app.route("/munjal")
def munjal():
    channelId = "ygorIsAwesome"
    token = channel.create_channel(channelId)

    return token

@app.route("/message/<channel_token>")
def channel_test(channel_token):
    channel.send_message(channel_token, "Some message")

def ask_permission(app_id):
    response = notifications.sendParseNotification(app_id)
    return {}, response.status_code
    

if __name__ == "__main__":
    app.run()