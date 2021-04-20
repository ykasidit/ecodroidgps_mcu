import math
import os


def get_module_path():
    return os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    

# amazing formula - from https://stackoverflow.com/questions/8898807/pythonic-way-to-iterate-over-bits-of-integer
def bits(n):
    while n:
        b = n & (~n+1)
        yield b
        n ^= b
        
        
def get_on_bit_offset_list(val):
    ret = []
    for b in bits(val):
        ret.append(int(math.log(b,2))) # b is value, we want bit offset
    return ret


def gen_edg_ln_feature_bitmask_hex_dump_str():
    import numpy as np
    # gen lnf bitmask
    bitmask = int(0)

    ln_bits = [
        ble_bit_offsets.ln_feature.Instantaneous_Speed_Supported,
        ble_bit_offsets.ln_feature.Location_Supported,
        ble_bit_offsets.ln_feature.Elevation_Supported,
        ble_bit_offsets.ln_feature.UTC_Time_Supported,
        ble_bit_offsets.ln_feature.Position_Status_Supported
    ]
    for bit_offset in ln_bits:
        print(("turn on bit:", bit_offset))
        bitmask = bit_utils.set_bit(bitmask, bit_offset)

    buffer = np.uint32(bitmask).tobytes()
    print(("buffer: {} type: {}", buffer, type(buffer)))
    return buffer.hex()


def bytes_to_hex(ba):
    if not isinstance(ba, bytearray):
        ba = bytearray(ba)
    print("ba:", ba)
    return ' '.join(('%02x' % x) for x in ba)
