#!bin/bash

python3 run_mock_display.py -v -n "mock_display_1" &
python3 run_mock_display.py -v -n "mock_display_2" &

read -rsp $'Press any key to quit...\n' -n1 key

#Kill all processes started by this script:
pkill -P $$