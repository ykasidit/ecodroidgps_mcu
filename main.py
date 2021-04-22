# cant run in linux python
# pylint: disable=E0401
import machine  
import time
import edg_gap
import sys


def main():
    if sys.platform != "esp32":
        return  # this code is for esp32 only

    # initial start led signal: quick on-off-on-off
    led = machine.Pin(2, machine.Pin.OUT)
    for i in range(4):
        led.value((i+1)%2)
        time.sleep(0.3)
        
    edg_gap.main_loop()


if __name__ == "__main__":
    main()
