import sys
import paho.mqtt.client
import json
import psycopg2
from psycopg2 import Error

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='Casa/Sala/#', qos=0)

def on_message(client, userdata, message):
    alexaQuery = "INSERT INTO alexa_echo (temperatura, fecha) VALUES (%s, %s)"
    personasQuery1 = "INSERT INTO contador_personas (cantidad_personas,mensaje,fecha) VALUES (%s, %s,%s)"
    personasQuery2 = "INSERT INTO contador_personas (cantidad_personas,fecha) VALUES (%s, %s)"
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
        create_table_query = '''CREATE TABLE IF NOT EXISTS contador_personas ( 
        contador_personas_id serial NOT NULL PRIMARY KEY, 
        cantidad_personas INTEGER NOT NULL,
        mensaje VARCHAR (100), 
        fecha timestamp NOT NULL
        ); '''
        cursor.execute(create_table_query)
        connection.commit()
        create_table_query = '''CREATE TABLE IF NOT EXISTS alexa_echo ( 
        alexa_echo_id serial NOT NULL PRIMARY KEY, 
        temperatura REAL NOT NULL,
        fecha timestamp NOT NULL
        ); '''
        cursor.execute(create_table_query)
        connection.commit()
        if resp.get("Cantidad Personas"):            
            if resp.get("mensaje"):
                itemTuple = (int(resp["Cantidad Personas"]),resp["mensaje"],resp["Fecha"])
                cursor.execute(personasQuery1,itemTuple)
            else:
                itemTuple = (int(resp["Cantidad Personas"]),resp["Fecha"])
                cursor.execute(personasQuery2,itemTuple)                
            connection.commit()
            print(itemTuple)
        elif resp.get("Temperatura Caracas"):
            itemTuple = (float(resp["Temperatura Caracas"]),resp["Fecha"])
            print(itemTuple)
            cursor.execute(alexaQuery,itemTuple)
            connection.commit()

    except(Exception,psycopg2.Error()) as Error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def main():
    client = paho.mqtt.client.Client(client_id='Sala-subs', clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('localhost',port=1883)
    client.loop_forever()    
        
if __name__ == '__main__':
    	main()
sys.exit(0)