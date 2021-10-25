import socket, sys, logging, json
from typing import Any, Dict

PORT = 6684

class Socket_Client():
    def __init__(self, host_ip, host_port=PORT) -> None:
        self.log = logging.getLogger(__name__)
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            self.log.fatal('Failed to create socket')
            sys.exit()
        
        self.log.debug('Socket created')

        self.sock.connect((host_ip, host_port))

        self.log.debug('Socket connected to ' + host_ip + '.')        

    def send_data(self, data:Dict) -> None:

        b_data = json.dumps(data).encode('utf-8')

        try:
            self.sock.send(b_data)
        except socket.error as e:
            self.log.error('Send failed: ' + e[1])
            #TODO: retry sending a few times

        self.log.debug('Data sent: '+ str(b_data))

    def recieve_data(self) -> Dict:
        b_data = self.sock.recv(4096)
        self.log.debug('Recieved: ' + str(b_data))
        return json.loads(b_data.decode('utf-8'))

    def close_connection(self) -> None:
        self.log.debug('Closing socket.')
        self.sock.close()