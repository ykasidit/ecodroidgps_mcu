import time
from ble_advertising import advertising_payload
import bluetooth
import edg_payloads


def start_gap():
    ble = bluetooth.BLE()
    pin = machine.Pin(2, machine.Pin.OUT)

    ble.active(True)
    '''
    gap_payload = advertising_payload(
        name="edg"
    )
    '''
    gap_payload = edg_payloads.eddystone_type_adv_data(b'\x13', FRAME_TYPE_EID)
    
    for i in range(60):
        print("i:", i)
        now = time.time()
        print('now: {}'.format(now))
        print('payload: {}'.format(bytes_to_hex(gap_payload)))
        pin.value(i%2)
        ble.gap_advertise(500*1000, adv_data=gap_payload)
        time.sleep(1.0)
