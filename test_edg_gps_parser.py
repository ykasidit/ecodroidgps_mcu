import edg_gps_parser
import time


def test():
    lat, lon, ts, bb = edg_gps_parser.gen_demo_ecodroidgps_gap_broadcast_buffer()
    print("braodcast_buff: {}".format(bb))
    parsed = edg_gps_parser.parse_ecodroidgps_gap_broadcast_buffer(bb)
    print("parsed: {}".format(parsed))
    assert parsed["lat"] == lat
    assert parsed["lon"] == lon
    assert parsed["ts"] == ts

    
if __name__ == "__main__":
    test()
