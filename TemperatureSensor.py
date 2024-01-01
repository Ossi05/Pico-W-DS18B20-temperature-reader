import utime
from time import sleep, sleep_ms
from config import ds_pin, ds_sensor, amountOfTriesToFindSensor, updateRateInSeconds, notificationsOn, SendNotificationWhenGoingBelow, SendNotificationWhenGoingOver
import Notifications


temperatureSensor = None

def FindTemperatureSensor():
    
    global temperatureSensor
    tries = amountOfTriesToFindSensor
    print("Finding DS devices...")
    while tries > 0 and temperatureSensor == None:     

        roms = ds_sensor.scan()
        try:          
            temperatureSensor = roms[0]
        except:
            print('Error finding DS devices! Tries left: ' + str(tries))
            tries -= 1
            sleep(1)

    if temperatureSensor == None:
        print('No DS devices found!')
    else:
        print('Found DS device: ' + str(temperatureSensor))
        

def ReadTemperature(decimals = 2):
    global temperatureSensor
 
    ds_sensor.convert_temp()
    sleep_ms(750)
    currentTemperature = ds_sensor.read_temp(temperatureSensor) # Read temperature
    print('Current temperature: ' + str(currentTemperature)) # Print temperature
    currentTemperature = round(currentTemperature, decimals)
    
    if (notificationsOn):
        
        if (Notifications.canSendMessage):
            if (currentTemperature > SendNotificationWhenGoingOver):              
                Notifications.canSendMessage = False
                Notifications.SendMessage(currentTemperature, SendNotificationWhenGoingOver, False)

            elif (currentTemperature < SendNotificationWhenGoingBelow):       
                Notifications.canSendMessage = False        
                Notifications.SendMessage(currentTemperature, SendNotificationWhenGoingBelow, True)            
        else:
            if (currentTemperature < SendNotificationWhenGoingOver and currentTemperature > SendNotificationWhenGoingBelow): 
                Notifications.canSendMessage = True
    
    return currentTemperature # Return temperature
    


