import machine
import Networking
import TemperatureSensor
import Webpage

# Remember to edit config.py with your settings

def main():
    try:
        TemperatureSensor.FindTemperatureSensor()
        ip = Networking.Connect() # Connect to network
        connection = Networking.OpenSocket(ip) # Open a socket

        # Serve the webpage
        Webpage.Serve(connection)

    except KeyboardInterrupt:
        machine.reset()
    except Exception as e:
        print('Error: ' + str(e))
        machine.reset()

if __name__ == "__main__":
    main()







