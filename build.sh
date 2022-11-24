rm *.mpy
find . -maxdepth 1 -name "*.py" -not -name "test*.py" -not -name "main.py" -not -name "boot.py" -not -name ".#*" -not -name "gen_lic.py" -not -name "run_test_ble_gap.py" -exec bash -c "echo \"mpy-cross: {}\" && mpy-cross {} || kill \$PPID"  \;
