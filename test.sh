#!/bin/bash

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

echo "running tests on remote dev via ampy..."
find . -maxdepth 1 -name "test*.py" -exec bash -c "echo running {} && ampy run {} || kill \$PPID" \;
exit_if_failed

echo "TEST SUCCESS"
