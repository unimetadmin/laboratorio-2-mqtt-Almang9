import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import time
import random
import datetime
import json
import sys
import ssl
import requests
def on_connect(client, userdata, flags, rc):
	print('alexa conectada')

def main():
    cont = 0
    resp = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Caracas&appid=746872ff706ff4ebf8cd394c72541b42')
    print(resp.json()["main"]["temp"])
    # Conversión de Kelvin a Celsius
    temp =int(resp.json()["main"]["temp"]) - 273.15
    print(temp)
    client = paho.mqtt.client.Client("Alexa",False)
    client.qos = 2
    client.on_connect = on_connect
    client.connect('localhost')
    hora =datetime.datetime.now()
    while cont < 100 :
        tempDelta = np.random.normal(1,0.5)
        payload = {
            "Temperatura Caracas": str(round(temp + tempDelta,2)),
            "Fecha": str(hora)
        }
        client.publish('Casa/Sala/alexa_echo',json.dumps(payload),qos=0)
        cont += 1
        print(payload)
        time.sleep(1)
        hora = hora + datetime.timedelta(seconds=300)
if __name__ == '__main__':
    main()
    sys.exit(0)
