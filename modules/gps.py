import serial 
from pynmeagps import NMEAReader

from .mqtt_utils import MqttTopics
from .mqtt_modules import MqttPubModule

class ZED_F9P_Hat_GPS(MqttPubModule):
    def __init__(self, mqtt_broker: str = "localhost", mqtt_broker_port=1883, serial_port="/dev/ttyS0", baud="38400") -> None:
        super().__init__([MqttTopics.POSITION, MqttTopics.SPEED], mqtt_broker, mqtt_broker_port)

        self.serial_con = serial.Serial(serial_port, baud, timeout=5)
        self.nmea_stream = NMEAReader(self.serial_con)

    def run(self): # This is an infinite loop pooling the gps
        while True:
            raw_data, parsed_data = self.nmea_stream.read()
            print(f"{parsed_data}")

class GPS(ZED_F9P_Hat_GPS): pass

gps = GPS()
gps.run()