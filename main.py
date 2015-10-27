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

@app.route("/permission/approve/<app_id>")
@set_renderers(JSONRenderer)
def approve(app_id):
    cookies, home = apps[app_id].login()
    print home
    data = { 'cookies': cookies, 'provider_home': home, 'provider_domain': apps[app_id].domain }
    notification = {'title':'Permission', 'body':'I need permission to see nudes'}
    response = notifications.send(notification, notifications.browser, data)

    return {
        "response":response.status_code,
        "system": app_id,
        "cookies": cookies
    }

def ask_permission(app_id):
    notification = {'title':'Permission',
            'body':'Allow login at ' + app_id + '?',
            'click_action':'LOGIN_REQUEST'}
    data = { 'approve_url':'https://bakery-dot-staging-api-getunseen.appspot.com/permission/approve/' + app_id,
             'reject_url':'https://bakery-dot-staging-api-getunseen.appspot.com/permission/reject/' + app_id }
    

    # response = notifications.send(notification, notifications.smartphone, data)
    response = notifications.sendParseNotification(data)

    return {}, response.status_code
    

if __name__ == "__main__":
    app.run()