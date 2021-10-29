import logging
from modules.socket_client import Socket_Client
from modules.mock.mock_display import Mock_Display_Peripheral

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

white_square_msg = {
    "command":"square",
    "pos_x":10,
    "pos_y":10,
    "width":25,
    "height":35,
    "color":[255, 255, 255]
}

black_square_msg = {
    "command":"square",
    "pos_x":25,
    "pos_y":25,
    "width":40,
    "height":20,
    "color":[0, 0, 0]
}

screen = Mock_Display_Peripheral(320, 240, "mock_display_1", "127.0.0.1")
screen.run()

logging.info("Done!")