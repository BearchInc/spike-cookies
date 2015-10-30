import urllib
from bs4 import BeautifulSoup
import Cookie
from google.appengine.api import urlfetch

class Github:
    home = 'https://github.com'
    domain = '.github.com'
    loginURL = 'https://github.com/login'
    sessionURL = 'https://github.com/session'
    
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def login(self):
        result = urlfetch.fetch(Github.loginURL)
        loginSetCookie= result.headers['Set-Cookie']
        doc = BeautifulSoup(result.content, "html.parser")
        token = doc.find('input', {'name': 'authenticity_token'}).attrs['value']
        print(token)

        data = urllib.urlencode({'authenticity_token': token, 'login':self.user, 'password': self.password})
        result = urlfetch.fetch(url=Github.sessionURL,
                payload=data,
                method=urlfetch.POST,
                follow_redirects=False,
                headers={ 'Cookie': loginSetCookie})

        sessionSetCookie = result.headers['Set-Cookie']
        print sessionSetCookie

        return readCookies(sessionSetCookie), self.home

class Facebook:
    domain = '.facebook.com'
    home = 'https://www.facebook.com'
    loginURL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=110'
    
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def login(self):
        data = urllib.urlencode({'email': self.user, 'pass': self.password})
        result = urlfetch.fetch(url=Facebook.loginURL, 
                payload=data, 
                method=urlfetch.POST, 
                follow_redirects=False, 
                headers={ 'cookie':'_ga=BakerySSO'})

        return readCookies(result.headers['Set-Cookie']), result.headers['location']


class Twitter:
    home = 'https://twitter.com'
    domain = '.twitter.com'
    loginURL = 'https://twitter.com/login'
    sessionURL = 'https://twitter.com/sessions'

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def login(self):
            result = urlfetch.fetch(Twitter.loginURL, headers= { "User-agent":"" })
            loginSetCookie = result.headers['Set-Cookie']

            print ""
            print ""
            print("Login cookies: " + loginSetCookie)

            print ""
            print ""
            print result.headers

            doc = BeautifulSoup(result.content, "html.parser")
            token = doc.find('input', {'name': 'authenticity_token'}).attrs['value']

            print ""
            print ""
            print(token)

            data = urllib.urlencode({'session[username_or_email]': self.user, 'session[password]': self.password, 'authenticity_token': token, "redirect_after_login":"/" })

            print ""
            print ""
            print data

            result = urlfetch.fetch(url=Twitter.sessionURL, 
                    payload=data, 
                    method=urlfetch.POST, 
                    follow_redirects=False, 
                    headers={ 'Cookie': loginSetCookie, "Content-type": "application/x-www-form-urlencoded" })

            sessionSetCookie = result.headers['Set-Cookie']

            print ""
            print ""
            print("Session cookies:" + sessionSetCookie)

            print ""
            print ""
            print result.headers

            return readCookies(loginSetCookie), result.headers['location']


def readCookies(str):
    c = Cookie.SimpleCookie()
    c.load(str)
    data = {}
    for key in c:
        data[key] = c[key].value
    return data
