import paho.mqtt.client as mqtt
import json
import mariadb
import datetime
import time

db = mariadb.connect(user="root", password="conceptball", host='localhost', database='releve_conceptball') #connexion à bdd

valueTemp=0
valueHumi=0
valueLumi=0

temperature_json = ""
c_id_Capteur_temp = 0
humidite_json = ""
c_id_Capteur_humi = 0
luminosite_json = ""
c_id_Capteur_lumi = 0

def insertReleve(value, id_Capteur):
    now = datetime.datetime.now() - datetime.timedelta(seconds=5) #Permet d'avoir un temps sans secondes dans la bdd
    
    cursor = db.cursor()
    insert = "INSERT INTO Releve (r_dateheure_Releve, r_valeur_Releve, c_id_Capteur) VALUES ('{}', {}, '{}')".format(now.strftime('%Y/%m/%d %H:%M:%S'), value, id_Capteur) #requête sql
    print(insert)
    cursor.execute(insert) #éxecute et transmet la requête SQL
    db.commit() #valide la transaction
    cursor.close()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))    

    client.subscribe("zigate/attribute_changed/#")

# The callback for when a PUBLISH message is received from the server.
def on_message_humi(client, userdata, msg):

    chaineHumidite=str(msg.payload) #Récupère la chaine postée sur le topic ou l'on est abonné 
    chaineHumidite = chaineHumidite[2:-1]
    humidite_json = json.loads(chaineHumidite)
    value = str(humidite_json['value'])

    #Récupère ID du capteur
    cursor = db.cursor()
    select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='humidity' LIMIT 1"
    cursor.execute(select)
    result = cursor.fetchone() 
    c_id_Capteur = result[0]
    cursor.close() #A NE SURTOUT PAS OUBLIE SINON ERREUR DE SYNCHRO

    global c_id_Capteur_humi
    global valueHumi
    c_id_Capteur_humi = c_id_Capteur
    valueHumi = value

def on_message_temp(client, userdata, msg):

    chaineTemperature=str(msg.payload) #Récupère la chaine postée sur le topic ou l'on est abonné 
    chaineTemperature = chaineTemperature[2:-1]
    temperature_json = json.loads(chaineTemperature)
    value = str(temperature_json['value'])

    #Récupère ID du capteur
    cursor = db.cursor()
    select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='temperature' LIMIT 1"
    cursor.execute(select)
    result = cursor.fetchone() 
    c_id_Capteur = result[0]
    cursor.close() #A NE SURTOUT PAS OUBLIE SINON ERREUR DE SYNCHRO
    
    global valueTemp
    global c_id_Capteur_temp 
    c_id_Capteur_temp = c_id_Capteur
    valueTemp = value

def on_message_lumi(client, userdata, msg):

    chaineLuminosite=str(msg.payload) #Récupère la chaine postée sur le topic ou l'on est abonné 
    chaineLuminosite = chaineLuminosite[2:-1]
    luminosite_json = json.loads(chaineLuminosite)
    value = str(luminosite_json['value'])

    #Récupère ID du capteur
    cursor = db.cursor()
    select = "SELECT c_id_Capteur FROM Capteur WHERE c_type_Capteur='luminosity' LIMIT 1"
    cursor.execute(select)
    result = cursor.fetchone() 
    c_id_Capteur = result[0]
    cursor.close() #A NE SURTOUT PAS OUBLIE SINON ERREUR DE SYNCHRO
    
    global valueLumi
    global c_id_Capteur_lumi
    c_id_Capteur_lumi = c_id_Capteur
    valueLumi = value

if __name__ == '__main__':

    client = mqtt.Client()
    client.message_callback_add('zigate/attribute_changed/afbe/01/0405/0000', on_message_humi) #humidité
    client.message_callback_add('zigate/attribute_changed/afbe/01/0402/0000', on_message_temp) #température
    client.message_callback_add('zigate/attribute_changed/e511/01/0400/0000', on_message_lumi) #luminosité
    client.on_connect = on_connect
    
    client.connect("localhost", 1883, 60) #Connexion au broker MQTT

    client.loop_start()
    time.sleep(4) #délai pour initialiser les données
    if c_id_Capteur_temp != 0:   
        insertReleve(valueTemp, c_id_Capteur_temp)
        print("{} : 'Temp' insérée".format(datetime.datetime.now()))
    
    if c_id_Capteur_humi != 0:
        insertReleve(valueHumi, c_id_Capteur_humi)
        print("{} : 'Humi' insérée".format(datetime.datetime.now()))

    if c_id_Capteur_lumi != 0:
        insertReleve(valueLumi, c_id_Capteur_lumi)
        print("{} : 'Lumi' insérée".format(datetime.datetime.now()))
    
    client.loop_stop()

