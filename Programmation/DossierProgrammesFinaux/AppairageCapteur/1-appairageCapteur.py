import logging 
import time

import zigate

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

#z = zigate.connect(port='/dev/serial0', gpio=True) #PiZigate
z = zigate.connect(port=None) #Zigate USB

#Appairrage
z.permit_join()
z.is_permitting_join()
