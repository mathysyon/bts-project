import json
from time import time, sleep
from datetime import datetime

while True:
    with open('/home/pi/.zigate.json') as zigateJson:

        data = json.load(zigateJson)
        date = datetime.now()

        print("------[{}:{}:{}]------".format(date.hour,date.minute,date.second)) #Affiche HH:MM:SS
        temp = data["devices"][0]["endpoints"][0]["clusters"][0]["attributes"][0]["value"] #humidite = z.devices[0].get_property('humidity')
        hum = data["devices"][0]["endpoints"][0]["clusters"][1]["attributes"][0]["value"]
        presence=data["devices"][1]["endpoints"][0]["clusters"][0]["attributes"][0]["value"]
        luminosite=data["devices"][1]["endpoints"][0]["clusters"][1]["attributes"][0]["value"]
        print("Température : {0}°C".format(temp))
        print("Humidité : {0} %".format(hum)) 
        print("Luminosité : {0} lm".format(luminosite))
        print("Présence : {0}".format(presence)) 

        sleep(180 - time() % 180) #print toutes les 6 minutes 

        #print("%s" %(item["discovery"])) #print l'addr
