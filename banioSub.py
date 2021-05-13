import sys
import paho.mqtt.client
import json
import psycopg2
from psycopg2 import Error

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='Casa/Banio/#', qos=0)

def on_message(client, userdata, message):
    tanqueQuery1 = "INSERT INTO nivel_tanque (nivel_agua,mensaje, fecha) VALUES (%s,%s, %s)"
    tanqueQuery2 = "INSERT INTO nivel_tanque (nivel_agua, fecha) VALUES (%s, %s)"
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
        create_table_query = '''CREATE TABLE IF NOT EXISTS nivel_tanque ( 
        nivel_tanque_id serial NOT NULL PRIMARY KEY, 
        nivel_agua REAL NOT NULL,
        mensaje VARCHAR (100), 
        fecha timestamp NOT NULL
        ); '''
        cursor.execute(create_table_query)
        connection.commit()
        if resp.get("Agua del Tanque"):            
            if resp.get("Mensaje"):
                itemTuple = (float(resp["Agua del Tanque"]),resp["Mensaje"],resp["Fecha"])
                cursor.execute(tanqueQuery1,itemTuple)
            else:
                itemTuple = (float(resp["Agua del Tanque"]),resp["Fecha"])
                cursor.execute(tanqueQuery2,itemTuple)                
            connection.commit()
            print(itemTuple)

    except(Exception,psycopg2.Error()) as Error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def main():
    client = paho.mqtt.client.Client(client_id='Banio-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('localhost',port=1883)
    client.loop_forever()    
        
if __name__ == '__main__':
    	main()
sys.exit(0)