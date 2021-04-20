find . -maxdepth 1 -name "*.py" -not -name "test*.py" -exec bash -c "echo \"mpy-cross: {}\" && mpy-cross {} || kill \$PPID"  \;
