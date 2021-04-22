# cant run in linux python
# pylint: disable=E0401,E1101

import os
import sys
import time
import gc
import math
import struct

import bluetooth
import machine

from ble_advertising import advertising_payload
import edg_gap_payloads
import edg_gps_parser
import edg_utils


def main_loop(test_mode=False, demo_position=False):

    print("start_gap() os.uname:", os.uname())
    print("sys.platform:", sys.platform)
    if sys.platform != "esp32":
        raise Exception("unsupported platform: {}".format(sys.platform))

    led = machine.Pin(2, machine.Pin.OUT)
    led.value(0)

    led.value()
    ble = bluetooth.BLE()
    ble.active(True)
  
    i = -1
    test_mode_n_rounds = 10
    while True:
        i += 1
        if test_mode:
            print("NOTE: test_mode == True")
            if i > test_mode_n_rounds:
                print("test_mode == True and i > test_mode_n_rounds so exit now")
                return

        # clear and print current free RAM
        gc.collect()
        mem_free = gc.mem_free()
        print("edg_gap.main_loop() i:", i, "mem_free:", mem_free)

        try:

            # read position from gnss device
            pos = edg_gps_parser.get_next_position(demo_position=demo_position)

            # turn on led to signal we got position
            led.value(1)

            # create gap payload from position
            edg_payload = edg_gap_payloads.gen_ecodroidgps_gap_broadcast_buffer(pos["lat"], pos["lon"], pos["ts"])
            gap_payload = edg_gap_payloads.eddystone_type_adv_data(edg_payload)

            # broadcast ble gap buffer
            print('payload: {}'.format(edg_utils.bytes_to_hex(gap_payload)))
            ble.gap_advertise(500*1000, adv_data=gap_payload)            
            
            # turn off led
            led.value(0)            
        except Exception as ex:
            if test_mode:
                raise ex
            print("WARNING: edg_gap.main_loop() got exception - will retry in 1 sec: {}".format(ex))
            led.value(0)
            time.sleep(1.0)
        


