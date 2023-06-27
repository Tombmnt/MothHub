from typing import Any, Callable
import paho.mqtt.client as mqtt
from modules.mqtt_utils import MqttPubClient, MqttSubClient

class MqttSubModule:
    def __init__(self, mqtt_topics: "list[str]", mqtt_broker: str = "localhost", mqtt_broker_port: int = 1883, start=True) -> None:
        self.mqtt_clients: "dict[str, MqttSubClient]" = {}
        
        for topic in mqtt_topics:
            self.mqtt_clients[topic] = MqttSubClient(topic, mqtt_broker, mqtt_broker_port, start)

    def register_client_callback(self, topic: str, callback: Callable[[mqtt.Client, Any, mqtt.MQTTMessage], Any]):
        self.mqtt_clients[topic].message_callback_add(topic, callback)

class MqttPubModule:
    def __init__(self, mqtt_topics: "list[str]", mqtt_broker: str = "localhost", mqtt_broker_port = 1883) -> None:
        self.mqtt_clients: "dict[str, MqttPubClient]" = {}
        
        for topic in mqtt_topics:
            self.mqtt_clients[topic] = MqttPubClient(topic, mqtt_broker, mqtt_broker_port)

    def publish(self, topic: str, message: str):
        self.mqtt_clients[topic].publish(message)

    def publish_all(self, message: str):
        for client in self.mqtt_clients.values():
            client.publish(message)