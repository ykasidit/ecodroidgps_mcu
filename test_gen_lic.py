import bluetooth
import edg_utils
import hashlib


def test():
    ble = bluetooth.BLE()
    ble.active(True)
    bdaddr = ble.config('mac')[1] # ex: (0, b'\x10R\x1cg\xfc\xbe')
    bdaddr_hex = edg_utils.bytes_to_hex(bdaddr)    
    print("bdaddr_hex:", bdaddr_hex)
    lic_hex = edg_utils.gen_lic_hex(bdaddr_hex)
    print("lic_hex:", lic_hex)
    with open('lic','wb') as f:
        f.write(lic_hex.encode('ascii'))
    
    
if __name__ == "__main__":
    test()
