import urllib
import flask
import json
from google.appengine.api import urlfetch
from flask import Flask
from flask.ext.api import FlaskAPI
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import JSONRenderer
from bs4 import BeautifulSoup
import Cookie

def readCookies(str):
    c = Cookie.SimpleCookie()
    c.load(str)
    data = {}
    for key in c:
        data[key] = c[key].value
    return data


class Github:
    loginURL = 'https://github.com/login'
    sessionURL = 'https://github.com/session'

    def login(self, user, password):
        result = urlfetch.fetch(Github.loginURL)
        loginSetCookiesHeader = result.headers['Set-Cookie']
        doc = BeautifulSoup(result.content, "html.parser")
        token = doc.find('input', {'name': 'authenticity_token'}).attrs['value']
        print(token)

        data = urllib.urlencode({'authenticity_token': token, 'login':user, 'password': password})
        result = urlfetch.fetch(url=Github.sessionURL,
                payload=data,
                method=urlfetch.POST,
                follow_redirects=False,
                headers={ 'Cookie': loginSetCookiesHeader })

        return readCookies(result.headers['Set-Cookie'])


class Facebook:
    loginURL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=110'
    def login(self, user, password):
        data = urllib.urlencode({'email': user, 'pass': password})
        result = urlfetch.fetch(url=Facebook.loginURL, 
                payload=data, 
                method=urlfetch.POST, 
                follow_redirects=False, 
                headers={ 'cookie':'_ga=BakerySSO'})
        return readCookies(result.headers['Set-Cookie'])


class Twitter:
    loginURL = 'https://twitter.com'
    sessionURL = 'https://twitter.com/sessions'

    def login(self, user, password):
            result = urlfetch.fetch(Twitter.loginURL)
            loginSetCookiesHeader = result.headers['Set-Cookie']
            doc = BeautifulSoup(result.content, "html.parser")
            token = doc.find('input', {'name': 'authenticity_token'}).attrs['value']

            data = urllib.urlencode({'authenticity_token': token, 'session[username_or_email]':user, 'session[password]': password})
            result = urlfetch.fetch(url=Twitter.sessionURL, 
                    payload=data, 
                    method=urlfetch.POST, 
                    follow_redirects=False, 
                    headers={ 'Cookie': loginSetCookiesHeader})

            return readCookies(result.headers['Set-Cookie'])

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
    cookies = Facebook().login('100010385929288@facebook.com', 'Unseen2015')
    return {
        "system": "facebook",
        "cookies": cookies
    }

@app.route("/login/github")
@set_renderers(JSONRenderer)
def login_github():
    cookies = Github().login('joaobearch', 'Unseen2015')
    return {
        "system": "github",
        "cookies": cookies
    }

@app.route("/login/twitter")
@set_renderers(JSONRenderer)
def login_twitter():
    cookies = Twitter().login('testunseen', 'bearch12')
    return {
        "system": "twitter",
        "cookies": cookies
    }

@app.route("/permission", methods=['POST'])
@set_renderers(JSONRenderer)
def ask_permission():
    data = json.dumps({'to':'mrpxT7P0Fzw:APA91bEgY9zCd5O8BcIv6DF58mgUivSCy9CPjaY75Oq6bcQfpeySVL9_mw9MA0srV48f_w6t-ODvBguPrsDnIEUQPgwg6Ra3MRYUK1RWAZEAFVnkgQEODV2RrDI-jAk5_guRZBF1F2gV', 
                            'content_available': True,
                            'notification':{'title':'Permission',
                                            'body':'I need permission to see nudes',
                                            'click_action':'LOGIN_REQUEST'}})

    response = urlfetch.fetch(url='https://gcm-http.googleapis.com/gcm/send',
                method=urlfetch.POST, 
                payload=data,
                headers={'Authorization':'key=AIzaSyD4jrcwQEsQrbHdhbkn22NWPH2tAByr-Jo'})

    return {}, response.status_code
    

if __name__ == "__main__":
    app.run()