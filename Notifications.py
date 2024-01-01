import urequests
import network
from config import api_key


overTitle = "Temperature is now over:"
belowTitle = "Temperature is now below:"
notificationBody = "Temperature is now:"
canSendMessage = True

def SendMessage(currentTemperature, reachedValue, isBelow):
    global api_key
    url = 'https://api.pushbullet.com/v2/pushes'
    global overTitle
    global belowTitle
    global notificationBody

    if isBelow:
        title = f"{belowTitle} {str(reachedValue)} celsius"
    else:
        title = f"{overTitle} {str(reachedValue)} celsius"  

    body = f"{notificationBody} {str(currentTemperature)} celsius"

    headers = {
        'Access-Token': api_key,
        'Content-Type': 'application/json'
    }

    data = {
        'title': title,
        'body': body,
        'type': 'note'
    }
    response = urequests.post(url, headers=headers, json=data)
    print(response.text)
    response.close()
    
