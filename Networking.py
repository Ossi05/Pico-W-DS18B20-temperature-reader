import network, socket
from time import sleep
from config import ssid, wifiPassword

def Connect(): #Connect to WLAN
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, wifiPassword)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)

    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def OpenSocket(ip): # Open a socket
    
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection



