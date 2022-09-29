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
from machine import UART
import utime

import adafruit_gps
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

    ble = bluetooth.BLE()
    ble.active(True)
    bdaddr = ble.config('mac')[1] # ex: (0, b'\x10R\x1cg\xfc\xbe')
    bdaddr_hex = edg_utils.bytes_to_hex(bdaddr)
    lic_hex_target = edg_utils.gen_lic_hex(bdaddr_hex)
    lic_hex = None
    try:
        with open('lic','rb') as f:
            lic_hex = f.read().decode('ascii')
    except Exception as ex:
        print("WARNING: read lic_hex exception:", ex)
    print("lic_hex:", lic_hex)
    print("lic_hex_target:", lic_hex_target)
    led.value(1)
    if lic_hex is None or lic_hex != lic_hex_target:
        raise Exception("invalid license")        

    #uart = UART(1, baudrate=9600)
    uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=15, rx=2, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=5000, timeout_char=2)
    #pins=('D15','D2')
    gps = adafruit_gps.GPS(uart)
    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command('PMTK220,1000')
    # Main loop runs forever printing the location, etc. every second.
    last_print = utime.ticks_ms()
  
    i = -1
    test_mode_n_rounds = 10    
    pos = {
        "lat": None,
        "lon": None,
        "ts": None,
    }

    prev_ts = None
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
            #pos = edg_gps_parser.get_next_position(demo_position=demo_position)
            gps.update()
            # Every second print out current location details if there's a fix.
            current = utime.ticks_ms()
            if utime.ticks_diff(last_print, current) >= 1000:
                last_print = current
            if not gps.has_fix:
                # Try again if we don't have a fix yet.
                print('no gnss fix yet...')
                continue
        
            # We have a fix! (gps.has_fix is true)
            # Print out details about the fix like location, date, etc.
            print('=' * 40)  # Print a separator line.
            print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
                gps.timestamp_utc[1],   # Grab parts of the time from the
                gps.timestamp_utc[2],  # struct_time object that holds
                gps.timestamp_utc[0],  # the fix time.  Note you might
                gps.timestamp_utc[3],  # not get all data like year, day,
                gps.timestamp_utc[4],   # month!
                gps.timestamp_utc[5]))
            ts = utime.mktime((gps.timestamp_utc[0], gps.timestamp_utc[1], gps.timestamp_utc[2], gps.timestamp_utc[3], gps.timestamp_utc[4], gps.timestamp_utc[5],0,0))
            print("ts:", ts)
            # check ts has changed
            new_ts = prev_ts is None or ts != prev_ts
            print("check new_ts:", new_ts)
            if new_ts:                
                pass # ok
            else:
                print("not new_ts so retry...")
                continue
            
            # turn on led to signal we got new position
            #led.value(1)
            
            prev_ts = ts

            # ex snippet credit to https://github.com/alexmrqt/micropython-gps.git - examples/gps_simpletest.py
            print('Latitude: {} degrees'.format(gps.latitude))
            print('Longitude: {} degrees'.format(gps.longitude))
            print('Fix quality: {}'.format(gps.fix_quality))
            pos["ts"] = ts
            pos["lat"] = gps.latitude
            pos["lon"] = gps.longitude
            # Some attributes beyond latitude, longitude and timestamp are optional
            # and might not be present.  Check if they're None before trying to use!
            if gps.satellites is not None:
                print('# satellites: {}'.format(gps.satellites))
            if gps.altitude_m is not None:
                print('Altitude: {} meters'.format(gps.altitude_m))
            if gps.track_angle_deg is not None:
                print('Speed: {} knots'.format(gps.speed_knots))
            if gps.track_angle_deg is not None:
                print('Track angle: {} degrees'.format(gps.track_angle_deg))
            if gps.horizontal_dilution is not None:
                print('Horizontal dilution: {}'.format(gps.horizontal_dilution))
            if gps.height_geoid is not None:
                print('Height geo ID: {} meters'.format(gps.height_geoid))


            # create gap payload from position
            edg_payload = edg_gap_payloads.gen_ecodroidgps_gap_broadcast_buffer(pos["lat"], pos["lon"], pos["ts"])
            gap_payload = edg_gap_payloads.eddystone_type_adv_data(edg_payload, name="AZQ")

            # broadcast ble gap buffer
            print('payload: {}'.format(edg_utils.bytes_to_hex(gap_payload)))
            ble.gap_advertise(500*1000, adv_data=gap_payload)            
            
            # turn off led
            #led.value(0)            
        except Exception as ex:
            if test_mode:
                raise ex
            print("WARNING: edg_gap.main_loop() got exception - will retry in 1 sec: {}".format(ex))            
            time.sleep(1.0)
        

if __name__ == "__main__":
    main_loop()
