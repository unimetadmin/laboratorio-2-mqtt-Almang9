import sys
import paho.mqtt.client
import json
import psycopg2
from psycopg2 import Error

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='Casa/Cocina/#', qos=0)

def on_message(client, userdata, message):
    neveraQuery = "INSERT INTO temperatura_nevera (temperatura,hielo, fecha) VALUES (%s,%s, %s)"
    ollaQuery1 = "INSERT INTO temperatura_olla (temperatura,mensaje,fecha) VALUES (%s, %s,%s)"
    ollaQuery2 = "INSERT INTO temperatura_olla (temperatura,fecha) VALUES (%s, %s)"
    print('------------------------------')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload)
    print('qos: %d' % message.qos)
    resp =json.loads(message.payload)
    try:
        connection = psycopg2.connect(user='prbzchlc',
        password='fyGFXrTIwYzWdNKFW6Tvnsarmnikd-Kw',
        host='queenie.db.elephantsql.com',
        database='prbzchlc')
        cursor = connection.cursor()
        create_table_query = '''CREATE TABLE IF NOT EXISTS temperatura_nevera ( 
        temperatura_nevera_id serial NOT NULL PRIMARY KEY, 
        temperatura REAL NOT NULL,
        hielo INTEGER NOT NULL,
        mensaje VARCHAR (100), 
        fecha timestamp NOT NULL
        ); '''
        cursor.execute(create_table_query)
        connection.commit()
        create_table_query = '''CREATE TABLE IF NOT EXISTS temperatura_olla ( 
        temperatura_olla_id serial NOT NULL PRIMARY KEY, 
        temperatura REAL NOT NULL,
        mensaje VARCHAR(100),
        fecha timestamp NOT NULL
        ); '''
        cursor.execute(create_table_query)
        connection.commit()
        if resp.get("Temperatura_Olla"):            
            if resp.get("mensaje"):
                itemTuple = (float(resp["Temperatura_Olla"]),resp["mensaje"],resp["Fecha"])
                cursor.execute(ollaQuery1,itemTuple)
            else:
                itemTuple = (float(resp["Temperatura_Olla"]),resp["Fecha"])
                cursor.execute(ollaQuery2,itemTuple)                
            connection.commit()
            print(itemTuple)
        elif resp.get("Temperatura_nevera"):
            itemTuple = (float(resp["Temperatura_nevera"]),resp["Cantidad_de_Hielo"],resp["Fecha"])
            cursor.execute(neveraQuery,itemTuple)
            connection.commit()
            print(itemTuple)
    except(Exception,psycopg2.Error()) as Error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def main():
    client = paho.mqtt.client.Client(client_id='Cocina-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('localhost',port=1883)
    client.loop_forever()    
        
if __name__ == '__main__':
    	main()
sys.exit(0)