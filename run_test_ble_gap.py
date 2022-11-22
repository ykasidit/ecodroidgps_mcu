# minimal BLE advertise name

import time
import bluetooth
from ble_advertising import advertising_payload as adpl

if __name__=='__main__':
    ble = bluetooth.BLE()
    pl = adpl(name='myname')
    ble.active(True)
    print("mtu:", ble.config)
    i = 0
    while True:
        print("starting new ad: {}".format(i))
        ad_interval_millis = 1000
        ble.gap_advertise(30*1000, adv_data=pl)
        time.sleep(0.001 * ad_interval_millis)
        i += 1
    
        
