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
    ollaEnUso = True
    mensajeExitoso = "El agua está hirviendo"
    mensajeFallido = "El agua no está hirviendo"
    cont = 0    
    client = paho.mqtt.client.Client("Olla",False)
    client.qos = 2
    client.on_connect = on_connect
    client.connect('localhost')
    hora =datetime.datetime.now()
    while cont <100 and ollaEnUso :
        minTemp = 50
        maxTemp = 150
        temp = np.random.uniform(minTemp,maxTemp)
        payload = {
            "Temperatura_Olla": str(round(temp,2)),            
            "Fecha": str(hora)
        }
        if ollaEnUso:
            if temp >100:                
                payload["mensaje"] = mensajeExitoso
            else:
                payload["mensaje"] = mensajeFallido
        client.publish('Casa/Cocina/temperatura_olla',json.dumps(payload),qos=0)        
        cont += 1
        print(payload)
        time.sleep(1)
        hora = hora + datetime.timedelta(seconds=1)
if __name__ == '__main__':
    main()
    sys.exit(0)
