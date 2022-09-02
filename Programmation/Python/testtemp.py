import logging 
import time

import zigate

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

#z = zigate.connect(port='/dev/serial0', gpio=True) #PiZigate
z = zigate.connect(port=None) #Zigate USB

for i in range (0, z.devices.__len__()):
    if z.devices[i].properties :
        device = z.devices[i]
        
        #Capteur Temp/Humidité
        if device.get_property('temperature') :
            print("Température : " + str(device.get_property_value('temperature')) + "°C")
            print("Humidité : " + str(device.get_property_value('humidity')) + "%")