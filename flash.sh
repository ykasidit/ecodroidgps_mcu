#!/bin/bash

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

if [ -z "$AMPY_PORT" ]
then
    echo "please export env AMPY_PORT, example:"
    echo "export AMPY_PORT=/dev/ttyUSB0"
    exit 1
fi


echo "### using env AMPY_PORT: $AMPY_PORT"
echo "### erase"
esptool.py --port $AMPY_PORT erase_flash
exit_if_failed


echo "### flash ori mpy bin"
esptool.py --port $AMPY_PORT -b 460800 write_flash -z 0x1000  esp32-20220618-v1.19.1.bin
exit_if_failed

echo "### flash our mpy bin"
esptool.py -p $AMPY_PORT -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 build-GENERIC/bootloader/bootloader.bin 0x8000 build-GENERIC/partition_table/partition-table.bin 0x10000 build-GENERIC/micropython.bin --verify
exit_if_failed

echo "### flash and test the rest"
./test.sh
exit_if_failed

echo "### flash SUCCESS"
