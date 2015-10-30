import json
import environment
from google.appengine.api import urlfetch

smartphone = 'mqGwBTlCOvA:APA91bHP-38jFofhFthoe7liaeuqN_tgmsrEBZhC8jfgjBfJ37AYPvUJZ-9H5H05nbA0jsyY6jlqUws7_XIHrPrsvI9VhReMHeE8S7qnPS64NzxZzAbZqmjY1ixe2uczNwFc2G7Uc_xI'
browser = 'APA91bE7iwCodCtkX6zBdRlpLXUidnQhSqDV7vZ2Ie8M_SRiTm1vnn-jZKsYbSn94oGUCIB4X3UZPTyQWFSbyflmIflUmZg_LyIJnyxPYWSCtui_XRs5DNO_aJBj1vsotew-EDD5M7P295s798-pIH_9OwohbLu3lw'

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