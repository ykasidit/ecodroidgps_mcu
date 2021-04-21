find . -maxdepth 1 -name "*.py" -not -name "test*.py" -not -name ".#*" -exec bash -c "echo \"mpy-cross: {}\" && mpy-cross {} || kill \$PPID"  \;
