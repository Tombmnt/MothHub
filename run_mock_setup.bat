START "md1" py.exe run_mock_display.py -v -n "mock_display_1"
START "md2" py.exe run_mock_display.py -v -n "mock_display_2"

PAUSE

TASKKILL /fi "WINDOWTITLE eq md1"
TASKKILL /fi "WINDOWTITLE eq md2"