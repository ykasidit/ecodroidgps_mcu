import os
import sys
import time

import bluetooth
import machine

from ble_advertising import advertising_payload
import edg_gap_payloads
import edg_gps_parser
import edg_utils

    
def start_gap(test_mode=False):

    print("start_gap() os.uname:", os.uname())
    print("sys.platform:", sys.platform)
    if sys.platform != "esp32":
        raise Exception("unsupported platform: {}".format(sys.platform))

    ble = bluetooth.BLE()
    pin = machine.Pin(2, machine.Pin.OUT)

    ble.active(True)
    '''
    gap_payload = advertising_payload(
        name="edg"
    )
    '''
  
    i = -1
    test_mode_n_rounds = 10
    while True:
        i += 1
        if test_mode and i > test_mode_n_rounds:
            return    
        print("i:", i)
        lat, lon, ts, bb = edg_gps_parser.gen_demo_ecodroidgps_gap_broadcast_buffer()
        gap_payload = edg_gap_payloads.eddystone_type_adv_data(bb)
        print('payload: {}'.format(edg_utils.bytes_to_hex(gap_payload)))
        pin.value(i%2)
        ble.gap_advertise(500*1000, adv_data=gap_payload)
        time.sleep(1.0)
