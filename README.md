remove all files from connected esp32
-------------------------------------

./clean_dev.sh

Then to verify:
ampy ls


run tests on local python3
-------------------------
make clean
make


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

ampy run test_get_sys_platform.py 

