import json
import environment
from google.appengine.api import urlfetch

smartphone = 'mqGwBTlCOvA:APA91bHP-38jFofhFthoe7liaeuqN_tgmsrEBZhC8jfgjBfJ37AYPvUJZ-9H5H05nbA0jsyY6jlqUws7_XIHrPrsvI9VhReMHeE8S7qnPS64NzxZzAbZqmjY1ixe2uczNwFc2G7Uc_xI'
browser = 'APA91bGm9xSIoO4v9sjNi08UXdtcPQgk78Wtesj4etRDRm5Su7WqmlZT3oh01jq8HhD0bQLIz6ic0B525BvJHc4CHvBxaOhUDcq3q4mVQrIYdIhduapvLjacHwEpM-Rou_ovUkcBdcFTvAGPX9FeM734ENanX2fY0g'

def send(notification, to, data={}):
    data = json.dumps({'to': to, 
                        'content_available': True,
                        'data' : data,
                        'time_to_live' : 0,
                        'notification': notification})

    headers = {'Authorization':'key=AIzaSyD4jrcwQEsQrbHdhbkn22NWPH2tAByr-Jo', 'Content-Type':'application/json'}

    response = urlfetch.fetch(url='https://gcm-http.googleapis.com/gcm/send',
                method=urlfetch.POST, payload=data, headers=headers)

    return response
    
def sendParseNotification(app_id=''):

    data = json.dumps({ 
        'where': { 'deviceType': 'ios' }, 
        'data': { 'aps': { 
                'alert': { 'body': 'Allow login at ' + app_id + '?', 'title': 'Notification Title' },
                'category': 'LOGIN_REQUEST',
                'login_url': environment.current_ip() + '/permission/approve/' + app_id,
                'reject_url': environment.current_ip() + '/permission/reject/' + app_id,
                'content-available': 1 
                }
        }
    })

    headers = {
        'X-Parse-Application-Id': 'wWnWoHxacJQauLNHHRkRdK8SW9mthV1TMCZEAyNQ', 
        'X-Parse-REST-API-Key': 'Kax6B4WgzQxwIdXMb6NVGMq0irVvOW7t3XiOf24M',
        'Content-Type': 'application/json'
    }

    response = urlfetch.fetch(url='https://api.parse.com/1/push', method=urlfetch.POST, payload=data, headers=headers)

    return response