from logging import debug
import logging
import socket, time
from typing import List

from .peripheric_handler import Peripheric_Handler
from .data_handler import Data_Handler

class Display_Handler(Peripheric_Handler):
    def __init__(self, client_conn: socket.socket, client_addr: List, name: str, data_handler: Data_Handler) -> None:
        logging.debug('Loaded display handler for ' + str(name))
        super().__init__(client_conn, client_addr, name, data_handler)

    def run(self) -> None:
        while(1):
            self.send_data({
                "command": "speed",
                "value": self.data_handler.get_speed()
            })
            time.sleep(0.5)
