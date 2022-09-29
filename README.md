how to flash the firmware
-------------------------

- Make a working Ubuntu 20.04 GNU\Linux machine.

- make sure python (3.x) is installed and the pip command is working

- run:
pip install esptool adafruit-ampy==1.1.0 pylint mpy-cross==1.14

- erase:
esptool.py --port /dev/ttyUSB0 erase_flash

- flash ori micropython bin: (somehow still required)
esptool.py --chip esp32 --port /dev/ttyUSB0 -b 460800 write_flash -z 0x1000 esp32-idf4-20210202-v1.14.bin

- test below must not get stuck:
export AMPY_PORT=/dev/ttyUSB0
ampy ls

it must output:
/boot.py

- Then, flash our micropython bin:
esptool.py -p /dev/ttyUSB0 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 build-GENERIC/bootloader/bootloader.bin 0x8000 build-GENERIC/partition_table/partition-table.bin 0x10000 build-GENERIC/micropython.bin --verify

- test below must not get stuck
ampy ls

it must output:
/boot.py

- clean, build, flash and test:
./test.sh

it must show:
TEST SUCCESS

- test connect from 'Bluetooth GNSS' app with 'ecodroidgps broadcast mode' enabled in settings

- DONE

---

remove all files from connected esp32
-------------------------------------

- run:
./clean_dev.sh

- then verify:
ampy ls

- output should be empty but not stuck

run tests on local python3
-------------------------
make clean
make -j`nproc`

it must print:
SUCCESS - ALL TESTS PASSED


build .mpy (compiled micropython) files
---------------

./build.sh


push mpy files to esp32 device
-----------------------------

./put.sh


run tests in esp32 device
-------------------------

./test.sh


run a specific test on local python3 example
--------------------------------------------

python3 test_get_sys_platform.py 


run a specific test on esp32 device example
------------------------------------------

ampy run <test file>

example:
ampy run test_get_sys_platform.py 


test, see output of main operation but in limited loops
-------------------------------------------------------

ampy run test_edg_gap_main_loop.py 

test, see output of main operation but in limited loops
-------------------------------------------------------
- reconnect power to device
- open new emacs instance, shell:
busybox microcom -s 115200 /dev/ttyUSB0


how to build micropython esp32 firmware with double precision float
-------------------------------------------------------------------

- Follow https://github.com/micropython/micropython/blob/master/ports/esp32/README.md - but before running final make, change .h file as per https://github.com/micropython/micropython/issues/4380

See https://micropython.org/download/esp32/
See https://docs.micropython.org/en/latest/esp32/tutorial/intro.html


(NOTE: just for reference - below is the original command to flash our micropython bin:
(this command is from the final output of make in above how to build micropython step - just added <port> and --verify):
cd ~/micropython/ports/esp32
/home/kasidit/.espressif/python_env/idf4.0_py2.7_env/bin/python ../../../esp-idf/components/esptool_py/esptool/esptool.py -p /dev/ttyUSB0 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size detect --flash_freq 40m 0x1000 build-GENERIC/bootloader/bootloader.bin 0x8000 build-GENERIC/partition_table/partition-table.bin 0x10000 build-GENERIC/micropython.bin --verify)
