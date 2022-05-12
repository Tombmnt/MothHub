
#TODO: update to MQTT

from colorama.ansi import Style
from ..types.wireless import Modes, WirelessModule, WrongModeException
from colorama import Fore

class Mock_Lora(WirelessModule):
    def __init__(self, port, rate, region, mode, callback) -> None:
        print("---------------------------------------")
        print("Using a fake Lora Module:")
        print(' Serial port : ' + port)
        print(' Data rate :   ' + str(rate))
        print(" Region :      " + ("Europe" if region == 1 else "America"))
        print(" Mode :        " + ("RX" if mode == 1 else "TX"))
        print("---------------------------------------")
        
        self.connected = False
        self.sport = port
        self.region = region
        self.mode = mode
    
    def send_data(self, data) -> None:
        if self.mode == Modes.transmit:
            print(Fore.GREEN + "Fake Lora module on " + self.sport + " sends: " + Style.RESET_ALL + data)
        else:
            raise WrongModeException(Fore.MAGENTA + "Lora module on " + self.sport + " is not in transmit mode.")

    def connect(self) -> None:
        if not self.connected:
            self.connected = True
            print(Fore.GREEN + "Fake Lora module on "+ self.sport + " connected")
        else:
            print(Fore.YELLOW + "Fake Lora module on "+ self.sport + " is already connected")
        
    def disconnect(self) -> None:
        if self.connected:
            self.connected = False
            print(Fore.GREEN + "Fake Lora module on "+ self.sport + " disconnected")
        else:
            print(Fore.YELLOW + "Fake Lora module on "+ self.sport + " is already disconnected")
        