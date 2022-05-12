#!bin/bash

python3 -m modules.mock.mock_display &
python3 -m modules.mock.mock_display &
python3 -m modules.database &
python3 -m modules.mock.mock_gps &

read -rsp $'Press any key to quit...\n' -n1 key

#Kill all processes started by this script:
pkill -P $$