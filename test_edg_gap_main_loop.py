import sys


def test():

    if sys.platform != "esp32":
        return  # this code is for esp32 only
    
    import edg_gap  # import here so wont fail in linux
    edg_gap.main_loop(test_mode=True, demo_position=True)

    
if __name__ == "__main__":
    test()
