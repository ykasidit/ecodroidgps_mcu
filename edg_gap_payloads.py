import struct
import edg_utils

FRAME_TYPE_EID = 0x30


def eddystone_type_adv_data(data, frame_type=FRAME_TYPE_EID):
    print("Encoding data for Eddystone beacon: '{}'".format(edg_utils.bytes_to_hex(data)))
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
