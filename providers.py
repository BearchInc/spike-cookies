import urllib
from bs4 import BeautifulSoup
import Cookie
from google.appengine.api import urlfetch

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


def readCookies(str):
    c = Cookie.SimpleCookie()
    c.load(str)
    data = {}
    for key in c:
        data[key] = c[key].value
    return data