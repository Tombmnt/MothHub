START "md1" py.exe -m modules.mock.mock_display
START "md2" py.exe -m modules.mock.mock_display
START "gps" py.exe -m modules.mock.mock_gps

PAUSE

TASKKILL /fi "WINDOWTITLE eq md1"
TASKKILL /fi "WINDOWTITLE eq md2"
TASKKILL /fi "WINDOWTITLE eq gps"