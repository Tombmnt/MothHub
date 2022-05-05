import datetime
import json
import random
from time import sleep
from modules.mqtt_modules import MqttPubModule
from modules.mqtt_utils import MqttTopics

class MockGPS(MqttPubModule):
    def __init__(self) -> None:
        super().__init__([MqttTopics.SPEED, MqttTopics.POSITION, MqttTopics.DIRECTION])

    def send_random_speed(self):
        speed = random.randrange(0, 25)
        data = {
            "time": datetime.datetime.utcnow(),
            "type": "gps",
            "value": speed
        }
        self.publish(MqttTopics.SPEED, json.dumps(data))

    def send_random_position(self):
        lat = random.randrange(0, 25)
        lon = random.randrange(0, 25)
        data = {
            "time": datetime.datetime.utcnow(),
            "type": "gps",
            "latitude": lat,
            "longitude": lon
        }
        self.publish(MqttTopics.SPEED, json.dumps(data))

    def run(self):
        while(1):
            self.send_random_speed()
            sleep(1)

    # TODO: send random position and direction


MockGPS().run()