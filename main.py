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
import logging



app = FlaskAPI(__name__)
app.debug = True
app.config['DEFAULT_RENDERERS'] = [
    'flask.ext.api.renderers.JSONRenderer',
    'flask.ext.api.renderers.BrowsableAPIRenderer',
]

channel_id = "ygor_is_awesome"
channel_token = ""

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
def approve(app_id):

    data = flask.request.get_json(True)
    print(data)
    cookies = data['cookies']
    print(cookies)
    data = { 'cookies': cookies, 'provider_home': apps[app_id].home, 'provider_domain': apps[app_id].domain }
    notification = {'title':'Permission', 'body':'I need permission to see nudes'}

    logging.info("Senging message to channel.")
    channel.send_message(channel_token, json.dumps(data))



    logging.info("Message sent")

    return {
        "response": 200,
        "system": app_id,
        "cookies": cookies
    }

@app.route("/notification/<browser_id>")
def notification(browser_id):
    notification = {'title':'Permission', 'body':'I need permission to see nudes'}
    notifications.send(notification, browser_id, { 'data': "munjal"})
    return ""

@app.route("/socket/<channel_token>")
def socket(channel_token):
    channel.send_message(channel_token, "munjal")
    return ""

@app.route("/munjal")
def munjal():
    print("Setting channel token")
    global channel_token
    channel_token = channel.create_channel(channel_id)
    return channel_token

def ask_permission(app_id):
    response = notifications.sendParseNotification(app_id)
    return {}, response.status_code
    

if __name__ == "__main__":
    app.run()