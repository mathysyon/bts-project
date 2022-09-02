import paho.mqtt.client as mqtt
import json

#import mysql.connector

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))    

    client.subscribe("zigate/attribute_changed/#")

# The callback for when a PUBLISH message is received from the server.
def on_message_humi(client, userdate, msg):
    humidite=str(msg.payload)

    humidite = humidite[2:-1]

    humidite_json = json.loads(humidite)
    value = str(humidite_json['value'])

    print("Humidité : "+value+" %")

def on_message_temp(client, userdate, msg):
    temperature=str(msg.payload)

    temperature = temperature[2:-1]

    temperature_json = json.loads(temperature)
    value = str(temperature_json['value'])

    print("Température : "+value+"°C")
    return value

def on_message_pres(client, userdate, msg):
    presence=str(msg.payload)

    presence = presence[2:-1] 

    presence_json = json.loads(presence)
    value = str(presence_json['value'])
    if value == "True":
        print("--------------MOUVEMENT DETECTE--------------")
    print("Présence : "+value)

def on_message_lum(client, userdate, msg):
    luminosite=str(msg.payload)

    luminosite = luminosite[2:-1] #Supprime le b' et le ' à la fin de la chaine permettant d'exploiter les données

    luminosite_json = json.loads(luminosite)
    value = str(luminosite_json['value']) #str permet de transformer la valeur (int) en un string, ce qui permet la concaténation dans l'affichage

    print("Luminosité : " + value + " lm")  

if __name__ == '__main__':
    client = mqtt.Client()    
    
    #A chaque changement d'attribut "attribute_changed", les fonctions sont appellées 
    client.message_callback_add('zigate/attribute_changed/d0d0/01/0405/0000', on_message_humi) 
    client.message_callback_add('zigate/attribute_changed/d0d0/01/0402/0000', on_message_temp)
    client.message_callback_add('zigate/attribute_changed/1b2f/01/0406/0000', on_message_pres)
    client.message_callback_add('zigate/attribute_changed/1b2f/01/0400/0000', on_message_lum)
    client.on_connect = on_connect
    
    client.connect("localhost", 1883, 60)
    
    #client.loop_forever()
    client.loop_start()
