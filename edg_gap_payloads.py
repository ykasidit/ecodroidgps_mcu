import time
import math
import struct

import edg_utils

# this file should be testable/runnable in linux too - dont put micropython-specific code in this file (put them all in edg_gap.py)

FRAME_TYPE_EID = 0x30
LAT_LON_RESOLUTION_MULTIPLIER = math.pow(10.0, 7)
ECODROIDGPS_EID_BROADCAST_HEADER_BYTE_VERSION1 = 0xE1


def eddystone_type_adv_data(data, frame_type=FRAME_TYPE_EID):
    #print("Encoding data for Eddystone beacon: '{}'".format(edg_utils.bytes_to_hex(data)))
    data_len = len(data)
    #print(("data_len:", data_len))

    message = [
            0x02,   # Flags length
            0x01,   # Flags data type value
            0x1a,   # Flags data

            0x03,   # Service UUID length
            0x03,   # Service UUID data type value
            0xaa,   # 16-bit Eddystone UUID
            0xfe,   # 16-bit Eddystone UUID

            5 + len(data), # Service Data length
            0x16,   # Service Data data type value
            0xaa,   # 16-bit Eddystone UUID
            0xfe,   # 16-bit Eddystone UUID

            frame_type,   # Eddystone-url frame type
            0x00,   # txpower
            ]

    message += data

    return bytearray(message)


def gen_position_status_and_location(logger_state_dict):
    gga = logger_state_dict['gga']
    gsa = logger_state_dict['gsa']
    if gga is None:
        raise Exception('gga is still None')
    if gsa is None:
        raise Exception('gsa is still None')
    
    # Fix types can be: 1 = no fix, 2 = 2D fix, 3 = 3D fix
    fix_type = gsa.mode_fix_type

    # spec says position_status is a two bit len field in flag so no payload: 0 = no position, 1 = position ok
    if fix_type >= 2:        
        lat = gga.latitude
        lon = gga.longitude

        ret = gen_lat_lon_buffer(lat, lon)
        return ret
        
    else:
        # leave flags as 0
        pass
    
    return None


def gen_lat_lon_buffer(lat, lon):
    lat *= LAT_LON_RESOLUTION_MULTIPLIER
    lon *= LAT_LON_RESOLUTION_MULTIPLIER
    ret = struct.pack('i', int(lat)) + struct.pack('i', int(lon))
    return ret


def gen_ecodroidgps_gap_broadcast_buffer(lat, lon, timestamp):
    """
    format:
    version: uint8: 0xE1
    lat: int32: this is latitude multiplied by LAT_LON_RESOLUTION_MULTIPLIER
    lon: int32: this is longitude multiplied by LAT_LON_RESOLUTION_MULTIPLIER
    """
    ret = bytearray([ECODROIDGPS_EID_BROADCAST_HEADER_BYTE_VERSION1])
    ret += gen_lat_lon_buffer(lat, lon)
    ret += struct.pack('I', int(timestamp))
    return ret
   

def parse_ecodroidgps_gap_broadcast_buffer(ba):
    pos = 0
    ver = ba[pos]
    pos += 1
    print(("ver:", hex(ver)))
    assert ver == ECODROIDGPS_EID_BROADCAST_HEADER_BYTE_VERSION1
    ret = {}

    # lat lon
    for float_param in ["lat", "lon"]:
        param_buffer = ba[pos:pos+4]
        pos += 4
        assert len(param_buffer) == 4
        val = struct.unpack('i', param_buffer)[0]
        val = float(val) / float(LAT_LON_RESOLUTION_MULTIPLIER)
        ret[float_param] = val

    # ts
    param_buffer = ba[pos:pos+4]
    pos += 4
    ts = struct.unpack('I', param_buffer)[0]
    ret["ts"] = ts

    return ret
