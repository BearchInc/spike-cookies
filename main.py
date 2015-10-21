import urllib
import flask
from google.appengine.api import urlfetch
from flask import Flask
from bs4 import BeautifulSoup


loginURL = 'https://github.com/login'
sessionURL = 'https://github.com/session'
unseenRepoURL = 'https://github.com/bearchinc/unseen-core'

class Github:
    def login(self, user, password):
        result = urlfetch.fetch(loginURL)
        loginSetCookiesHeader = result.headers['Set-Cookie']
        print('login cookie: ' + loginSetCookiesHeader)
        doc = BeautifulSoup(result.content, "html.parser")
        token = doc.find('input', {'name': 'authenticity_token'}).attrs['value']
        print(token)

        data = urllib.urlencode({'authenticity_token': token, 'login':user, 'password': password})
        result = urlfetch.fetch(url=sessionURL,
                payload=data,
                method=urlfetch.POST,
                follow_redirects=False,
                headers={ 'Cookie': loginSetCookiesHeader })

        return result.headers['set-cookie']


app = Flask(__name__)
app.debug = True

@app.route("/login")
def login():
    return "Hello World"

@app.route("/login/github")
def login_github():
    cookies = Github().login('joaobearch', 'Unseen2015')
    return flask.jsonify(**{
        "system": "github",
        "set-cookie": cookies
    })

if __name__ == "__main__":
    app.run()