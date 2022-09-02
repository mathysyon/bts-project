import logging
import time

import zigate

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

#z = zigate.connect(port='/dev/serial0', gpio=True) #PiZigate
z = zigate.connect(port=None) #Zigate USB

z.erase_persistent()
z.factory_reset()

while True:
    len_devices = len(z.devices)
    if len_devices == 0:
        print('Reset finito!')
        break

    print(len_devices)
    print('.', end='')
    time.sleep(5.0)
