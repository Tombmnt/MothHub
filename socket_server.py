import socket, sys, threading, logging, json
from time import sleep
from typing import List

from database_service import Database_Service
from handlers.display_handler import Display_Handler
from modules.types.peripherals import peripheral_types

HOST = ""
PORT = 6684  # moth on a phone

#Server starts as a Thread itself to allow main program to continue with it's jobs
class Socket_Server(threading.Thread):

    def __init__(self, data_handler: Database_Service) -> None:
        threading.Thread.__init__(self)

        self.daemon = False #daemon threads are killed when main thread exits, non-daemon threads will force to main thread to wait.

        self.clients = [] #Storing all the clients
        self.running = True
        self.data_handler = data_handler

        self.log = logging.getLogger(__name__)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log.debug("Socket created")

        try:
            self.sock.bind((HOST, PORT))
        except socket.error as e:
            self.log.fatal('Bind failed: \nError: ' + str(e[0]) + ' \nMessage: ' + e[1])
            sys.exit()
        
        self.log.debug("Socket bind complete")
        
        self.sock.listen(50)
        self.log.debug("Socket listening...")

        self.start() #Start the thread

    def run(self) -> None:
        while(self.running):
            #wait to accept a connection - blocking call
            conn, addr = self.sock.accept()
            self.log.info('Connected with '+ str(addr[0]) + ':' + str(addr[1]))
            
            self.clients.append(Client_Thread(conn, addr, self.data_handler)) # auto starts the client thread

        self.sock.close()

    def stop(self) -> None:
        self.running = False

class Client_Thread(threading.Thread):
    def __init__(self, client_conn : socket.socket, client_addr : List, data_handler: Database_Service):
        threading.Thread.__init__(self)
        self.peripheric_handler = None

        logging.debug("Checking client type for " + str(client_addr))
        b_data = client_conn.recv(4096)
        if(b_data):
            data = json.loads(b_data.decode('utf-8'))
        else:
            logging.error("Client did not sent identifier, closing... ")
            client_conn.close()
            sys.exit()

        if(data["type"] == peripheral_types.display):
            logging.debug("Client is type " + peripheral_types.display)
            self.peripheric_handler = Display_Handler(client_conn, client_addr, data["name"], data_handler)
        else:
            logging.info("Client " + str(client_addr) + "'s type is unknown, closing connection and skipping.")
            client_conn.close()
            sys.exit() # exit the thread

        self.start()

    def run(self):    
        self.peripheric_handler.run()

