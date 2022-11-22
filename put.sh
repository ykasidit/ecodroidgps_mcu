#!/bin/bash

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

echo "putting files..."
find . -maxdepth 1 -name "*.py" -exec bash -c "echo \"put {}\" && ampy put {} || kill \$PPID"  \;
exit_if_failed

echo "final put main.py" # required otherwise somehow only with main.mpy it wont work on boot - confirmed in https://forum.micropython.org/viewtopic.php?t=8410
ampy put main.py  
echo "final put boot.py"
ampy put boot.py

exit_if_failed
echo "PUT SUCCESS"
