from logging import debug
import logging
import socket, time
from typing import List

from .peripheric_handler import Peripheric_Handler
from database_service import Database_Service

class Display_Handler(Peripheric_Handler):
    def __init__(self, client_conn: socket.socket, client_addr: List, name: str, database_service: Database_Service) -> None:
        logging.debug('Loaded display handler for ' + str(name))
        super().__init__(client_conn, client_addr, name, database_service, "display")

    def run(self) -> None:
        while(1):
            self.send_data({
                "command": "speed",
                "value": 0
            })
            time.sleep(0.5)
