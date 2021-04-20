import os
import machine
import edg_gap


def main():
    print(os.uname())
    edg_gap.start_gap()


if __name__ == "__main__":
    main()
