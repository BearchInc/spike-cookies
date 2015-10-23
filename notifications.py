import json
from google.appengine.api import urlfetch

smartphone = 'mrpxT7P0Fzw:APA91bEgY9zCd5O8BcIv6DF58mgUivSCy9CPjaY75Oq6bcQfpeySVL9_mw9MA0srV48f_w6t-ODvBguPrsDnIEUQPgwg6Ra3MRYUK1RWAZEAFVnkgQEODV2RrDI-jAk5_guRZBF1F2gV'
browser = 'APA91bEGknJYkXmuJHIxnLQyFmEjxIC2Sddg6WFo8xj0QsVXXPjwde0wgXs2kRsTbCuA7BjorF-V_BCOFWtRBMkA6xF7NXNCnIj1uwY5ZnkKA15M_jbxhHUt1qqVo1Vp3_udfXRiuMvWhiOzMq2R84ZYPNs3vR3c9w'

def send(notification, to, data={}):
    data = json.dumps({'to': to, 
                        'content_available': True,
                        'data' : data,
                        'time_to_live' : 0,
                        'notification': notification})

    response = urlfetch.fetch(url='https://gcm-http.googleapis.com/gcm/send',
                method=urlfetch.POST, 
                payload=data,
                headers={'Authorization':'key=AIzaSyD4jrcwQEsQrbHdhbkn22NWPH2tAByr-Jo', 'Content-Type':'application/json'})
    return response
    