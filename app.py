import flask
import requests
from flask import Flask
from bs4 import BeautifulSoup

loginURL = 'https://github.com/login'
sessionURL = 'https://github.com/session'
unseenRepoURL = 'https://github.com/bearchinc/unseen-core'

class Github:
    def login(self, user, password):
        r = requests.get(loginURL)
        loginSetCookiesHeader = r.headers['Set-Cookie']
        doc = BeautifulSoup(r.text)
        token = doc.find('input', {'name': 'authenticity_token'}).attrs['value']
        r = requests.post(sessionURL,
                          headers={ 'Cookie': loginSetCookiesHeader },
                          data={'utf8': '%E2%9C%93', 'authenticity_token': token, 'login':user, 'password': password})
        return r.headers['Set-Cookie']

app = Flask(__name__)
app.debug = True

@app.route("/login")
def login():
    return "Hello World"

@app.route("/login/github")
def login_github():
    cookies = Github().login('user', 'password')
    return flask.jsonify(**{
        "system": "github",
        "set-cookie": cookies
    })

if __name__ == "__main__":
    app.run()