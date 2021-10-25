import socket, json, logging
from typing import Dict, List
from handlers.data_handler import Data_Handler

class Peripheric_Handler():
    def __init__(self, client_conn: socket.socket, client_addr: List, name: str, data_handler: Data_Handler) -> None:
        self.client_conn = client_conn
        self.client_addr = client_addr
        self.data_handler = data_handler
        self.name = name

    def run(self) -> None:
        raise NotImplementedError("Please write a run method for your peripheral handler!")

    def send_data(self, data:Dict) -> None:

        b_data = json.dumps(data).encode('utf-8')

        try:
            self.client_conn.send(b_data)
        except socket.error as e:
            logging.error('Send failed: ' + e[1])
            #TODO: retry sending a few times

        logging.debug('Data sent: '+ str(b_data))

    def recieve_data(self) -> Dict:
        b_data = self.client_conn.recv(4096)
        logging.debug('Recieved: ' + str(b_data))
        return json.loads(b_data.decode('utf-8'))

    def __del__(self) -> None:
        try:
            self.client_conn.close()
        except socket.error:
            pass # ignore errors if socket already closed