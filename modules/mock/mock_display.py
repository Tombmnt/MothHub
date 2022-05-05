import json
import multiprocessing
import pyglet
import numpy as np 
import paho.mqtt.client as mqtt
from modules.mqtt_modules import MqttSubModule
from modules.mqtt_utils import MqttTopics

class MockDisplay(MqttSubModule):
    def __init__(self, w: int = 320, h: int = 240) -> None:
        super().__init__(mqtt_topics=[MqttTopics.SPEED])
        self.register_client_callback(MqttTopics.SPEED, self.on_speed_message)

        self.width = w
        self.height = h
        self.frame_data = np.zeros((h, w, 3), dtype=np.ubyte)
        self.frame_data[0:h, 0:w] = [150, 150, 150]
        
        self.speed = 0

        self.display_thread()
        #self.display = multiprocessing.Process(target=self.display_thread)
        #self.display.start()

    def convert_frame(self) -> list:
        raw_data = self.frame_data.flatten()
        return (pyglet.gl.glu.GLubyte * len(raw_data))(*raw_data)

    def on_speed_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        print(f"Recieved: [{msg.topic}]:{msg.payload}\n")
        data = json.loads(msg.payload)
        if(data):
            self.speed = data["value"]

        #data = json.loads(msg.payload)
        #if(data):
        #    if(data["command"] == "square"):
        #        self.add_colored_quare(data["pos_x"], data["pos_y"], data["width"], data["height"], data["color"])

    # Draws a colored square on the screen
    # requires a "command" as a dict:
    #{
    #    "command":"square",
    #    "pos_x":0,
    #    "pos_y":0,
    #    "width":20,
    #    "height":20,
    #    "color":[255, 255, 255]
    #}
    def add_colored_quare(self, pos_x: int, pos_y: int, w: int, h: int, color) -> None:
        for x in range(0, w):
            for y in range(0, h):
                if(((x + pos_x) < self.width) and ((y + pos_y) < self.height)):
                    self.frame_data[y + pos_y, x + pos_x] = color

    def display_thread(self):

        window = pyglet.window.Window(self.width, self.height)
        speed_label = pyglet.text.Label(text='Speed: '+str(self.speed), font_size=36, color=(0, 0, 150, 255),
            anchor_x='center', anchor_y='center', x=window.width//2, y=window.height//2)

        @window.event
        def on_draw():
            window.clear()
            scr = pyglet.image.ImageData(self.width, self.height, 'RGB', self.convert_frame())
            scr.blit(0, 0)
            speed_label.draw()

        def update(dt):
            speed_label.text = 'Speed: '+str(self.speed)
            
        pyglet.clock.schedule_interval(update, 1/60)
        pyglet.app.run()



MockDisplay()

input("Press enter to quit...")
