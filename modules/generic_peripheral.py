from modules.socket_client import Socket_Client

class Generic_Peripheral():
    def __init__(self, host_ip: str, port: int = None) -> None:
        
        if port:
            self.socket_client = Socket_Client(host_ip, port)
        else:
            self.socket_client = Socket_Client(host_ip)

    def __del__(self):
        self.socket_client.close_connection()