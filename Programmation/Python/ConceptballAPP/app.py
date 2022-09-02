#from re import A
import paho.mqtt.client as mqtt
import json
from flask import Flask, render_template
import mariadb
from datetime import datetime

db = mariadb.connect(user="root", password="conceptball", host='localhost', database='releve_conceptball') #connexion à bdd

app = Flask(__name__)

valueTemp=0
valueHumi=0
valuePres=""
valueLumi=0

def insertReleve(value_json, id_Capteur):
    now = datetime.now()
    cursor = db.cursor()
    insert = "INSERT INTO Releve (r_dateheure_Releve, r_valeur_Releve, c_id_Capteur) VALUES ('{}', {}, '{}')".format(now.strftime('%Y/%m/%d %H:%M:%S'), str(value_json['value']), id_Capteur) #requête sql
    cursor.execute(insert) #éxecute et transmet la requête SQL
    db.commit() #valide la transaction
    cursor.close()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))    

    client.subscribe("zigate/attribute_changed/#")

# The callback for when a PUBLISH message is received from the server.
def on_message_humi(client, userdate, msg):
    now = datetime.now()

    chaineHumidite=str(msg.payload)
    chaineHumidite = chaineHumidite[2:-1]
    humidite_json = json.loads(chaineHumidite)
    value = str(humidite_json['value'])

    #Récupère ID du capteur
    cursor = db.cursor()
    select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='humidity' LIMIT 1"
    cursor.execute(select)
    result = cursor.fetchone() 
    c_id_Capteur = result[0]

    #Récupère la dernière date à laquelle la dernière valeur à été mise
    cursor = db.cursor()
    selectDatePrecedente = "SELECT MAX(r_dateheure_Releve) FROM Releve WHERE c_id_Capteur={} LIMIT 1".format(c_id_Capteur) 
    cursor.execute(selectDatePrecedente)
    resultDate = cursor.fetchone() 
    precedenteDate = resultDate[0]
    cursor.close() #A NE SURTOUT PAS OUBLIE SINON ERREUR DE SYNCHRO

    if precedenteDate is None: #Si il n'y a aucune valeur dans la bdd pour éviter une erreur 
        precedenteDate=now
        insertReleve(humidite_json, c_id_Capteur)

    #Récupère différence entre maintenant et le dernier datetime en minutes
    difDateTime = now - precedenteDate
    difDateTime = difDateTime.total_seconds()/60
    
    #Insert les données seulement si le précédent datetime de il y a 10 min
    if((difDateTime > 10) and (precedenteDate != now)):
        insertReleve(humidite_json, c_id_Capteur)

    global valueHumi
    valueHumi = value

def on_message_temp(client, userdate, msg):
    now = datetime.now()

    chaineTemperature=str(msg.payload)
    chaineTemperature = chaineTemperature[2:-1]
    temperature_json = json.loads(chaineTemperature)
    value = str(temperature_json['value'])

    #Récupère ID du capteur
    cursor = db.cursor()
    select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='temperature' LIMIT 1"
    cursor.execute(select)
    result = cursor.fetchone() 
    c_id_Capteur = result[0]

    #Récupère la dernière date à laquelle la dernière valeur à été mise
    cursor = db.cursor()
    selectDatePrecedente = "SELECT MAX(r_dateheure_Releve) FROM Releve WHERE c_id_Capteur={} LIMIT 1".format(c_id_Capteur) 
    cursor.execute(selectDatePrecedente)
    resultDate = cursor.fetchone() 
    precedenteDate = resultDate[0]
    cursor.close() #A NE SURTOUT PAS OUBLIE SINON ERREUR DE SYNCHRO

    if precedenteDate is None: #Si il n'y a aucune valeur dans la bdd pour éviter une erreur 
        precedenteDate=now
        insertReleve(temperature_json, c_id_Capteur)

    #Récupère différence entre maintenant et le dernier datetime en minutes
    difDateTime = now - precedenteDate
    difDateTime = difDateTime.total_seconds()/60 
    
    #Insert les données seulement si le précédent datetime date de il y a 10 min
    if((difDateTime > 10) and (precedenteDate != now)):
        insertReleve(temperature_json, c_id_Capteur)

    global valueTemp
    valueTemp = value

#def on_message_pres(client, userdate, msg):
#    global now
#
#    chainePresence=str(msg.payload)
#    chainePresence = chainePresence[2:-1] 
#    presence_json = json.loads(chainePresence)
#    value = str(presence_json['value'])

     #Récupère ID du capteur
#    cursor = db.cursor()
#    select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='presence'"
#    cursor.execute(select)
#    result = cursor.fetchone() 
#    c_id_Capteur = result[0]

#    insert = "INSERT INTO Releve (r_dateheure_Releve, r_valeur_Releve, c_id_Capteur) VALUES ('{}', {}, '{}')".format(now.strftime('%Y/%m/%d %H:%M:%S'), str(presence_json['value']), c_id_Capteur) #requête sql
#    cursor.execute(insert) #éxecute et transmet la requête SQL
#    db.commit() #valide la transaction

#    global valuePres
#    valuePres = value

def on_message_lum(client, userdate, msg):
    now = datetime.now()
    
    chaineLuminosite=str(msg.payload)
    chaineLuminosite = chaineLuminosite[2:-1] #Supprime le b' et le ' à la fin de la chaine permettant d'exploiter les données
    luminosite_json = json.loads(chaineLuminosite)
    value = str(luminosite_json['value']) #str permet de transformer la valeur (int) en un string, ce qui permet la concaténation dans l'affichage

    #Récupère ID du capteur
    cursor = db.cursor()
    select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='luminosity' LIMIT 1"
    cursor.execute(select)
    result = cursor.fetchone() 
    c_id_Capteur = result[0]

    #Récupère la dernière date à laquelle la dernière valeur à été mise
    cursor = db.cursor()
    selectDatePrecedente = "SELECT MAX(r_dateheure_Releve) FROM Releve WHERE c_id_Capteur={} LIMIT 1".format(c_id_Capteur) 
    cursor.execute(selectDatePrecedente)
    resultDate = cursor.fetchone() 
    precedenteDate = resultDate[0]
    cursor.close() #A NE SURTOUT PAS OUBLIE SINON ERREUR DE SYNCHRO

    #Si il n'y a aucune valeur dans la bdd pour éviter une erreur
    if precedenteDate is None: 
        precedenteDate=now
        insertReleve(luminosite_json, c_id_Capteur)

    difDateTime = now - precedenteDate
    difDateTime = difDateTime.total_seconds()/60 #calcul la différence entre maintenant et la dernière valeur en minutes
    
    #Insert les données seulement si le précédent datetime de il y a 10 min est différent
    if((difDateTime > 10) and (precedenteDate != now)): 
        insertReleve(luminosite_json, c_id_Capteur)

    global valueLumi
    valueLumi = value 

@app.route('/')
def affValue():
    return render_template('index.html', temp=valueTemp, humi=valueHumi, lumi=valueLumi, pres=valuePres)

if __name__ == '__main__':

    client = mqtt.Client()
    client.message_callback_add('zigate/attribute_changed/d0d0/01/0405/0000', on_message_humi)
    client.message_callback_add('zigate/attribute_changed/d0d0/01/0402/0000', on_message_temp)
    #client.message_callback_add('zigate/attribute_changed/1b2f/01/0406/0000', on_message_pres)
    client.message_callback_add('zigate/attribute_changed/1b2f/01/0400/0000', on_message_lum)
    client.on_connect = on_connect
    
    client.connect("localhost", 1883, 60) #Connexion au broker MQTT
    
    client.loop_start()

    app.run(debug=True, host='0.0.0.0', port=5000) #Lancement du serveur Flask : 10.171.20.39:5000