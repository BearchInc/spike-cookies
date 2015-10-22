import flask
import json
import providers
import notifications
from google.appengine.api import urlfetch
from flask import Flask
from flask.ext.api import FlaskAPI
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import JSONRenderer


app = FlaskAPI(__name__)
app.debug = True
app.config['DEFAULT_RENDERERS'] = [
    'flask.ext.api.renderers.JSONRenderer',
    'flask.ext.api.renderers.BrowsableAPIRenderer',
]

@app.route("/login")
def login():
    return "Hello World"

@app.route("/login/facebook")
@set_renderers(JSONRenderer)
def login_facebook():
    cookies = providers.Facebook().login('100010385929288@facebook.com', 'Unseen2015')
    return {
        "system": "facebook",
        "cookies": cookies
    }

@app.route("/login/github")
@set_renderers(JSONRenderer)
def login_github():
    cookies = providers.Github().login('joaobearch', 'Unseen2015')
    return {
        "system": "github",
        "cookies": cookies
    }

@app.route("/login/twitter")
@set_renderers(JSONRenderer)
def login_twitter():
    cookies = providers.Twitter().login('testunseen', 'bearch12')
    return {
        "system": "twitter",
        "cookies": cookies
    }

@app.route("/permission/github/approve")
def approve():
    cookies = providers.Twitter().login('testunseen', 'bearch12')
    notification = {'title':'Permission', 'body':'I need permission to see nudes','cookies': cookies }
    reponse = notifications.send(notification)
    return {}, reponse.status_code


@app.route("/permission", methods=['POST'])
@set_renderers(JSONRenderer)
def ask_permission():
    notification = {'title':'Permission',
            'body':'TIBIA NOW HAS SOUNDS',
            'click_action':'LOGIN_REQUEST'}
    data = { 'approve_url':'https://bakery-dot-staging-api-getunseen.appspot.com/permission/approve',
              'reject_url':'https://bakery-dot-staging-api-getunseen.appspot.com/permission/reject' }

    response = notifications.send(notification, data)
    return {}, response.status_code
    

if __name__ == "__main__":
    app.run()