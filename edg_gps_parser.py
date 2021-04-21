import math
import struct
import time

LAT_LON_RESOLUTION_MULTIPLIER = math.pow(10.0, 7)
ECODROIDGPS_EID_BROADCAST_HEADER_BYTE_VERSION1 = 0xE1


def gen_position_status_and_location(flag_bit_list, logger_state_dict):
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

        # set value of position_status bit to 1
        flag_bit_list.append(ble_bit_offsets.location_and_speed.Position_Status)

        
        lat = gga.latitude
        lon = gga.longitude

        ret = gen_lat_lon_buffer(lat, lon)

        # set location_present flag
        flag_bit_list.append(ble_bit_offsets.location_and_speed.Location_Present)

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


def gen_demo_ecodroidgps_gap_broadcast_buffer():
    lat = 123.1234567
    lon = -1.0*lat
    ts = int(time.time())
    #print("ori ts: {}".format(ts))
    bb = gen_ecodroidgps_gap_broadcast_buffer(lat, lon, ts)
    return lat, lon, ts, bb
    

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
