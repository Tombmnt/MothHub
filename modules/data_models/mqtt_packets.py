from dataclasses import dataclass
import json
from typing import Any
from calypso_anemometer.core import CalypsoDeviceApi, Settings
from calypso_anemometer.model import CalypsoReading


# Default init values "defines"
DEFAULT_TIMESTAMP = 0
DEFAULT_SENDER_TYPE = "null"

DEFAULT_LONGITUDE = 0.0 
DEFAULT_LON_DIR = "W" 
DEFAULT_LATITUDE = 0.0, 
DEFAULT_LAT_DIR = "N"

DEFAULT_SPEED = 0.0
DEFAULT_SPEED_UNIT = "N"
DEFAULT_DIRECTION = "0.0"
DEFAULT_DIRECTION_UNIT = "T"


DEFAULT_NAME ="calyso_anemo"
#DEFAULT_WIND_SPD = 0.0
#DEFAULT_WIND_DIR = 0.0

@dataclass
class SenderTypes:
    gps = "gps",
    imu = "imu"
    other = "unknown"
    wind ="wind"

class MQTTPacket:
    def __init__(self, 
        timestamp: int = DEFAULT_TIMESTAMP, 
        sender_type: str = DEFAULT_SENDER_TYPE
    ):
        self.time = timestamp
        self.type = sender_type

    def __str__(self) -> str:
        return json.dumps(self.__dict__)
    
    def add_data(self, name: str, value: Any):
        setattr(self, name, value)
    
    def add_data_mul_dict(self, data_dict: dict):
        for n, v in data_dict.items():
            setattr(self, n, v)
    
    def reset_to_default(self):
        dict = self.__dict__.copy()
        for attr in dict.keys():
            delattr(self, attr)
        self.__init__()

class MQTTPositionPkt(MQTTPacket):
    def __init__(self, 
        timestamp: int = DEFAULT_TIMESTAMP, 
        sender_type: str = DEFAULT_SENDER_TYPE, 
        longitude: float = DEFAULT_LONGITUDE, 
        lon_dir: str = DEFAULT_LON_DIR, 
        latitude: float = DEFAULT_LATITUDE, 
        lat_dir: str = DEFAULT_LAT_DIR
    ):
        super().__init__(timestamp, sender_type)
        self.lon = longitude
        self.lonEW = lon_dir
        self.lat = latitude
        self.latNS = lat_dir

class MQTTSpeedPkt(MQTTPacket):
    def __init__(self, 
        timestamp: int = DEFAULT_TIMESTAMP, 
        sender_type: str = DEFAULT_SENDER_TYPE,
        speed: float = DEFAULT_SPEED,
        speed_unit: str = DEFAULT_SPEED_UNIT,
        direction: float = DEFAULT_DIRECTION,
        direction_unit: str = DEFAULT_DIRECTION_UNIT
    ):
        super().__init__(timestamp, sender_type)
        self.speed = speed,
        self.spd_unit = speed_unit,
        self.dir = direction,
        self.dir_unit = direction_unit

class MQTTOrientationPkt(MQTTPacket):
    def __init__(self, 
        timestamp: int = DEFAULT_TIMESTAMP,
        sender_type: str  = DEFAULT_SENDER_TYPE, 
        acceleration: "tuple(float, float, float)" = (0.0, 0.0, 0.0), # x, y, z, ms^2, constant acceleration (gravity + movement)
        linear_acceleration: "tuple(float, float, float)" = (0.0, 0.0, 0.0), # x, y, z ms^2, dynamic acceleration (movement)
        rotation: "tuple(float, float, float, float)" = (0.0, 0.0, 0.0, 0.0), # Quaternion, 
        gyroscope: "tuple(float, float, float)" = (0.0, 0.0, 0.0) # x, y, z radian/sec
    ):
        super().__init__(timestamp, sender_type)
        self.acc_x, self.acc_y, self.acc_z = acceleration
        self.lin_x, self.lin_y, self.lin_z = linear_acceleration
        self.rot_w, self.rot_x, self.rot_y, self.rot_z = rotation
        self.gyr_x, self.gyr_y, self.gyr_z = gyroscope



class MQTTwindPkt(MQTTPacket):
    def __init__(self,
        timestamp: int = DEFAULT_TIMESTAMP,
        sender_type: str = DEFAULT_SENDER_TYPE,
        #name: str = DEFAULT_NAME,
        wind_spd: float = (0.0),
        wind_dir: int = (0) 
    ):

        super().__init__(timestamp, sender_type)
        #DEFAULT_NAME = name
        self.wind_speed=wind_spd
        self.wind_direction =wind_dir
