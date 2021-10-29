import socket, sys, logging, json, time
from typing import Any, Dict

PORT = 6684
MAX_TRIES = 10

class Socket_Client():
    def __init__(self, client_type: str, client_name: str, host_ip: str, host_port=PORT) -> None:
        self.log = logging.getLogger(__name__)
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            self.log.fatal('Failed to create socket:' + str(e))
            sys.exit()
        
        self.log.debug('Socket created')

        self.host_ip = host_ip
        self.host_port = host_port
        self.sock.connect((host_ip, host_port))
        self.log.debug('Socket connected to ' + host_ip + '.')     

        self.cl_type = client_type
        self.cl_name = client_name
        self.send_data({
            "type": self.cl_type,
            "name": self.cl_name
        })

    def reconnect(self) -> None:
        self.sock.close()
        time.sleep(0.1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for i in range(1, MAX_TRIES + 1):
            try:
                self.log.info('Trying to reconnect to ' + str(self.host_ip) + ':' + str(self.host_port) + ' (' + str(i) + '/' + str(MAX_TRIES) + ')')
                self.sock.connect((self.host_ip, self.host_port))
                
                self.send_data({
                    "type": self.cl_type,
                    "name": self.cl_name
                })
                return #on success
            except socket.error as e:
                self.log.error('Failed to reconnect to ' + str(self.host_ip) + ':' + str(self.host_port) + ' (' + str(i) + '/' + str(MAX_TRIES) + ')\nError: ' + str(e))

                if (i == MAX_TRIES):
                    logging.error('Server lost, exiting.')
                    sys.exit() # kill this thread. 
            
            time.sleep(1)

    def send_data(self, data:Dict) -> None:

        b_data = json.dumps(data).encode('utf-8')

        for i in range(1, MAX_TRIES + 1):
            try:
                self.sock.send(b_data)
                logging.debug('Data sent: '+ str(b_data))
                break # success => break out of the loop.
            except socket.error as e:
                logging.error('Send failed: ' + str(e) + ', retrying... (' + str(i) + '/' + str(MAX_TRIES) + ')')
                time.sleep(1)

                if(i == MAX_TRIES): #last try failed
                    logging.error('Server lost, exiting.')
                    sys.exit() # kill this thread. 
        
    # Blocking!!! 
    def recieve_data(self) -> Dict:
        try:
            b_data = self.sock.recv(4096)
            self.log.debug('Recieved: ' + str(b_data))
            if b_data:
                return json.loads(b_data.decode('utf-8'))
            else:
                self.reconnect()

        except socket.error as e:
            self.log.error("Failed to recieve data: "+ str(e))
            self.reconnect()

    def close_connection(self) -> None:
        self.log.debug('Closing socket.')
        self.sock.close()