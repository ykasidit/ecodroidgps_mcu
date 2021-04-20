#!/bin/bash

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

echo "putting files..."
find . -maxdepth 1 -name "*.py" -not -name "test*.py" -exec bash -c "echo \"put {}\" && ampy put {} || kill \$PPID"  \;
exit_if_failed
echo "PUT SUCCESS"
