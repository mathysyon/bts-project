import logging 
import time

import zigate

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

#z = zigate.connect(port='/dev/serial0', gpio=True) #PiZigate
z = zigate.connect(port=None) #Zigate USB

print("------------------------Liste des appareils connectés------------------------")
z.get_devices_list()

#Appairrage
z.permit_join()
z.is_permitting_join()
