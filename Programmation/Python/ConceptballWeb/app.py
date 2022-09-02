from re import A
import paho.mqtt.client as mqtt
import json
from flask import Flask, render_template
#import mysql.connector


app = Flask(__name__)

valueTemp=0
valueHumi=0
valuePres=""
valueLumi=0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))    

    client.subscribe("zigate/attribute_changed/#")

# The callback for when a PUBLISH message is received from the server.
def on_message_humi(client, userdate, msg):
    chaineHumidite=str(msg.payload)

    chaineHumidite = chaineHumidite[2:-1]

    humidite_json = json.loads(chaineHumidite)
    value = str(humidite_json['value'])
    #print("Humidité : "+value+" %") #Permet d'écrire dans la console le pourcentage d'humidité

    global valueHumi
    valueHumi = value

def on_message_temp(client, userdate, msg):
    chaineTemperature=str(msg.payload)

    chaineTemperature = chaineTemperature[2:-1]

    temperature_json = json.loads(chaineTemperature)
    value = str(temperature_json['value'])
    #print("Température : "+value+"°C") #Permet d'écrire dans la console la température actuelle

    global valueTemp
    valueTemp = value

def on_message_pres(client, userdate, msg):
    chainePresence=str(msg.payload)

    chainePresence = chainePresence[2:-1] 

    presence_json = json.loads(chainePresence)
    value = str(presence_json['value'])
    #print("Présence : "+value) #Permet d'écrire dans la console si il y a une présence ou non

    global valuePres
    valuePres = value

def on_message_lum(client, userdate, msg):
    chaineLuminosite=str(msg.payload)

    chaineLuminosite = chaineLuminosite[2:-1] #Supprime le b' et le ' à la fin de la chaine permettant d'exploiter les données

    luminosite_json = json.loads(chaineLuminosite)
    value = str(luminosite_json['value']) #str permet de transformer la valeur (int) en un string, ce qui permet la concaténation dans l'affichage
    #print("Luminosité : " + value + " lm") #Permet d'écrire dans la console la luminosité

    global valueLumi
    valueLumi = value

@app.route('/')
def affTemp():
    return render_template('index.html', temp=valueTemp, humi=valueHumi, lumi=valueLumi, pres=valuePres)

if __name__ == '__main__':

    client = mqtt.Client()
    client.message_callback_add('zigate/attribute_changed/d0d0/01/0405/0000', on_message_humi)
    client.message_callback_add('zigate/attribute_changed/d0d0/01/0402/0000', on_message_temp)
    client.message_callback_add('zigate/attribute_changed/1b2f/01/0406/0000', on_message_pres)
    client.message_callback_add('zigate/attribute_changed/1b2f/01/0400/0000', on_message_lum)
    client.on_connect = on_connect
    
    client.connect("localhost", 1883, 60) #Connexion au broker MQTT
    
    client.loop_start()

    app.run(debug=True, host='0.0.0.0', port=5000) #Lancement du serveur Flask : 10.171.20.39:5000
    
    
