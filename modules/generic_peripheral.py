from modules.socket_client import Socket_Client

class Generic_Peripheral():
    def __init__(self, client_type: str, client_name: str, host_ip: str, port: int = None) -> None:
        self.type = client_type
        self.name = client_name

        if port:
            self.socket_client = Socket_Client(self.type, self.name, host_ip, port)
        else:
            self.socket_client = Socket_Client(self.type, self.name, host_ip)

    def run(self):
        raise NotImplementedError

    def __del__(self):
        self.socket_client.close_connection()