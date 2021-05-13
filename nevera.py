import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import time
import random
import datetime
import json
import sys
import ssl

def on_connect(client, userdata, flags, rc):
	print('alexa conectada')

def main():
    cont = 0    
    client = paho.mqtt.client.Client("Nevera",False)
    client.qos = 2
    client.on_connect = on_connect
    client.connect('localhost')
    hora =datetime.datetime.now()
    while cont <100 :
        meanTemp = 10
        stndTemp = 2
        minHielo = 0
        maxHielo = 10
        temp = np.random.normal(meanTemp,stndTemp)
        hielo = np.random.uniform(minHielo,maxHielo)
        payload = {
            "Temperatura_nevera": str(round(temp,2)),
            "Cantidad_de_Hielo": str(round(hielo)),
            "Fecha": str(hora)
        }
        client.publish('Casa/Cocina/temperatura_nevera',json.dumps(payload),qos=0)
        cont += 1
        print(payload)
        time.sleep(1)
        hora = hora + datetime.timedelta(seconds=300)
if __name__ == '__main__':
    main()
    sys.exit(0)
