import edg_gps_parser
import edg_gap_payloads
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

    lat_int = int(lat*edg_gap_payloads.LAT_LON_RESOLUTION_MULTIPLIER)
    bb = struct.pack('i', lat_int)
    bb_hex = edg_utils.bytes_to_hex(bb)
    lat_int_unpacked = struct.unpack('i', bb)[0]
    print("lat_int_unpacked: ", lat_int_unpacked)
    assert lat_int == lat_int_unpacked
    print("bb_hex: "+bb_hex)
    assert bb_hex == "07 26 63 49"

    pos = edg_gps_parser.get_next_position(demo_position=True)
    edg_payload = edg_gap_payloads.gen_ecodroidgps_gap_broadcast_buffer(pos["lat"], pos["lon"], pos["ts"])
    print("braodcast_buff: {}".format(bb))
    parsed = edg_gap_payloads.parse_ecodroidgps_gap_broadcast_buffer(edg_payload)
    print("parsed: {}".format(parsed))
    assert parsed["lat"] == pos["lat"]
    assert parsed["lon"] == pos["lon"]
    assert parsed["ts"] == pos["ts"]
    
    ba = edg_gap_payloads.gen_ecodroidgps_gap_broadcast_buffer(pos["lat"], pos["lon"], pos["ts"])
    gap_payload = edg_gap_payloads.eddystone_type_adv_data(ba)
    print("gap_payload: {}".format(edg_utils.bytes_to_hex(gap_payload)))
    assert gap_payload[:-4] == b'\x02\x01\x1a\x03\x03\xaa\xfe\x12\x16\xaa\xfe\x30\x00\xe1\x07\x26\x63\x49\xf9\xd9\x9c\xb6'

   
if __name__ == "__main__":
    test()
