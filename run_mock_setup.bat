START "md1" py.exe -m modules.mock.mock_display
START "md2" py.exe -m modules.mock.mock_display
START "db" py.exe -m modules.database
START "gps" py.exe -m modules.mock.mock_gps

PAUSE

TASKKILL /fi "WINDOWTITLE eq gps"
TASKKILL /fi "WINDOWTITLE eq db"
TASKKILL /fi "WINDOWTITLE eq md1"
TASKKILL /fi "WINDOWTITLE eq md2"