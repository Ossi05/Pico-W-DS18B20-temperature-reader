import TemperatureSensor
import machine
from config import updateRateInSeconds, notificationsOn, NotificationUpdateRateInSeconds
from config import SendNotificationWhenGoingOver as upValue
from config import SendNotificationWhenGoingBelow as belowValue

def Serve(connection):

    print('Serving webpage...')

    while True:
        try:
            print('Waiting for client...')

            connection.settimeout(NotificationUpdateRateInSeconds)
            try:
                client = connection.accept()[0] # Accept a client
            except:
                temperature = TemperatureSensor.ReadTemperature()
                continue
            request = client.recv(1024)
            request = str(request)
            temperature = TemperatureSensor.ReadTemperature()
            try:
                request = request.split()[1]
                print(request)
            except IndexError:
                pass

            if request.endswith("Settings"):
                params = request.split('?')[1].split('&')
                ReadForm(params)
                # Respond with the entire HTML page
                html = GetWebPage(temperature)
                client.send(html)
                
            elif request.endswith("get_temperature"):
                temperature = TemperatureSensor.ReadTemperature()
                client.send(str(temperature) + " °C")
            else:
                # Respond with the entire HTML page
                html = GetWebPage(temperature)
                client.send(html)

            client.close()
        except KeyboardInterrupt:
            machine.reset()         
        except Exception as e:
            print(e)
            machine.reset()           


def ReadForm(params):
    global updateRateInSeconds
    global notificationsOn
    global upValue
    global belowValue
    for param in params:
        if param.startswith("updateRate"):
            updateRateInSeconds = int(param.split('=')[1])
        elif param.startswith("up"):
            upValue = int(param.split('=')[1])
        elif param.startswith("below"):
            belowValue = int(param.split('=')[1])
        elif param.startswith("notification"):
            # Set notificationsOn to True if the checkbox is checked
            notificationsOn = True if param.split('=')[1] == "on" else False
    
    print("Settings updated")
    



def GetWebPage(temperature):

    global updateRateInSeconds
    global notificationsOn
    global upValue
    global belowValue
    


    css = """body {
                font-family: 'Arial', sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
                }

                .container {
                max-width: 500px;
                margin: 50px auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }

                h1 {
                text-align: center;
                color: #333333;
                }

                #temperature {
                font-size: 2em;
                text-align: center;
                margin: 0;
                }

                form {
                text-align: center;
                }

                label {
                display: block;
                margin: 10px 0;
                }

                input {
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                box-sizing: border-box;
                }

                #button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 10px 0;
                cursor: pointer;
                width: 100%;
                border-radius: 5px;
                }"""

    javascript = """
        <script>
        function updateTemperature() {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("temperature").innerHTML = this.responseText;
                }
            };
            xhttp.open("GET", "/get_temperature", true);
            xhttp.send();
        }

        setInterval(updateTemperature, """ + str(updateRateInSeconds * 1000) + """);
        </script>
    """

    html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Temperature Monitor</title>
            </head>
            <style> {css} </style>
            <body>
            <div class="container">
                <h1>Temperature</h1>
            <p id="temperature">{temperature} °C</p>
            <form name='settings' id='settings' method='get'>
                </label>
                <label for="number">Update rate (seconds):
                    <input type="number" name="updateRate" id="updateRate" value="{updateRateInSeconds}">
                </label>
                <p>Receive notification when:</p>
                <label for="number">Temperature goes up:
                    <input type="number" name="up" id="up" value="{upValue}">
                </label>
                <label for="number">Temperature goes below:
                    <input type="number" name="below" id="below" value="{belowValue}">
                </label>
                <input type="submit" name="settingsSubmit" id="submit" value="Update Settings">
            </form>
            <p>&nbsp;</p>
            </div>
            {javascript}
            </body>
            </html>

            """
    return html






