import json
from google.appengine.api import urlfetch

def send(body):
    data = json.dumps({'to':'mrpxT7P0Fzw:APA91bEgY9zCd5O8BcIv6DF58mgUivSCy9CPjaY75Oq6bcQfpeySVL9_mw9MA0srV48f_w6t-ODvBguPrsDnIEUQPgwg6Ra3MRYUK1RWAZEAFVnkgQEODV2RrDI-jAk5_guRZBF1F2gV', 
                            'content_available': True,
                            'notification': body})

    response = urlfetch.fetch(url='https://gcm-http.googleapis.com/gcm/send',
                method=urlfetch.POST, 
                payload=data,
                headers={'Authorization':'key=AIzaSyD4jrcwQEsQrbHdhbkn22NWPH2tAByr-Jo'})
    return response
    