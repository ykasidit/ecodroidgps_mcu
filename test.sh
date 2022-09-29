#!/bin/bash

exit_if_failed() {
    if [ $? -ne 0 ]; then
	echo "ABORT: Previous step failed"
	exit 1
    fi
}

echo "run: ./clean_dev.sh"
./clean_dev.sh
exit_if_failed

echo "run: ./build_and_put.sh"
./build_and_put.sh
exit_if_failed

echo "gen license..."
ampy run gen_lic.py
exit_if_failed

echo "running tests on remote dev via ampy..."
find . -maxdepth 1 -name "test*.py" -not -name "test_000_compile_and_lint_all_py_files.py" -exec bash -c "echo running {} && ampy run {} || kill \$PPID" \;
exit_if_failed

echo "TEST SUCCESS"
