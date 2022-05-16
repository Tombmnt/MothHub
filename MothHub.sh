#!/bin/bash

python3 -m modules.database &
python3 -m modules.gps &
python3 -m modules.imu &

read -rsp $'Press any key to quit...\n' -n1 key

#Kill all processes started by this script:
pkill -P $$