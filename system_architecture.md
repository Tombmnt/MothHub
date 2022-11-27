# MotHub architecture and module layout

- Mosquitto mqtt server: Mqtt broker, auto-started on py boot.
- Every module is a python program using mqtt to sub/pub to topics

## Topic list
These topics are the main topics available to pub/sub to, you can technically use custom topics, but undocumented topics are not recomended. All the documented topics are (should) be available in the `MqttTopics` from `modules/mqtt_utils.py`.
- speed: The boat's speed over ground, whether gps or calculated or otherwise.
- direction: The direction the boat is pointing/heading to. usually from gps or calculated.
- orientation: The 3 axis orientation of the boat in space (heel, roll, etc.).
- position: The geographical position of the boat in gps coordinates.
- wind_speed: The speed of the wind.
- wind_direction: The direction of the wind.
- strength: The strength data for strength/tension/etc. sensors. Needs to be formated with either the measurement type.

## Making a module
Here are basic module example for both pub and sub modules.
### Sub module
This sub module reads json data and displays it.
The given callback method has to have the `client, userdata, msg` parameters.
```python
import json
import paho.mqtt.client as mqtt
# Relative imports assuming this is in the modules folder.
from ..mqtt_modules import MqttSubModule 

class DemoSub(MqttSubModule):
    def __init__(self):
        super().__init__(mqtt_topic="demo")

        # Register callback methods that the client will call on getting data.
        self.register_client_callback("demo", self.on_message)

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        # msg.payload is a json string with a known format.
        data = json.loads(msg.payload) 
        print(f"Name: {data["name"]}, Type: {data["type"]}")
```
### Pub module
This pub module sends `Hello World` to the topic when `run()` is called.
```python
import json
import paho.mqtt.client as mqtt
# Relative imports assuming this is in the modules folder.
from ..mqtt_modules import MqttPubModule 

class DemoPub(MqttPubModule):
    def __init__(self):
        super().__init__(mqtt_topic="demo")

    def run(self):
        self.publish("demo", "Hello World")
```

