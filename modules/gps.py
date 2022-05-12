import datetime
import json
from turtle import pos
from xmlrpc.client import DateTime
import serial 
from pynmeagps import NMEAReader, NMEAMessage

from modules.data_models.mqtt_packets import MQTTPositionPkt, MQTTSpeedPkt, SenderTypes

from .mqtt_utils import MqttTopics
from .mqtt_modules import MqttPubModule

# Available message types: 
# ['$GNRMC', '$GNVTG', '$GNGGA', '$GNGSA', '$GPGSV', '$GLGSV', '$GAGSV', '$GBGSV', '$GNGLL']

# Used:
# RMC: Position, time
# VTG: Speed over ground
# GGA: Position, quality
NMEA_MESSAGE_GSA = "GSA"
NMEA_MESSAGE_RMC = "RMC"
NMEA_MESSAGE_VTG = "VTG"
NMEA_MESSAGE_GGA = "GGA"
NMEA_MESSAGE_GSV = "GSV"
NMEA_MESSAGE_GLL = "GLL"

class ZED_F9P_Hat_GPS(MqttPubModule):
    def __init__(self, mqtt_broker: str = "localhost", mqtt_broker_port=1883, serial_port="/dev/ttyS0", baud="38400") -> None:
        super().__init__([MqttTopics.POSITION, MqttTopics.SPEED], mqtt_broker, mqtt_broker_port)

        self.serial_con = serial.Serial(serial_port, baud, timeout=5)
        self.nmea_stream = NMEAReader(self.serial_con)

    def run(self): # This is an infinite loop pooling the gps
        while True:
            parsed_msg: NMEAMessage = None
            _, parsed_msg = self.nmea_stream.read()
            # TODO: actuall logging 
            print(f"{parsed_msg}")

            pos_data = MQTTPositionPkt(sender_type=SenderTypes.gps)
            dt: datetime.datetime = 0.0
                
            if(parsed_msg.msgID == NMEA_MESSAGE_RMC):
                # RMC message is the first relevant message we get per data burst, we can use it to send the timestamp for the whole burst.
                dt = datetime.datetime.combine(parsed_msg.date, parsed_msg.time).astimezone(datetime.timezone.utc)
                pos_data.time = int(dt.timestamp()) # time as a unix timestamp
                pos_data.lon = parsed_msg.lon
                pos_data.lonEW = parsed_msg.EW
                pos_data.lat = parsed_msg.lat
                pos_data.latNS = parsed_msg.NS
                pos_data.add_data("nav_status", parsed_msg.navStatus)

            elif(parsed_msg.msgID == NMEA_MESSAGE_GGA):
                pos_data.add_data("quality", parsed_msg.quality)
                pos_data.add_data("sat_nbr", parsed_msg.numSV)
                pos_data.add_data("h_precision", parsed_msg.HDOP) #in meters
                pos_data.add_data("altitude", parsed_msg.alt)
                pos_data.add_data("alt_unit", parsed_msg.altUnit)
                pos_data.add_data("geoid_sep", parsed_msg.sep)
                pos_data.add_data("geoid_sep_unit", parsed_msg.sepUnit)

                # The GGA message is the last (relevant) message we get for each data burst
                self.publish(MqttTopics.POSITION, str(pos_data))
                pos_data.reset_to_default()
                pos_data.type = SenderTypes.gps
                dt = 0.0

            elif(parsed_msg.msgID == NMEA_MESSAGE_VTG):
                spd_data = MQTTSpeedPkt(
                    timestamp = int(dt.timestamp()),
                    sender_type = SenderTypes.gps,
                    speed = parsed_msg.sogn, # Speed by default in knots
                    speed_unit = parsed_msg.sognUnit,
                    direction = parsed_msg.cogt, # Course over groub by default in degree true
                    direction_unit = parsed_msg.cogtUnit
                )
                spd_data.add_data_mul_dict({"speed_kmh": parsed_msg.sogk, "dir_mag": parsed_msg.cogm})

                self.publish(MqttTopics.POSITION, str(spd_data))

class GPS(ZED_F9P_Hat_GPS): pass

gps = GPS()
gps.run()