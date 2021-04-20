#!/bin/bash

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

ampy put *.py
exit_if_failed

ampy run $1
exit_if_failed
