
import machine, onewire, ds18x20
#Network settings
ssid = ''
wifiPassword = ''

#Temperature sensor
ds_pin = machine.Pin(27)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
amountOfTriesToFindSensor = 5

#Pushbullet
api_key = ''  # Update with your Pushbullet API key
notificationsOn = True
# How many seconds to check the temperature if no client is connected
NotificationUpdateRateInSeconds = 60
SendNotificationWhenGoingOver = 80
SendNotificationWhenGoingBelow = 0

#Webpage
updateRateInSeconds = 10
