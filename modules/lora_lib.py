import serial
from threading import Lock
from types.wireless import WirelessModule

class LoRa_Commands:
    at = ""
    id = "ID"
    mode = "MODE"
    ptp = "TEST"

class LoRaE5(WirelessModule):

    def __init__(self, serialPort, region, mode, recieveCallback) -> None:

        self.command_in_use = Lock()

        freq = "903.3" #default freq America
        if(region==1):
            freq = "869.3"

        self.serPort = serialPort
        self.serCon = serial.Serial(self.serPort, 9600, timeout=5)

        self._sendCommand(LoRa_Commands.mode, "TEST")
        self._sendCommand(LoRa_Commands.ptp, "RFCFG," + freq + ",SF7,125,12,15,14,ON,OFF,OFF")
        
        self.isReciever = False
        if(mode == Modes.recieve):
            self.isReciever = True
            self.callback = recieveCallback
            self._sendCommand(LoRa_Commands.ptp, "RXLRPKT")
            self._loopRecieve()

    # This is a VERY BAD WAY to do this, but this is just demo code
    def _loopRecieve(self):
        while(True):
            line=self.serCon.readline()
            if(line):
                self.callback(line)

    def _sendCommand(self, command, parameterString):
        self.command_in_use.acquire()
        
        msg = "AT"
        if(command):
            msg += "+" + command
            
            if(parameterString):
                msg += "=" + parameterString
        
        msg += "\n\r"

        bmsg = bytes(msg, 'utf-8')
        self.serCon.write(bmsg)

        # TODO: a proper way to check that transaction is done
        line = self.serCon.readline()
        line = self.serCon.readline()

        self.command_in_use.release()


    def sendString(self, string) -> bool:
        if(not self.isReciever):
            self._sendCommand(LoRa_Commands.ptp, "TXLRSTR,\""+string+"\"")
            return True
        else:
            return False
