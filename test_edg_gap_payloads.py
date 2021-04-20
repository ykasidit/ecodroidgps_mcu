import edg_gap_payloads
import edg_gps_parser
import time
import edg_utils
import struct


def test():
    lat_str = "123.1234567"
    lat = float(lat_str)    
    lon = -1.0*lat
    ts = 0

    # test float can hold vals (had issues on esp32)
    print("lat_str: ", lat_str)
    print("lat: ", lat)
    assert str(lat) == lat_str

    lat_int = int(lat*edg_gps_parser.LAT_LON_RESOLUTION_MULTIPLIER)
    bb = struct.pack('i', lat_int)
    bb_hex = edg_utils.bytes_to_hex(bb)
    lat_int_unpacked = struct.unpack('i', bb)[0]
    print("lat_int_unpacked: ", lat_int_unpacked)
    assert lat_int == lat_int_unpacked
    print("bb_hex: "+bb_hex)
    assert bb_hex == "07 26 63 49"
    '''
    TODO esp32 facing:
    ba: bytearray(b'\x00&cI')
    lat_int_unpacked:  1231234560
    bb_hex: 00 26 63 49
    '''
    
    ba = edg_gps_parser.gen_ecodroidgps_gap_broadcast_buffer(lat, lon, ts)
    gap_payload = edg_gap_payloads.eddystone_type_adv_data(ba)
    print("gap_payload: {}".format(edg_utils.bytes_to_hex(gap_payload)))
    assert gap_payload == b'\x02\x01\x1a\x03\x03\xaa\xfe\x12\x16\xaa\xfe\x30\x00\xe1\x07\x26\x63\x49\xf9\xd9\x9c\xb6\x00\x00\x00\x00'

   
if __name__ == "__main__":
    test()
