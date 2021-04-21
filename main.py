import edg_gap
import machine


def main():
    pin = machine.Pin(2, machine.Pin.OUT)
    pin.value(1)    
    edg_gap.start_gap()


if __name__ == "__main__":
    main()
