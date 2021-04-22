import time


def get_next_position(demo_position=False):
    """ Get parsed nmea (from uart) position dict
    Parse and keep-states of nmea stream until we get new GGA sentence
    """
    ret = {}
    if demo_position:
        # note - read from file, sleep until matches 1 sec from last report
        lat = 123.1234567
        lon = -1.0*lat
        ts = int(time.time())
        ret["lat"] = lat
        ret["lon"] = lon
        ret["ts"] = ts
        time.sleep(0.9)
    else:
        raise Exception("TODO read nmea from uart and parse required data")
    return ret



