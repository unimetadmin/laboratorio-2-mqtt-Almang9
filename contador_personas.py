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
    mensajeAlerta = "¡No deben haber más de 5 personas en la Sala! por favor retirense"
    cont = 0    
    client = paho.mqtt.client.Client("contadorPersonas",False)
    client.qos = 0
    client.on_connect = on_connect
    client.connect(host='localhost', port=1883)
    hora =datetime.datetime.now()
    while cont <100 :
        minPer = 0
        maxPer = 10       
        personas = np.random.uniform(minPer,maxPer)
        payload = {
            "Cantidad Personas": str(round(personas)),
            "Fecha":str(hora)
        }
        if personas > 5:
            payload["mensaje"] = mensajeAlerta       
        client.publish(topic='Casa/Sala/contador_personas',payload= json.dumps(payload),qos=0)
        cont += 1
        print(payload)
        time.sleep(1)
        hora = hora + datetime.timedelta(seconds=60)
if __name__ == '__main__':
    main()
    sys.exit(0)
