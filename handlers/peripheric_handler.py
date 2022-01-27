from datetime import datetime
from os import error
import socket, json, logging, time, sys
from typing import Dict, List
from database_service import Database_Service

MAX_TRIES = 10

class Peripheric_Handler():
    def __init__(self, client_conn: socket.socket, client_addr: List, name: str, database_service: Database_Service, database_name: str) -> None:
        self.client_conn = client_conn
        self.client_addr = client_addr
        self.name = name
        self._database_service = database_service
        self._database_name = database_name

    def run(self) -> None:
        raise NotImplementedError("Please write a run method for your peripheral handler!")

    def save_data(self, data: Dict) -> None:
        self._database_service.insert_data(self._database_name, data)

    # from_date has to be further in time than to_date. Ex: from 25/02/2022 to 30/02/2022
    def load_data(self, from_date: datetime, to_date: datetime) -> List:
        return self._database_service.obtain_data(self._database_name, from_date, to_date)

    def send_data(self, data: Dict) -> None:

        b_data = json.dumps(data).encode('utf-8')

        for i in range(1, MAX_TRIES + 1):
            try:
                self.client_conn.send(b_data)
                logging.debug('[' + self.name + '] Data sent: '+ str(b_data))
                break # success => break out of the loop.
            except socket.error as e:
                logging.error('[' + self.name + '] Send failed: ' + str(e) + ', retrying... (' + str(i) + '/' + str(MAX_TRIES) + ')')
                time.sleep(1)

                if(i == MAX_TRIES): #last try failed
                    logging.error('[' + self.name + '] Client lost, exiting.')
                    sys.exit() # kill this thread. 
        
    def recieve_data(self) -> Dict:
        try:
            b_data = self.sock.recv(4096)
            self.log.debug('Recieved: ' + str(b_data))
            if b_data:
                return json.loads(b_data.decode('utf-8'))
            else:
                logging.error('[' + self.name + '] Client lost, exiting.')
                sys.exit() # kill this thread. 

        except socket.error as e:
            self.log.error("Failed to recieve data: "+ str(e))
            logging.error('[' + self.name + '] Client lost, exiting.')
            sys.exit() # kill this thread. 

    def __del__(self) -> None:
        try:
            self.client_conn.close()
        except socket.error:
            pass # ignore errors if socket already closed