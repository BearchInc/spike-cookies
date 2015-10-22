import flask
import json
import providers
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
    data = json.dumps({'to':'APA91bEGknJYkXmuJHIxnLQyFmEjxIC2Sddg6WFo8xj0QsVXXPjwde0wgXs2kRsTbCuA7BjorF-V_BCOFWtRBMkA6xF7NXNCnIj1uwY5ZnkKA15M_jbxhHUt1qqVo1Vp3_udfXRiuMvWhiOzMq2R84ZYPNs3vR3c9w', 
                            'content_available': True,
                            'notification':{'title':'Permission',
                                            'body':'I need permission to see nudes',
                                            'cookies': cookies
                                            }})
    response = urlfetch.fetch(url='https://gcm-http.googleapis.com/gcm/send',
                method=urlfetch.POST, 
                payload=data,
                headers={'Authorization':'key=AIzaSyD4jrcwQEsQrbHdhbkn22NWPH2tAByr-Jo'})
    print reponse.status_code
    return reponse.status_code


@app.route("/permission", methods=['POST'])
@set_renderers(JSONRenderer)
def ask_permission():
    data = json.dumps({'to':'mrpxT7P0Fzw:APA91bEgY9zCd5O8BcIv6DF58mgUivSCy9CPjaY75Oq6bcQfpeySVL9_mw9MA0srV48f_w6t-ODvBguPrsDnIEUQPgwg6Ra3MRYUK1RWAZEAFVnkgQEODV2RrDI-jAk5_guRZBF1F2gV', 
                            'content_available': True,
                            'notification':{'title':'Permission',
                                            'approve_url':'https://bakery-dot-staging-api-getunseen.appspot.com/permission/approve',
                                            'reject_url':'https://bakery-dot-staging-api-getunseen.appspot.com/permission/reject',
                                            'body':'I need permission to see nudes',
                                            'click_action':'LOGIN_REQUEST'}})

    response = urlfetch.fetch(url='https://gcm-http.googleapis.com/gcm/send',
                method=urlfetch.POST, 
                payload=data,
                headers={'Authorization':'key=AIzaSyD4jrcwQEsQrbHdhbkn22NWPH2tAByr-Jo'})
    return {}, response.status_code
    

if __name__ == "__main__":
    app.run()