rm *.mpy
find . -maxdepth 1 -name "*.py" -not -name "test*.py" -not -name "main.py" -not -name "boot.py" -not -name ".#*" -exec bash -c "echo \"mpy-cross: {}\" && mpy-cross {} || kill \$PPID"  \;
