import urllib
import flask
from google.appengine.api import urlfetch
from flask import Flask
from bs4 import BeautifulSoup

class Github:
    loginURL = 'https://github.com/login'
    sessionURL = 'https://github.com/session'

    def login(self, user, password):
        result = urlfetch.fetch(Github.loginURL)
        loginSetCookiesHeader = result.headers['Set-Cookie']
        print('login cookie: ' + loginSetCookiesHeader)
        doc = BeautifulSoup(result.content, "html.parser")
        token = doc.find('input', {'name': 'authenticity_token'}).attrs['value']
        print(token)

        data = urllib.urlencode({'authenticity_token': token, 'login':user, 'password': password})
        result = urlfetch.fetch(url=Github.sessionURL,
                payload=data,
                method=urlfetch.POST,
                follow_redirects=False,
                headers={ 'Cookie': loginSetCookiesHeader })

        return result.headers['set-cookie']



class Facebook:
    loginURL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=110'
    def login(self, user, password):
        data = urllib.urlencode({'email': user, 'pass': password})
        result = urlfetch.fetch(url=Facebook.loginURL, payload=data, follow_redirects=False, method=urlfetch.POST, headers={ 'cookie':'_ga=BakerySSO'})
        print(result.headers)


app = Flask(__name__)
app.debug = True

@app.route("/login")
def login():
    return "Hello World"

@app.route("/login/facebook")
def login_facebook():
    cookies = Facebook().login('100010385929288@facebook.com', 'Unseen2015')
    return flask.jsonify(**{
        "system": "facebook",
        "set-cookie": cookies
    })

@app.route("/login/github")
def login_github():
    cookies = Github().login('joaobearch', 'Unseen2015')
    return flask.jsonify(**{
        "system": "github",
        "set-cookie": cookies
    })

if __name__ == "__main__":
    app.run()