import math
import os
import hashlib


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


def bytes_to_hex(ba):
    if not isinstance(ba, bytearray):
        ba = bytearray(ba)
    print("ba:", ba)
    return ' '.join(('%02x' % x) for x in ba)


def gen_lic_hex(bdaddr_hex):
    sha = hashlib.sha1()
    salt = "edgb"
    sha.update(bdaddr_hex+salt)
    return bytes_to_hex(sha.digest())
