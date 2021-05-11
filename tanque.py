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
    aguaTanque = 100
    capMaxima = 0
    aguaObtenida = 0
    alertaNaranja = "Peligro, nivel de agua a menos del 50%"
    alertaRoja = "Peligro, Tanque Vacío"
    meanAgua = aguaTanque*0.1
    stndAgua = aguaTanque*0.05
    tiempoLlenado = 0
    cont = 0    
    client = paho.mqtt.client.Client("TanqueAgua",False)
    client.qos = 2
    client.on_connect = on_connect
    client.connect(host='localhost',port=1883)
    hora =datetime.datetime.now()
    while cont <100:
        capMaxima = 100 - aguaTanque
        if tiempoLlenado >= 3:
            aguaObtenida = np.random.normal(capMaxima*0.2,capMaxima*0.05)
            aguaTanque += aguaObtenida        
        aguaPerdida = np.random.normal(meanAgua,stndAgua)
        if aguaTanque>aguaPerdida:
            aguaTanque = aguaTanque - aguaPerdida
        else:
            aguaTanque = 0

        payload = {
            "Agua del Tanque": str(round(aguaTanque,2)),            
            "Fecha": str(hora)
        }
        if aguaTanque < 50:
            payload["Mensaje"] = alertaNaranja
            if aguaTanque == 0:
                payload["Mensaje"] = alertaRoja
        client.publish('Casa/Banio/nivel_tanque',json.dumps(payload),qos=0)        
        cont += 1
        print(payload)
        time.sleep(1)
        tiempoLlenado += 1        
        hora = hora + datetime.timedelta(seconds=600)
if __name__ == '__main__':
    main()
    sys.exit(0)
